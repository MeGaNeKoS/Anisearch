from setuptools import setup, find_packages

setup(
    name='Anisearch',
    version='1.0.2',
    description="Anisearch is the lib for accessing anime or manga from anilist.co on the Python Platform.",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
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
