import hashlib


class File:
    def __init__(self, path: str, contents: bytes, mode: bytes):
        self.path = path
        self.contents = contents
        self.mode = mode

    @property
    def hexsha(self):
        return hashlib.sha256(self.contents).hexdigest()

    def __eq__(self, other):
        return self.path == other.path and self.contents == other.contents
