import setuptools

from swissreframe import __meta__ as meta

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=meta.__title__,
    version=meta.__release__,
    author=meta.__author__,
    author_email=meta.__author_email__,
    descriptclearion=meta.__description__,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url=meta.__url__,
    download_url=meta.__download_url__,
    install_requires=['JPype1'],
    packages=['swissreframe'],
    include_package_data=True,
    keywords=["geodesy", "geography", "swiss", "coordinates", "transformation"],
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
