import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gs1-compression",
    version="0.0.2",
    author="Di Zhu",
    author_email="di.zhu@trust.codes",
    description="A Python package to decompress compressed GS1 digital link",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TrustCodes/gs1-compression",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
