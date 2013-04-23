# TileStache Goodies

## SparseCache

Example config:

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

Example config:

```json
{
  "cache":
  {
    "class": "LanternCache",
    "kwargs": {
      "path": "/tmp/stache",
      "umask": "0000",
      "land": "cd37744a985b79ed29bb6269e45da27f",
      "sea": "35f515ac80cd2fb679de95699044ee7b"
    }
  },
}
```
