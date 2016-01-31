# -*- coding: utf8 -*-
"""
    pyqqwry.qqwry
    ~~~~~~~~~~~~~

    QQ wry.
"""

import mmap
import os
import socket
from struct import unpack

from pylru import lrudecorator
from pyqqwry.macro import Flag
from pyqqwry.utils import decode, generate


class QQWry(object):

    def __init__(self, path):
        """Initialize.

        :param str path: QQ wry dat file
        """
        if not os.path.exists(path):
            raise Exception("{} is an invalid path".format(path))

        self.path = path
        self.data = {}

        self.__open_qqwry()
        self.__get_file_header()

        # Get total index length.
        self.idx_num = (self.idx_end - self.idx_start) / 7 + 1

    def __open_qqwry(self):
        """Open qqwry.dat.
        """
        with open(self.path, "rb") as f:
            self.file_obj = mmap.mmap(
                f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)

    def __get_file_header(self):
        """Get index start point and end point.
        """
        self.file_obj.seek(0)  # Set file point position to start.
        self.idx_start = unpack("I", self.file_obj.read(4))[0]
        self.idx_end = unpack("I", self.file_obj.read(4))[0]

    def __read_ip_from_index_block(self, offset):
        """Read ip value from index block.

        :param int offset: IP offset
        :return: Python style binary.
        """
        self.file_obj.seek(offset)
        tmp = self.file_obj.read(4)
        return unpack("I", tmp)[0]

    def __read_record_area_offset(self, offset):
        """Read record area offset.

        :param int offset: Offset in index block
        :return: Record offset.
        """
        self.file_obj.seek(offset)
        tmp = self.file_obj.read(3)
        return unpack("I", tmp + "\0")[0]

    def __binary_search(self, target, head, tail):
        """Find target index.

        :param str target: Be found ip
        :param int head: Start point
        :param int tail: End point
        :return: IP index.
        """
        if tail - head <= 1:
            return head

        mid = (tail + head) / 2

        # Get mid offset in file.
        mid_offset = self.idx_start + mid * 7

        # Get ip value of current point.
        mid_offset_ip = self.__read_ip_from_index_block(mid_offset)

        if target > mid_offset_ip:
            return self.__binary_search(target, mid, tail)
        else:
            return self.__binary_search(target, head, mid)

    def __read_flag(self, offset):
        """Read flag.

        :param int offset: Flag offset
        :return: Flag.
        """
        self.file_obj.seek(offset)
        tmp = self.file_obj.read(1)
        return ord(tmp) if tmp else 0

    def __read_value(self, offset):
        """Read value.

        :param int offset: Offset
        :return: Value.
        """
        # If the offset is zero, country or region is unknown.
        if offset == 0:
            return "N/A"

        flag = self.__read_flag(offset)
        if flag == Flag.TWO:
            tmp = self.file_obj.read(3)
            offset = unpack("I", tmp + "\0")[0]
            return self.__read_value(offset)

        buf = []
        self.file_obj.seek(offset)
        while True:
            tmp = self.file_obj.read(1)
            if tmp == "\0":
                break
            buf.append(tmp)
        return "".join(buf)

    def __read_record(self, offset):
        """Read record block.

        :param int offset: Record start offset
        :return: A tuple includes country and region or None.
        """
        self.file_obj.seek(offset)

        # Get flag.
        tmp = self.file_obj.read(1)
        flag = ord(tmp)

        if flag == Flag.ONE:
            tmp = self.file_obj.read(3)
            offset = unpack("I", tmp + "\0")[0]

            country = self.__read_value(offset)
            flag = self.__read_flag(offset)

            if flag == Flag.TWO:
                region = self.__read_value(offset + 4)
            else:
                region = self.__read_value(offset + len(country) + 1)
        elif flag == Flag.TWO:
            tmp = self.file_obj.read(3)
            cn_offset = unpack("I", tmp + "\0")[0]
            country = self.__read_value(cn_offset)
            region = self.__read_value(offset + 4)
        else:
            country = self.__read_value(offset)
            region = self.__read_value(offset + len(country) + 1)

        return (country, region)

    @lrudecorator(1000)
    def query(self, ip):
        """Query country and region by ip address.

        :param str ip: IPv4 address
        :return: A tuple includes country and region or None.
        """
        ip = socket.inet_aton(ip)
        ip = unpack("!I", ip)[0]

        idx = self.__binary_search(ip, 0, self.idx_num - 1)
        idx_offset = self.idx_start + idx * 7
        record_offset = self.__read_record_area_offset(idx_offset + 4)
        rst = self.__read_record(record_offset + 4)

        if rst:
            country, province, city = generate(decode(rst[0]))
            return (country, province, city, decode(rst[1]))
        else:
            return None
