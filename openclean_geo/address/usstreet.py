# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

from typing import List, Optional, Union

from openclean.function.token.base import Token, Tokens, TokenTransformer, CapitalizeTokens, LowerTokens, UpperTokens
from openclean.function.token.convert import TokenListConverter, TokenMapper
from openclean.function.token.filter import RepeatedTokenFilter, TokenFilter, TokenTypeFilter
from openclean.function.token.split import ChartypeSplit, DEFAULT_CLASSIFIER
from openclean.function.value.text import AlphaNumeric

import openclean.function.token.base as TT


# -- Token filter -------------------------------------------------------------

class StreetNumberSuffixFilter(TokenTransformer):
    """The street number suffix filter is used to remove tokens from street
    numbers like '1ST', '2ND', '3RD', '4TH', etc..

    This implementation assumes that the tokens have been generated using the
    :class:`openclean.function.token.split.ChartypeSplit` tokenizer that will
    create separate tokens for number and suffix, e.g., '1', 'ST'. The filter
    removes a 'ST' token if it follows a token that ends with '1', a 'ND' token
    if it follows a token that ends with '2', a 'RD' token if it follows a
    token that ends with '3', and a 'TH' token if it follows a token that ends
    with a digit.
    """
    def transform(self, tokens: List[Token]) -> List[Token]:
        """Transform a list of string tokens.

        Removes all street number suffix tokens 'ST', 'ND', 'RD, and 'TH' if
        they follow a token that ends with a digit ('1' for 'ST', '2' for 'ND',
        '3' for 'RD', and any digit for 'TH').

        Patameters
        ----------
        tokens: list of openclean.function.token.base.Token
            List of string tokens.

        Returns
        -------
        list of openclean.function.token.base.Token
        """
        # Return immediately if the list of tokens is empty.
        if not tokens:
            return tokens
        # Remove street suffixes from token list.
        result = [tokens[0]]
        for i in range(1, len(tokens)):
            t = tokens[i].upper()
            if t == 'ST' and tokens[i - 1][-1] == '1':
                continue
            if t == 'ND' and tokens[i - 1][-1] == '2':
                continue
            if t == 'RD' and tokens[i - 1][-1] == '3':
                continue
            if t == 'TH' and tokens[i - 1][-1] in '0123456789':
                continue
            result.append(tokens[i])
        return result


# -- Token converter ----------------------------------------------------------

"""Create maping of street numbers from their textual form to their numeric
value. The mapping currently only contains mappings for number 1-12.
"""

STREET_NR_MAPPING = {
    'FIRST': '1',
    'SECOND': '2',
    'THIRD': '3',
    'FOURTH': '4',
    'FIFTH': '5',
    'SIXTH': '6',
    'SEVENTH': '7',
    'EIGHTH': '8',
    'NINTH': '9',
    'TENTH': '10',
    'ELEVENTH': '11',
    'TWELFTH': '6',
}

"""Create mapping of common street type abbreviations to a standardized value.
This is primarily intended for US street names. Generated from:
https://github.com/VIDA-NYU/openclean-pattern/blob/master/resources/data/street_abvs.csv
"""

STREET_TYPE = 'STREET_TYPE'

