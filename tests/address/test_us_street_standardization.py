# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the US street prefix and suffix standardizer."""

import pytest

from openclean.function.token.base import Token, CapitalizeTokens, LowerTokens, UpperTokens
from openclean_geo.address.usstreet import StandardizeUSStreetName, UpdateStreetPrefixSuffix
from openclean_geo.address.usstreet import DIRECTION, STREET_TYPE

import openclean.function.token.base as TT


@pytest.mark.parametrize(
    'inputs,result_text,result_types',
    [
        ([], '', []),
        (['AVE', 'of', 'the', 'Americas'], 'AVENUE of the Americas', [TT.ALPHA] + [TT.ANY] * 3),
        (['W', '35', 'STR'], 'WEST 35 ST', [DIRECTION, TT.ANY, STREET_TYPE]),
        (['35', 'STR', 'W'], '35 STR W', [TT.ANY] * 3)
    ]
)
def test_street_prefix_suffix_standardization(inputs, result_text, result_types):
    """Test functionality of the Street address prefix and suffix
    standardizer.
    """
    f = UpdateStreetPrefixSuffix()
    tokens = f.transform([Token(t) for t in inputs])
    assert ' '.join(tokens) == result_text
    assert [t.type() for t in tokens] == result_types


def test_standardize_init_error():
    """Test error case when intializing the street name standardizer with an
    invalid characters argument.
    """
    with pytest.raises(ValueError):
        StandardizeUSStreetName(characters='unknown')


@pytest.mark.parametrize(
    'characters,result',
    [
        (None, 'East 25 St'),
        ('capitalize', 'East 25 St'),
        ('lower', 'east 25 st'),
        ('upper', 'EAST 25 ST'),
        (CapitalizeTokens(), 'East 25 St'),
        (LowerTokens(), 'east 25 st'),
        (UpperTokens(), 'EAST 25 ST')
    ]
)
def test_standardize_street_name(characters, result):
    """Test the specialized U.S. street name standardizer."""
    f = StandardizeUSStreetName(characters=characters)
    assert f.eval('e 25TH str') == result
