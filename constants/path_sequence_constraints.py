"""pathSequenceConstraints is used to ensure that for those
 primary identification keys in which multiple key qualifiers may
  appear in the URI path information, they SHALL appear in the expected order.

Note that currently only GTIN (01) and ITIP (8006)
 have more than one permitted key qualifier.
"""
PATH_SEQUENCE_CONSTRAINTS = {"01": ["22", "10", "21"],
                             "8006": ["22", "10", "21"]}
