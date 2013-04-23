""" Additional TileStache caches.
"""

import os
from os.path import exists

import hashlib

from wsgiref.headers import Headers

from .Core import TheTileLeftANote
from .Caches import Disk

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


class LanternCache(Disk):
    """ Disk cache which appends metadata about the content of a tile.
    """
    def __init__(self, land='', sea='', **kwargs):
        self.land_md5 = land
        self.sea_md5 = sea

        return Disk.__init__(self, **kwargs)


    def signal_land_or_sea(self, body):
        if body:
            m = hashlib.md5()
            m.update(body)

            md5sum = m.hexdigest()

            if md5sum == self.land_md5:
                raise TheTileLeftANote(content=body, headers=Headers([('X-Land-Or-Sea', 1)]))
            elif md5sum == self.sea_md5:
                raise TheTileLeftANote(content=body, headers=Headers([('X-Land-Or-Sea', 2)]))
            else:
                raise TheTileLeftANote(content=body, headers=Headers([('X-Land-Or-Sea', 0)]))


    def read(self, layer, coord, format):
        body = Disk.read(self, layer, coord, format)

        self.signal_land_or_sea(body)

        # we should never get here
        return body


    def save(self, body, layer, coord, format):
        Disk.save(self, body, layer, coord, format)

        self.signal_land_or_sea(body)
