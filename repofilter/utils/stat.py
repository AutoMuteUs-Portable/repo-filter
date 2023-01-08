from ctypes import (
    CDLL,
    CFUNCTYPE,
    POINTER,
    Structure,
    c_int,
    c_int64,
    c_short,
    c_uint,
    c_ushort,
    c_wchar_p,
)


# Reference "sys/stat.h"
#
# struct _stat64
# {
#     _dev_t         st_dev;
#     _ino_t         st_ino;
#     unsigned short st_mode;
#     short          st_nlink;
#     short          st_uid;
#     short          st_gid;
#     _dev_t         st_rdev;
#     __int64        st_size;
#     __time64_t     st_atime;
#     __time64_t     st_mtime;
#     __time64_t     st_ctime;
# };
class _stat64(Structure):
    _fields_ = [
        ("st_dev", c_uint),
        ("st_ino", c_ushort),
        ("st_mode", c_ushort),
        ("st_nlink", c_short),
        ("st_uid", c_short),
        ("st_gid", c_short),
        ("st_rdev", c_uint),
        ("st_size", c_int64),
        ("st_atime", c_int64),
        ("st_mtime", c_int64),
        ("st_ctime", c_int64),
    ]


prototype_wstat64 = CFUNCTYPE(c_int, c_wchar_p, POINTER(_stat64))


def _wstat64(_FileName: str) -> _stat64:
    dll = CDLL("api-ms-win-crt-filesystem-l1-1-0.dll")
    _wstat64 = prototype_wstat64(("_wstat64", dll))
    _Stat = _stat64()
    result = _wstat64(_FileName, _Stat)
    if result == 0:
        return _Stat
    else:
        raise Exception(f"Got error code {result} from _wstat64")
