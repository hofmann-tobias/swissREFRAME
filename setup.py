import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='swissREFRAME',
    version='1.0.0',
    author='adal02',
    author_email='hofmann.tobias121@gmail.com',
    description="Interface for the official swisstopo's REFRAME DLL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/adal02/swissREFRAME',
    download_url='https://github.com/adal02/swissREFRAME/archive/V1.0.0.tar.gz',
    install_requires=['comtypes'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords=["geodesy", "geography", "swiss", "coordinates", "transformation"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ]
)
