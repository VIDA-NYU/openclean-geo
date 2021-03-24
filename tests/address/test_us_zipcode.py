# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the U.S. Zip code to city mapping."""

from openclean_geo.address.uszipcode import USZipToCity


def test_us_zipcode_eval():
    """Test functionality of the Zip-code to city name mapping."""
    assert USZipToCity().eval('10003') == 'New York'


def test_us_zipcode_lookup():
    """Test functionality of the Zip-code lookup library."""
    assert USZipToCity().lookup(10003)['zipcode'] == '10003'
