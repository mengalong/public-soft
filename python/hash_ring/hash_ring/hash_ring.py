#!/usr/bin/env python
import bisect
import hashlib
import six
import struct

class HashRing(object):

    def __init__(self, nodes, replicas=100):
        self._ring = dict()
        self._sorted_keys = []

        for node in nodes:
            for r in six.moves.range(replicas):
                hashed_key = self._hash('%s-%s' % (node, r))
                self._ring[hashed_key] = node
                self._sorted_keys.append(hashed_key)
        self._sorted_keys.sort()

    @staticmethod
    def _hash(key):
        return struct.unpack_from('>I',
                                  hashlib.md5(str(key).encode()).digest())[0]

    def _get_position_on_ring(self, key):
        hashed_key = self._hash(key)
        position = bisect.bisect(self._sorted_keys, hashed_key)
        return position if position < len(self._sorted_keys) else 0

    def get_node(self, key):
        if not self._ring:
            return None
        pos = self._get_position_on_ring(key)
        return self._ring[self._sorted_keys[pos]]

if __name__ == "__main__":
    members = ["along", "xiaoming"]
    hr = HashRing(members)
    for i in xrange(1, 10):

        name = hr.get_node(str(i))
        print "%s:%s" % (i, name)
