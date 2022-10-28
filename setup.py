from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

with open("CHANGELOG.txt", encoding="utf-8") as f:
    CHANGELOG = f.read()

setup(
    name='Anisearch',
    version='1.1.0',
    description="Anisearch is the lib for accessing anime or manga from anilist.co on the Python Platform.",
    long_description=README + "\n\n" + CHANGELOG,
    long_description_content_type="text/markdown",
    url='https://github.com/MeGaNeKoS/Anisearch',
    license='MIT',
    author='めがねこ',
    author_email='evictory91@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    keywords="Anime Manga Anilist",
    install_requires=['requests']
)