STREET_TYPE_MAPPING = {
    'ALLEE': 'ALY',
    'ALLEY': 'ALY',
    'ALLY': 'ALY',
    'ANEX': 'ANX',
    'ANNEX': 'ANX',
    'ANNX': 'ANX',
    'ARCADE': 'ARC',
    'AV': 'AVE',
    'AVEN': 'AVE',
    'AVENU': 'AVE',
    'AVENUE': 'AVE',
    'AVN': 'AVE',
    'AVNUE': 'AVE',
    'BAYOO': 'BYU',
    'BAYOU': 'BYU',
    'BEACH': 'BCH',
    'BEND': 'BND',
    'BLUF': 'BLF',
    'BLUFF': 'BLF',
    'BLUFFS': 'BLFS',
    'BOT': 'BTM',
    'BOTTM': 'BTM',
    'BOTTOM': 'BTM',
    'BOUL': 'BLVD',
    'BOULEVARD': 'BLVD',
    'BOULV': 'BLVD',
    'BRNCH': 'BR',
    'BRANCH': 'BR',
    'BRDGE': 'BRG',
    'BRIDGE': 'BRG',
    'BROOK': 'BRK',
    'BROOKS': 'BRKS',
    'BURG': 'BG',
    'BURGS': 'BGS',
    'BYPA': 'BYP',
    'BYPAS': 'BYP',
    'BYPASS': 'BYP',
    'BYPS': 'BYP',
    'CAMP': 'CP',
    'CMP': 'CP',
    'CANYN': 'CYN',
    'CANYON': 'CYN',
    'CNYN': 'CYN',
    'CAPE': 'CPE',
    'CAUSEWAY': 'CSWY',
    'CAUSWA': 'CSWY',
    'CEN': 'CTR',
    'CENT': 'CTR',
    'CENTER': 'CTR',
    'CENTR': 'CTR',
    'CENTRE': 'CTR',
    'CNTER': 'CTR',
    'CNTR': 'CTR',
    'CENTERS': 'CTRS',
    'CIRC': 'CIR',
    'CIRCL': 'CIR',
    'CIRCLE': 'CIR',
    'CRCL': 'CIR',
    'CRCLE': 'CIR',
    'CIRCLES': 'CIRS',
    'CLIFF': 'CLF',
    'CLIFFS': 'CLFS',
    'CLUB': 'CLB',
    'COMMON': 'CMN',
    'COMMONS': 'CMNS',
    'CORNER': 'COR',
    'CORNERS': 'CORS',
    'COURSE': 'CRSE',
    'COURT': 'CT',
    'COURTS': 'CTS',
    'COVE': 'CV',
    'COVES': 'CVS',
    'CREEK': 'CRK',
    'CRESCENT': 'CRES',
    'CRSENT': 'CRES',
    'CRSNT': 'CRES',
    'CREST': 'CRST',
    'CROSSING': 'XING',
    'CRSSNG': 'XING',
    'CROSSROAD': 'XRD',
    'CROSSROADS': 'XRDS',
    'CURVE': 'CURV',
    'DALE': 'DL',
    'DAM': 'DM',
    'DIV': 'DV',
    'DIVIDE': 'DV',
    'DVD': 'DV',
    'DRIV': 'DR',
    'DRIVE': 'DR',
    'DRV': 'DR',
    'DRIVES': 'DRS',
    'ESTATE': 'EST',
    'ESTATES': 'ESTS',
    'EXP': 'EXPY',
    'EXPR': 'EXPY',
    'EXPRESS': 'EXPY',
    'EXPRESSWAY': 'EXPY',
    'EXPW': 'EXPY',
    'EXTENSION': 'EXT',
    'EXTN': 'EXT',
    'EXTNSN': 'EXT',
    'FALLS': 'FLS',
    'FERRY': 'FRY',
    'FRRY': 'FRY',
    'FIELD': 'FLD',
    'FIELDS': 'FLDS',
    'FLAT': 'FLT',
    'FLATS': 'FLTS',
    'FORD': 'FRD',
    'FORDS': 'FRDS',
    'FOREST': 'FRST',
    'FORESTS': 'FRST',
    'FORG': 'FRG',
    'FORGE': 'FRG',
    'FORGES': 'FRGS',
    'FORK': 'FRK',
    'FORKS': 'FRKS',
    'FORT': 'FT',
    'FRT': 'FT',
    'FREEWAY': 'FWY',
    'FREEWY': 'FWY',
    'FRWAY': 'FWY',
    'FRWY': 'FWY',
    'GARDEN': 'GDN',
    'GARDN': 'GDN',
    'GRDEN': 'GDN',
    'GRDN': 'GDN',
    'GARDENS': 'GDNS',
    'GRDNS': 'GDNS',
    'GATEWAY': 'GTWY',
    'GATEWY': 'GTWY',
    'GATWAY': 'GTWY',
    'GTWAY': 'GTWY',
    'GLEN': 'GLN',
    'GLENS': 'GLNS',
    'GREEN': 'GRN',
    'GREENS': 'GRNS',
    'GROV': 'GRV',
    'GROVE': 'GRV',
    'GROVES': 'GRVS',
    'HARB': 'HBR',
    'HARBOR': 'HBR',
    'HARBR': 'HBR',
    'HRBOR': 'HBR',
    'HARBORS': 'HBRS',
    'HAVEN': 'HVN',
    'HT': 'HTS',
    'HIGHWAY': 'HWY',
    'HIGHWY': 'HWY',
    'HIWAY': 'HWY',
    'HIWY': 'HWY',
    'HWAY': 'HWY',
    'HILL': 'HL',
    'HILLS': 'HLS',
    'HLLW': 'HOLW',
    'HOLLOW': 'HOLW',
    'HOLLOWS': 'HOLW',
    'HOLWS': 'HOLW',
    'ISLAND': 'IS',
    'ISLND': 'IS',
    'ISLANDS': 'ISS',
    'ISLNDS': 'ISS',
    'ISLES': 'ISLE',
    'JCTION': 'JCT',
    'JCTN': 'JCT',
    'JUNCTION': 'JCT',
    'JUNCTN': 'JCT',
    'JUNCTON': 'JCT',
    'JCTNS': 'JCTS',
    'JUNCTIONS': 'JCTS',
    'KEY': 'KY',
    'KEYS': 'KYS',
    'KNOL': 'KNL',
    'KNOLL': 'KNL',
    'KNOLLS': 'KNLS',
    'LAKE': 'LK',
    'LAKES': 'LKS',
    'LANDING': 'LNDG',
    'LNDNG': 'LNDG',
    'LANE': 'LN',
    'LIGHT': 'LGT',
    'LIGHTS': 'LGTS',
    'LOAF': 'LF',
    'LOCK': 'LCK',
    'LOCKS': 'LCKS',
    'LDGE': 'LDG',
    'LODG': 'LDG',
    'LODGE': 'LDG',
    'LOOPS': 'LOOP',
    'MANOR': 'MNR',
    'MANORS': 'MNRS',
    'MEADOW': 'MDW',
    'MDW': 'MDWS',
    'MEADOWS': 'MDWS',
    'MEDOWS': 'MDWS',
    'MILL': 'ML',
    'MILLS': 'MLS',
    'MISSN': 'MSN',
    'MSSN': 'MSN',
    'MOTORWAY': 'MTWY',
    'MNT': 'MT',
    'MOUNT': 'MT',
    'MNTAIN': 'MTN',
    'MNTN': 'MTN',
    'MOUNTAIN': 'MTN',
    'MOUNTIN': 'MTN',
    'MTIN': 'MTN',
    'MNTNS': 'MTNS',
    'MOUNTAINS': 'MTNS',
    'NECK': 'NCK',
    'ORCHARD': 'ORCH',
    'ORCHRD': 'ORCH',
    'OVL': 'OVAL',
    'OVERPASS': 'OPAS',
    'PRK': 'PARK',
    'PARKS': 'PARK',
    'PARKWAY': 'PKWY',
    'PARKWY': 'PKWY',
    'PKWAY': 'PKWY',
    'PKY': 'PKWY',
    'PARKWAYS': 'PKWY',
    'PKWYS': 'PKWY',
    'PASSAGE': 'PSGE',
    'PATHS': 'PATH',
    'PIKES': 'PIKE',
    'PINE': 'PNE',
    'PINES': 'PNES',
    'PLAIN': 'PLN',
    'PLAINS': 'PLNS',
    'PLAZA': 'PLZ',
    'PLZA': 'PLZ',
    'POINT': 'PT',
    'POINTS': 'PTS',
    'PORT': 'PRT',
    'PORTS': 'PRTS',
    'PRAIRIE': 'PR',
    'PRR': 'PR',
    'RAD': 'RADL',
    'RADIAL': 'RADL',
    'RADIEL': 'RADL',
    'RANCH': 'RNCH',
    'RANCHES': 'RNCH',
    'RNCHS': 'RNCH',
    'RAPID': 'RPD',
    'RAPIDS': 'RPDS',
    'REST': 'RST',
    'RDGE': 'RDG',
    'RIDGE': 'RDG',
    'RIDGES': 'RDGS',
    'RIVER': 'RIV',
    'RVR': 'RIV',
    'RIVR': 'RIV',
    'ROAD': 'RD',
    'ROADS': 'RDS',
    'ROUTE': 'RTE',
    'SHOAL': 'SHL',
    'SHOALS': 'SHLS',
    'SHOAR': 'SHR',
    'SHORE': 'SHR',
    'SHOARS': 'SHRS',
    'SHORES': 'SHRS',
    'SKYWAY': 'SKWY',
    'SPNG': 'SPG',
    'SPRING': 'SPG',
    'SPRNG': 'SPG',
    'SPNGS': 'SPGS',
    'SPRINGS': 'SPGS',
    'SPRNGS': 'SPGS',
    'SPURS': 'SPUR',
    'SQR': 'SQ',
    'SQRE': 'SQ',
    'SQU': 'SQ',
    'SQUARE': 'SQ',
    'SQRS': 'SQS',
    'SQUARES': 'SQS',
    'STATION': 'STA',
    'STATN': 'STA',
    'STN': 'STA',
    'STRAV': 'STRA',
    'STRAVEN': 'STRA',
    'STRAVENUE': 'STRA',
    'STRAVN': 'STRA',
    'STRVN': 'STRA',
    'STRVNUE': 'STRA',
    'STREAM': 'STRM',
    'STREME': 'STRM',
    'STREET': 'ST',
    'STRT': 'ST',
    'STR': 'ST',
    'STREETS': 'STS',
    'SUMIT': 'SMT',
    'SUMITT': 'SMT',
    'SUMMIT': 'SMT',
    'TERR': 'TER',
    'TERRACE': 'TER',
    'THROUGHWAY': 'TRWY',
    'TRACE': 'TRCE',
    'TRACES': 'TRCE',
    'TRACK': 'TRAK',
    'TRACKS': 'TRAK',
    'TRK': 'TRAK',
    'TRKS': 'TRAK',
    'TRAFFICWAY': 'TRFY',
    'TRAIL': 'TRL',
    'TRAILS': 'TRL',
    'TRLS': 'TRL',
    'TRAILER': 'TRLR',
    'TRLRS': 'TRLR',
    'TUNEL': 'TUNL',
    'TUNLS': 'TUNL',
    'TUNNEL': 'TUNL',
    'TUNNELS': 'TUNL',
    'TUNNL': 'TUNL',
    'TRNPK': 'TPKE',
    'TURNPIKE': 'TPKE',
    'TURNPK': 'TPKE',
    'UNDERPASS': 'UPAS',
    'UNION': 'UN',
    'UNIONS': 'UNS',
    'VALLEY': 'VLY',
    'VALLY': 'VLY',
    'VLLY': 'VLY',
    'VALLEYS': 'VLYS',
    'VDCT': 'VIA',
    'VIADCT': 'VIA',
    'VIADUCT': 'VIA',
    'VIEW': 'VW',
    'VIEWS': 'VWS',
    'VILL': 'VLG',
    'VILLAG': 'VLG',
    'VILLAGE': 'VLG',
    'VILLG': 'VLG',
    'VILLIAGE': 'VLG',
    'VILLAGES': 'VLGS',
    'VILLE': 'VL',
    'VIST': 'VIS',
    'VISTA': 'VIS',
    'VST': 'VIS',
    'VSTA': 'VIS',
    'WALKS': 'WALK',
    'WY': 'WAY',
    'WELL': 'WL',
    'WELLS': 'WLS'
}


