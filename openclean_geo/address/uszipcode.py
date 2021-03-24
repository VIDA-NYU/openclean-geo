# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Wrapper functions for the ``uszipcode`` package that provides mappings of
U.S. Zip codes to information about the city, county, etc..
"""

from typing import Dict
from uszipcode import SearchEngine

from openclean.data.types import Value
from openclean.function.value.base import PreparedFunction


class USZipToCity(PreparedFunction):
    """Lookup function for US Zip codes. based on yje ``uszipcode`` package."""
    def __init__(self, simple_zipcode=True):
        """Initialize the search engine.

        Parameters
        ----------
        simple_search: bool, default=True
            Ff True, use the simple zipcode database. In that database rich
            demographics, real estate, employment, and education information
            is not available. If False, use the rich database that contains
            additional information.
        """
        self.search = SearchEngine(simple_zipcode=simple_zipcode)

    def eval(self, value: Value) -> str:
        """Get the city name that is associated with a given Zip code.

        Parameters
        ----------
        value: str or int
            Zip code value.

        Returns
        -------
        str
        """
        return self.search.by_zipcode(value).major_city

    def lookup(self, value: Value) -> Dict:
        """Get the full dictionary containing information associated with a
        given Zip code.

        Parameters
        ----------
        value: str or int
            Zip code value.

        Returns
        -------
        dict
        """
        return self.search.by_zipcode(value).to_dict()
