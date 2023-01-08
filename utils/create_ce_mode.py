# These codes are followed by https://github.com/git/git
# "compat/vcbuild/include/unistd.h"
# "compat/mingw.h"
# "git-compat-util.h"
# "cache.h"


S_IFMT = 0xF000
S_IFLNK = 0o120000
S_IFREG = 0o100000
S_IFDIR = 0o40000
S_IFGITLINK = 0o160000

# #define	S_ISDIR(m)	(((m) & S_IFMT) == S_IFDIR)
def S_ISDIR(m: int) -> bool:
    return (m & S_IFMT) == S_IFDIR


# #define S_ISLNK(x) (((x) & S_IFMT) == S_IFLNK)
def S_ISLNK(x: int) -> bool:
    return (x & S_IFMT) == S_IFLNK


# #define S_ISGITLINK(m) (((m)&S_IFMT) == S_IFGITLINK)
def S_ISGITLINK(m: int) -> bool:
    return (m & S_IFMT) == S_IFGITLINK


# #define S_ISSPARSEDIR(m) ((m) == S_IFDIR)
def S_ISSPARSEDIR(m: int) -> bool:
    return m == S_IFDIR


# #define ce_permissions(mode) (((mode) & 0100) ? 0755 : 0644)
def ce_permissions(mode: int) -> int:
    return 0o755 if (mode & 0o100) else 0o644


# static inline unsigned int create_ce_mode(unsigned int mode)
# {
# 	if (S_ISLNK(mode))
# 		return S_IFLNK;
# 	if (S_ISSPARSEDIR(mode))
# 		return S_IFDIR;
# 	if (S_ISDIR(mode) || S_ISGITLINK(mode))
# 		return S_IFGITLINK;
# 	return S_IFREG | ce_permissions(mode);
# }
def create_ce_mode(mode: int) -> int:
    if S_ISLNK(mode):
        return S_IFLNK
    if S_ISSPARSEDIR(mode):
        return S_IFDIR
    if S_ISDIR(mode) or S_ISGITLINK(mode):
        return S_IFGITLINK
    return S_IFREG | ce_permissions(mode)
