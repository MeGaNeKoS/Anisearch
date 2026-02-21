"""Tests for Connection (sync) with mocked HTTP."""

import json
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from Anisearch.connection import Connection
from Anisearch.errors import (
    RateLimitError, ServerError,
    ConnectionError as AnilistConnectionError,
)
from Anisearch.retry import RetryStrategy
import requests


def _mock_response(status_code=200, json_data=None, text="", headers=None):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.text = text or json.dumps(json_data or {})
    resp.headers = headers or {}
    if json_data is not None:
        resp.json.return_value = json_data
    else:
        resp.json.side_effect = json.JSONDecodeError("fail", "", 0)
    return resp


class TestConnectionRequest(unittest.TestCase):
    def test_successful_request(self):
        conn = Connection(retry=RetryStrategy(max_retries=0))
        data = {"data": {"Media": {"id": 1}}}
        with patch.object(conn.session, "post", return_value=_mock_response(200, data)):
            result = conn.request({"id": 1}, "query { Media(id: $id) { id } }")
        self.assertEqual(result, data)

    def test_filters_none_variables(self):
        conn = Connection(retry=RetryStrategy(max_retries=0))
        data = {"data": {}}
        with patch.object(conn.session, "post", return_value=_mock_response(200, data)) as mock_post:
            conn.request({"id": 1, "type": None}, "query")
            call_kwargs = mock_post.call_args
            sent_json = call_kwargs[1]["json"] if "json" in call_kwargs[1] else call_kwargs.kwargs["json"]
            self.assertNotIn("type", sent_json["variables"])

    def test_rate_limit_raises(self):
        conn = Connection(retry=RetryStrategy(max_retries=0))
        resp = _mock_response(429, headers={"Retry-After": "30"})
        resp.json.return_value = {}  # won't be reached
        with patch.object(conn.session, "post", return_value=resp):
            with self.assertRaises(RateLimitError) as ctx:
                conn.request({}, "query")
            self.assertEqual(ctx.exception.retry_after, 30)

    def test_server_error_raises(self):
        conn = Connection(retry=RetryStrategy(max_retries=0))
        resp = _mock_response(500, text="Internal Server Error")
        with patch.object(conn.session, "post", return_value=resp):
            with self.assertRaises(ServerError) as ctx:
                conn.request({}, "query")
            self.assertEqual(ctx.exception.status_code, 500)

    def test_connection_error_raises(self):
        conn = Connection(retry=RetryStrategy(max_retries=0))
        with patch.object(conn.session, "post", side_effect=requests.exceptions.ConnectionError("refused")):
            with self.assertRaises(AnilistConnectionError):
                conn.request({}, "query")

    @patch("Anisearch.retry.time.sleep")
    def test_retry_on_rate_limit(self, mock_sleep):
        conn = Connection(retry=RetryStrategy(max_retries=1, on_rate_limit="wait", max_wait=5))
        rate_resp = _mock_response(429, headers={"Retry-After": "2"})
        ok_resp = _mock_response(200, {"data": {}})
        with patch.object(conn.session, "post", side_effect=[rate_resp, ok_resp]):
            result = conn.request({}, "query")
        self.assertEqual(result, {"data": {}})

    @patch("Anisearch.retry.time.sleep")
    def test_retry_on_server_error(self, mock_sleep):
        conn = Connection(retry=RetryStrategy(max_retries=1, on_server_error="backoff"))
        err_resp = _mock_response(502, text="Bad Gateway")
        ok_resp = _mock_response(200, {"data": {}})
        with patch.object(conn.session, "post", side_effect=[err_resp, ok_resp]):
            result = conn.request({}, "query")
        self.assertEqual(result, {"data": {}})

    @patch("Anisearch.retry.time.sleep")
    def test_retry_on_connection_error(self, mock_sleep):
        conn = Connection(retry=RetryStrategy(max_retries=1, on_connection_error="backoff"))
        ok_resp = _mock_response(200, {"data": {}})
        with patch.object(conn.session, "post", side_effect=[
            requests.exceptions.ConnectionError("timeout"), ok_resp
        ]):
            result = conn.request({}, "query")
        self.assertEqual(result, {"data": {}})

    def test_json_decode_error_returns_error_dict(self):
        conn = Connection(retry=RetryStrategy(max_retries=0))
        resp = _mock_response(200, text="not json")
        with patch.object(conn.session, "post", return_value=resp):
            result = conn.request({}, "query")
        self.assertIn("errors", result)
        self.assertEqual(result["errors"][0]["message"], "Failed to convert to JSON")

    def test_max_retries_exhausted_returns_error(self):
        conn = Connection(retry=RetryStrategy(max_retries=1, on_server_error="raise"))
        resp = _mock_response(500, text="error")
        with patch.object(conn.session, "post", return_value=resp):
            with self.assertRaises(ServerError):
                conn.request({}, "query")

    def test_no_retry_strategy(self):
        conn = Connection(retry=None)
        data = {"data": {"Media": {"id": 1}}}
        with patch.object(conn.session, "post", return_value=_mock_response(200, data)):
            result = conn.request({"id": 1}, "query")
        self.assertEqual(result, data)

    def test_no_strategy_connection_error(self):
        conn = Connection(retry=None)
        with patch.object(conn.session, "post", side_effect=requests.exceptions.ConnectionError("fail")):
            with self.assertRaises(AnilistConnectionError):
                conn.request({}, "query")

    def test_legacy_num_retries(self):
        """Legacy num_retries param creates a temporary strategy."""
        conn = Connection(retry=None)
        data = {"data": {}}
        with patch.object(conn.session, "post", return_value=_mock_response(200, data)):
            result = conn.request({}, "query", num_retries=3)
        self.assertEqual(result, data)

    def test_custom_settings(self):
        settings = {
            "header": {"Content-Type": "application/json"},
            "api_url": "https://custom.api/graphql",
        }
        conn = Connection(setting=settings, retry=None)
        self.assertEqual(conn.settings["api_url"], "https://custom.api/graphql")

    def test_custom_params(self):
        conn = Connection(custom_param={"verify": False}, retry=None)
        self.assertEqual(conn.custom_param, {"verify": False})


class TestAnilistInit(unittest.TestCase):
    def test_default_init(self):
        from Anisearch import Anilist
        a = Anilist()
        self.assertIsNotNone(a._retry)

    def test_custom_retry(self):
        from Anisearch import Anilist
        r = RetryStrategy(max_retries=5)
        a = Anilist(retry=r)
        self.assertEqual(a._retry.max_retries, 5)

    def test_log_name(self):
        from Anisearch import Anilist
        a = Anilist(log_name="test")
        self.assertIn("test", a.logger.name)

    def test_log_level_without_name_warns(self):
        import warnings
        from Anisearch import Anilist
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            a = Anilist(log_level=10)
            self.assertTrue(any("log_level is ignored" in str(warning.message) for warning in w))

    def test_set_logger_level(self):
        import logging
        from Anisearch import Anilist
        Anilist.set_logger_level(logging.WARNING)
        self.assertEqual(Anilist.logger.level, logging.WARNING)
        # Reset
        Anilist.set_logger_level(logging.NOTSET)


if __name__ == "__main__":
    unittest.main()