"""Create mapping for abbreviations of cardinal directions."""

DIRECTION = 'DIRECTION'

DIRECTION_MAPPING = {
    'E': 'EAST',
    'W': 'WEST',
    'N': 'NORTH',
    'S': 'SOUTH'
}


class UpdateStreetPrefixSuffix(TokenTransformer):
    """Token transformer that updates the first and last token of a list of
    tokens that are expected to represent a U.S. street address.

    The first token is standardized if (a) it is an abbreviation for an avenue
    (e.g., in values like Ave of the Americas), or (b) if it is the abbreviation
    for a cardinal directions, i.e., 'N', 'E', 'S', or 'W'.

    The last token is standardized if it is a common abbreviation for a street
    type.
    """
    def __init__(self):
        """Initialize the transformers for token list prefix and suffix."""
        self.prefix = TokenListConverter(
            converters=[
                TokenMapper(label=TT.ALPHA, lookup={
                    'AV': 'AVENUE',
                    'AVE': 'AVENUE',
                    'AVEN': 'AVENUE',
                    'AVENU': 'AVENUE',
                    'AVN': 'AVENUE',
                    'AVNUE': 'AVENUE'
                }),
                TokenMapper(label=DIRECTION, lookup=DIRECTION_MAPPING)
            ]
        )
        self.suffix = TokenMapper(label=STREET_TYPE, lookup=STREET_TYPE_MAPPING)

    def transform(self, tokens: List[Token]) -> List[Token]:
        """Transform the first and last token in the given list.

        Patameters
        ----------
        tokens: list of openclean.function.token.base.Token
            List of string tokens.

        Returns
        -------
        list of openclean.function.token.base.Token
        """
        if not tokens or len(tokens) < 2:
            return tokens
        return self.prefix.transform([tokens[0]]) + tokens[1:-1] + self.suffix.transform([tokens[-1]])


