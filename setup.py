import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gs1-compression",
    version="0.1.3",
    author="Di Zhu",
    author_email="di.zhu@trust.codes",
    description=("A Python package to handle compression"
                 " and decompression of GS1 digital links"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Trust-Codes-Ltd/gs1-compression",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
