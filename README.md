# GS1 Digital Link Decompression Prototype in Python
This package is a Python conversion of the [GS1 digital link compression prototype](https://github.com/gs1/GS1DigitalLinkCompressionPrototype) in Javascript.

* [Background](#Background)
* [Examples](#Examples)
* [Installation](#Installation)
* [Usage](#Usage)
* [Contributors](#contributors)
* [Disclaimer](#disclaimer)
* [License](#License)

## Background

The GS1 identification system is widely used worldwide within product barcodes, as well as within barcodes for shipments, assets, locations and so on.

Further information about GS1 can be found at https://www.gs1.org

Details about the GS1 identification system and GS1 Application Identifiers can be found in the GS1 General Specifications at https://www.gs1.org/docs/barcodes/GS1_General_Specifications.pdf and a searchable list of GS1 Application Identifiers is at https://www.gs1.org/standards/barcodes/application-identifiers?lang=en

GS1 Digital Link is a new Web URI syntax for expressing GS1 Application Identifiers and their values in a Web-friendly format, to make it easier to connect identifiers of products, shipments, locations, assets etc. to related online information and services on the Web via simple Web redirects using Web resolver infrastructure.

The GS1 Digital Link syntax is defined in https://www.gs1.org/standards/Digital-Link/1-0

A demonstration tool is available at https://id.gs1.org/uritool although it does not currently use this toolkit

See also https://github.com/gs1/digital-link.js for a related toolkit for GS1 Digital Link

## Examples

The following example uses the all-numeric application identifier `01` to indicate GTIN.

    https://id.gs1.org/01/09780345418913
    
The following example uses short texts `gtin` `lot` and `expdt` to indicate GTIN, lot number and expiry date. A non-GS1 key-value pair `{'k1': 'v1'}` also appeared in this example.

    https://id.gs1.org/gtin/05412345000013/lot/ABC%26%2B123?expdt=1903061658&k1=v1

## Installation 

To install, make sure Python3 is installed, and installation in a virtual environment is preferred.

    $ pip install --upgrade gs1-compression
    
## Usage

### Decompression

To decompress a compressed GS1 Digital Link URI, import `decompress_gs1_digital_link`:

    >>> from gs1 import decompress_gs1_digital_link

An example of decompression:

    >>> compressed_uri = "https://id.gs1.org/ARHKVAdpQg"
    >>> original_link = decompress_gs1_digital_link(compressed_uri, use_short_text=False)
    >>> print("Original Link: " + original_link)
        Original Link: https://id.gs1.org/01/09780345418913
The `decompress_gs1_digital_link` function has two parameters.

Set the second parameter, `use_short_text=True` if you prefer the GS1 Digital Link URI 
to use alphabetic mnemonic short names as defined in the GS1 Digital Link standard, e.g. /gtin/. 
Set it `False` if you prefer the GS1 Digital Link URI to use all-numeric GS1
 application identifiers, e.g. `/01/`.

### Compression
To compress a full-length GS1 digital link, import `compress_gs1_digital_link`:

    >>> from gs1 import compress_gs1_digital_link

A code snippet of GS1 digital link compression:

    >>> full_uri = "https://id.gs1.org/gtin/9421902960055/lot/2010005828/ser/xyz1234"
    >>> compressed_link = compress_gs1_digital_link(digital_link_uri=full_uri, use_optimizations=False, compress_other_key_value_pairs=False)
    >>> print("Compressed Link: " + compressed_link)
        Compressed Link: https://id.gs1.org/AREjalurbiAUO-cgohCz45Z67b8A

There are four parameters in the function: 

- Pass the full length URI in the `digital_link_uri` parameter.

- Pass the URI prefix in the `uri_stem` parameter. Normally you might want to be the same as the full-length URI's prefix.

- Set `use_optimizations=True` if you would like to use optimized encoding of GS1 application identifiers and save more characters in the compressed string. By default, it's set to be `False`.

- Set `compress_other_key_value_pairs=True` if you would like to compress non-GS1 key-value pairs in the full URI. By default, it's set to be `False`.

## Contributors

- Di Zhu    di.zhu@trust.codes

## Sponsors

- [Trust Codes Limited](https://www.trust.codes/) : Using anti-counterfeit solutions and supply-chain traceability, Trust Codes® data-driven software connects brands to consumers with item level serialisation and world leading algorithms. 

## Disclaimer

### Legal Notice
In addition to the terms of the licence, this source code is provided by Trust Codes Limited, a New Zealand company, on an as-is basis, with no warranty expressed or implied. Neither Trust Codes Limited nor the contributors accept any liability for its use nor for any damages caused through its use. Trust Codes® is a registered trademark of Trust Codes Limited in New Zealand.
 
 All Rights Reserved.
  
  © Trust Codes Limited 2021.

## License

Apache-2.0 License
