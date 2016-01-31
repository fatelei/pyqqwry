======================================
pyqqwry 基于纯真ip库，查询ip对应的地点
======================================

Python Parse QQWry, based `qqwry.pdf`_. You can get location by ip.

-------
API
-------

* query
  * str ip: IP address wanted to be queried.
  * return a tuple, including country, province, city, isp. 

-------
Install
-------

::

  pip install pyqqwry


-----
Usage
-----

::

    >>> from pyqqwry.qqwry import QQWry
    >>> qq_wry = QQWry(path)
    >>> rst = qq_wry.query("59.117.128.17")
    >>> print rst


.. _qqwry.pdf: https://drive.google.com/file/d/0B0EvSfZXS15seVVBRTlUOVlUb2M/view?usp=sharing
