# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the US street token generator and collision key generator."""

import pytest

from openclean_geo.address.usstreet import USStreetNameKey, USStreetNameTokenizer


@pytest.mark.parametrize(
    'value,key',
    [('W 35th Street', '35 ST WEST')]
)
def test_us_street_collision_key_generator(value, key):
    """Test the collision key generator for U.S. street addresses."""
    assert USStreetNameKey().eval(value) == key


@pytest.mark.parametrize(
    'value,key',
    [
        ('W 35th Street', ['WEST', '35', 'ST']),
        ('E First Str/2nd Avenue', ['EAST', '1', 'STR', '/', '2', 'AVE']),
    ]
)
def test_us_street_tokenizer(value, key):
    """Test the U.S. street addresses tokenizer."""
    assert USStreetNameTokenizer().tokens(value) == key