class USStreetNameKey(Tokens):
    """Key generator for US street names. Keys are generated based on tokenization
    of input values. Tokens are generated using the character type splitter that
    generates tokens of homogeneous character type distinguishing between letters,
    digits and other. For example, a value of 'W35ST' is split into three tokens
    'W', '35', 'ST'.

    The key generator removes all tokens that contain non- alphenumeric
    characters. The remaining tokens are converted to upper case and normalized
    using the following rules:

    (1) abbreviations for 'AVENUE' that occur in the first token are
        standardized,
    (2) abbreviations for cardinal directions 'N', 'E', 'S', 'W' that occur in
        the first token are standardized, and
    (3) abbreviations for street types such as 'Ave', 'Str', 'Ln' that occur
        in the last token.

    Note that duplicate tokens are not removed by this key generator. The reason
    is that some abbreviations for street types (e.g., ST) can have multiple
    semantics, e.g., 'ST. MARKS ST'. Removing duplicates would make the previous
    example similar to 'MARKS STREET'.

    Tokens are sorted in alphabetic order.
    """
    def __init__(self):
        """Initialize the tokenizer and token transformer in the super class."""
        super(USStreetNameKey, self).__init__(
            tokenizer=ChartypeSplit(),
            transformer=[
                TokenFilter(AlphaNumeric()),
                UpperTokens(),
                StreetNumberSuffixFilter(),
                TokenMapper(label=TT.DIGIT, lookup=STREET_NR_MAPPING),
                UpdateStreetPrefixSuffix()
            ],
            delim=' ',
            sort=True,
            unique=False
        )


