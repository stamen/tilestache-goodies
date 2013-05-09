# TileStache Goodies

## SparseCache

`SparseCache` is identical to TileStache's Disk cache except that it returns
404s for "empty" tiles (with a file size matching the `empty_size` kwarg).

This may improve performance under some circumstances, as it eliminates the
need to transfer additional, duplicate empty files (although it doesn't
eliminate the requests for them, nor does it prevent them from being saved to
the cache).

### kwargs

* `empty_size` - size of an empty file (in bytes). 334 bytes (the default
  value) is the size of an empty, transparent, 24-bit PNG (the default output).

### Example Configuration

```json
{
  "cache":
  {
    "class": "SparseCache",
    "kwargs": {
      "path": "/tmp/stache",
      "umask": "0000",
      "empty_size": 334
    }
  },
}
```

## LanternCache

`LanternCache` exposes an additional `X-Land-Or-Sea` header corresponding to
the content of a given tile (determined by its `md5sum`).

The value will be `1` if by land, `2` if by sea, `0` if by both or
indeterminate (i.e. the `second` tile is not yet present in the cache).

This can be used to conditionally load related tiles (tiles at the next zoom or
additional data tiles), reducing the number of requests a client needs to make
to display a consistent view.

### kwargs

* `land` - `md5sum` of a tile that is entirely "land".
* `sea` - `md5sum` of a tile that is entirely "sea".
* `second` - Name of an alternate layer that should be used to compare
  `md5sums` with the primary layer. Its cache configuration should roughly
  match the LanternCached layer.

### Example Configuration

```json
{
  "cache":
  {
    "class": "LanternCache",
    "kwargs": {
      "path": "/tmp/stache",
      "umask": "0000",
      "land": "cd37744a985b79ed29bb6269e45da27f",
      "sea": "35f515ac80cd2fb679de95699044ee7b",
      "second": "layer2"
    }
  },
}
```

## License

Released under the BSD license.
