""" Additional TileStache cache providers.
"""

import os
from os.path import exists

import hashlib

from wsgiref.headers import Headers

from TileStache.Core import TheTileLeftANote
from TileStache.Caches import Disk

class SparseCache(Disk):
    """ Disk cache which 404s "empty" tiles.
    """
    def __init__(self, empty_size=334, **kwargs):
        """ Initialize the SparseCache
            334 is the file size of a 256x256 transparent PNG
        """
        # TODO support multiple sizes
        self.empty_size = empty_size

        return Disk.__init__(self, **kwargs)


    def read(self, layer, coord, format):
        """ Read a cached tile.
        """
        fullpath = self._fullpath(layer, coord, format)
        
        if not exists(fullpath):
            return None

        if os.stat(fullpath).st_size == self.empty_size:
            raise TheTileLeftANote(status_code=404, emit_content_type=False)

        return Disk.read(self, layer, coord, format)


class LayerStub:
    """ A Layer-like substance with enough depth for Disk.read()
    """
    def __init__(self, name):
        self.cache_lifespan = None
        self._name = name


    def name(self):
        return self._name


class LanternCache(Disk):
    """ Disk cache which appends metadata about the content of a tile.
    """
    def __init__(self, land='', sea='', second=None, **kwargs):
        self.land_md5 = land
        self.sea_md5 = sea
        self.second = LayerStub(second)

        return Disk.__init__(self, **kwargs)


    def md5sum(self, body):
        if body:
            m = hashlib.md5()
            m.update(body)

            return m.hexdigest()


    def signal_land_or_sea(self, body, layer, coord, format):
        if body:
            md5sum = self.md5sum(body)
            second_md5sum = self.md5sum(Disk.read(self, self.second, coord, format))
            
            headers = Headers([('Access-Control-Expose-Headers', 'X-Land-Or-Sea')])
            headers.setdefault('X-Land-Or-Sea', '0')
            
            if second_md5sum is None or md5sum == second_md5sum:
                if md5sum == self.land_md5:
                    headers['X-Land-Or-Sea'] = '1'
                elif md5sum == self.sea_md5:
                    headers['X-Land-Or-Sea'] = '2'

            raise TheTileLeftANote(content=body, headers=headers)


    def read(self, layer, coord, format):
        body = Disk.read(self, layer, coord, format)

        self.signal_land_or_sea(body, layer, coord, format)

        # we should never get here
        return body


    def save(self, body, layer, coord, format):
        Disk.save(self, body, layer, coord, format)

        self.signal_land_or_sea(body, layer, coord, format)