class USStreetNameTokenizer(Tokens):
    """Tokenizer for US street names. Tokens are generated using the character
    type splitter that generates tokens of homogeneous character type,
    distinguishing between letters, digits and other. For example, a value of
    'W35ST' is split into three tokens ['W', '35', 'ST'].

    The tokenizer removes all tokens that contain whitespace characters and the
    remaining tokens to all upper case. Tokens are then

    (1) filtered to remove street number suffixes resulting from values like
        '1st, '2nd, '3rd', etc..,
    (2) normalized by replacing text representations of street numbers
        like 'first', 'second', 'third' with the respective numbers,
    (3) abbreviations for 'AVENUE' that occur in the first token are
        standardized,
    (4) abbreviations for cardinal directions 'N', 'E', 'S', 'W' that occur in
        the first token are standardized, and
    (5) abbreviations for street types such as 'Ave', 'Str', 'Ln' that occur
        in the last token.
    """
    def __init__(
        self, unique: Optional[bool] = False, alphanum: Optional[bool] = False,
        repeated: Optional[bool] = True
    ):
        """Initialize the tokenizer and token transformer in the super class.

        If the unique flag is set dplicate tokens will be removed. Note that
        this may cause confusion for addresses like ST JOHNS STR.

        Parameters
        ----------
        unique: bool, default=False
            Remove duplicate tokens before generating the collision key if this
            flag is set to True.
        alphanum: bool, default=False
            Keep only alpha-numeric tokens if True.
        repeated: bool, default=True
            Allow consecutive identical tokens if True. If False, repeated
            tokens are removed.
        """
        # Define the default transformer.
        transformer = [
            TokenFilter(AlphaNumeric()) if alphanum else TokenTypeFilter(types={TT.SPACE}, negated=True),
            UpperTokens(),
            StreetNumberSuffixFilter(),
            TokenMapper(label=TT.DIGIT, lookup=STREET_NR_MAPPING),
            UpdateStreetPrefixSuffix()
        ]
        # Add repeated token filter if the flag is True.
        if not repeated:
            transformer.append(RepeatedTokenFilter())
        super(USStreetNameTokenizer, self).__init__(
            tokenizer=ChartypeSplit(
                chartypes=DEFAULT_CLASSIFIER + [(str.isspace, TT.SPACE)]
            ),
            transformer=transformer,
            delim='',
            sort=False,
            unique=unique
        )


