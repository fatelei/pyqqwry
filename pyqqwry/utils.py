# -*- coding: utf8 -*-
"""
    pyqqwry.utils
    ~~~~~~~~~~~~~

    Utils modules.
"""


def decode(hex_str):
    """Decode hex str from cz.net to unicode.

    :param str hex_str: Str in hex format
    :return: Unicode string.
    """
    try:
        return unicode(hex_str, "gbk").encode("utf8")
    except:
        return ""
