# GS1 Digital Link Decompression Prototype in Python
This is a Python translation of the JavaScript Toolkit that decompresses element strings to GS1 digital links.

## Background

The GS1 identification system is widely used worldwide within product barcodes, as well as within barcodes for shipments, assets, locations and so on.

Further information about GS1 can be found at https://www.gs1.org

Details about the GS1 identification system and GS1 Application Identifiers can be found in the GS1 General Specifications at https://www.gs1.org/docs/barcodes/GS1_General_Specifications.pdf and a searchable list of GS1 Application Identifiers is at https://www.gs1.org/standards/barcodes/application-identifiers?lang=en

GS1 Digital Link is a new Web URI syntax for expressing GS1 Application Identifiers and their values in a Web-friendly format, to make it easier to connect identifiers of products, shipments, locations, assets etc. to related online information and services on the Web via simple Web redirects using Web resolver infrastructure.

The GS1 Digital Link syntax is defined in https://www.gs1.org/standards/Digital-Link/1-0

A demonstration tool is available at https://id.gs1.org/uritool although it does not currently use this toolkit

See also https://github.com/gs1/digital-link.js for a related toolkit for GS1 Digital Link

## Examples

    https://dlnkd.tn.gg/01/09780345418913
    
    https://dlnkd.tn.gg/01/05412345000013/10/ABC%26%2B123?7003=1903061658&k1=v1

## Installation 

To install, make sure Python3 is installed, and installation in a virtual environment is preferred.

    $ pip install gs1-compression
    
## Decompression

To decompress a compressed GS1 Digital Link URI, import `decompress_gs1_digital_link`:

    >>> from gs1 import decompress_gs1_digital_link

An example of decompression:

    >>> compressed_uri = "https://dlnkd.tn.gg/ARHKVAdpQg"
    >>> original_link = decompress_gs1_digital_link(compressed_uri, use_short_text=False, uri_stem="https://dlnkd.tn.gg")
    >>> print("Original Link: " + original_link)
        Original Link: https://dlnkd.tn.gg/01/09780345418913
The `decompress_gs1_digital_link` function has three parameters.

Set the second parameter, `use_short_text=True` if you prefer the GS1 Digital Link URI 
to use alphabetic mnemonic short names as defined in the GS1 Digital Link standard, e.g. /gtin/. 
Set it `False` if you prefer the GS1 Digital Link URI to use all-numeric GS1
 application identifiers, e.g. /01/.

Set the third parameter, `uri_stem` to a valid URI prefix if you wish to construct 
a GS1 Digital Link using a specific domain name. If it's set to be `None` or `''`,
a default URI prefix `https://id.gs1.org` will be used.

## Contributors

- Di Zhu    di.zhu@trust.codes