class StandardizeUSStreetName(Tokens):
    """Value function to standardize U.S. street names. Uses the specialized
    tokenizer to create standardized tokens. Then applies a string transformation
    to the tokens, e.g., to convert them to all lower case.
    """
    def __init__(
        self, characters: Optional[Union[str, TokenTransformer]] = None,
        alphanum: Optional[bool] = False, repeated: Optional[bool] = True
    ):
        """Initialize the transformer that is applied to the generated tokens
        before concatenating them.

        Parameters
        ----------
        characters: string or openclean.function.token.base.TokenTransformer, default=None
            Specify transformer that is applied to generated tokens. The transformer
            can either be specified using one of the following values: 'capitalize',
            'lower', 'upper', or be given as a token transformer instance. By
            default, all tokens are capitalized.
        alphanum: bool, default=False
            Keep only alpha-numeric tokens if True.
        repeated: bool, default=True
            Allow consecutive identical tokens if True. If False, repeated
            tokens are removed.
        """
        if characters is None:
            transformer = [CapitalizeTokens()]
        else:
            if isinstance(characters, str):
                if characters == 'capitalize':
                    transformer = [CapitalizeTokens()]
                elif characters == 'lower':
                    transformer = [LowerTokens()]
                elif characters == 'upper':
                    transformer = None
                else:
                    raise ValueError("unknown string transformer '{}'".format(characters))
            else:
                transformer = [characters]
        super(StandardizeUSStreetName, self).__init__(
            tokenizer=USStreetNameTokenizer(alphanum=alphanum, repeated=repeated),
            transformer=transformer,
            delim=' ',
            sort=False,
            unique=False
        )
