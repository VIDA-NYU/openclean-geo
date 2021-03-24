# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the US street number suffix filter."""

import pytest

from openclean.function.token.base import Token
from openclean_geo.address.usstreet import StreetNumberSuffixFilter


@pytest.mark.parametrize(
    'tokens,result',
    [
        (['ST', '1', 'Str'], ['ST', '1', 'Str']),
        (['W', '1', 'ST', 'Str'], ['W', '1', 'Str']),
        (['W', '22', 'ND'], ['W', '22']),
        (['W', '23', 'RD', 'RD'], ['W', '23', 'RD']),
        (['W', '23', 'ST', 'RD'], ['W', '23', 'ST', 'RD']),
        (['5', 'TH', 'Ave'], ['5', 'Ave'])
    ]
)
def test_streetnr_suffix_filter(tokens, result):
    """Test the street number suffix filter functionality."""
    filter = StreetNumberSuffixFilter()
    assert filter.transform([Token(t) for t in tokens]) == result
