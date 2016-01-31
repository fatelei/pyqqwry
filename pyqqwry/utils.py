# -*- coding: utf8 -*-
"""
    pyqqwry.utils
    ~~~~~~~~~~~~~

    Utils modules.
"""

from pyqqwry.macro import Province


def decode(hex_str):
    """Decode hex str from cz.net to unicode.

    :param str hex_str: Str in hex format
    :return: Unicode string.
    """
    try:
        return unicode(hex_str, "gbk").encode("utf8")
    except:
        return ""


def generate(row):
    """Get china: country, province, city.

    :param str row: The result of row parsed from qqwry
    :return: A tuple.  
    """
    candicates = Province.china

    for (cn, province) in candicates:
        if province in row:
            _, city = row.split(province)
            return cn, province, city
    return row, "", ""
