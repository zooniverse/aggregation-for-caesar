from argparse import ArgumentTypeError as err
import os

# modified from https://stackoverflow.com/a/33181083/1052418


class PathType(object):
    def __init__(self, type='file'):
        '''
        exists:
            True: a path that does exist
            False: a path that does not exist, in a valid parent directory
            None: don't care
        type: file, dir, symlink, None, or a function returning True for valid paths
            None: don't care
        dash_ok: whether to allow "-" as stdin/stdout
        '''
        assert type in ('file', 'dir', 'symlink', None) or hasattr(type, '__call__')
        self._type = type

    def __call__(self, string):
        e = os.path.exists(string)
        if not e:
            raise err("path does not exist: '%s'" % string)

        if self._type is None:
            pass
        elif self._type == 'file':
            if not os.path.isfile(string):
                raise err("path is not a file: '{0}'".format(string))
        elif self._type == 'symlink':
            if not os.path.symlink(string):
                raise err("path is not a symlink: '{0}'".format(string))
        elif self._type == 'dir':
            if not os.path.isdir(string):
                raise err("path is not a directory: '{0}'".format(string))
        elif not self._type(string):
            raise err("path not valid: '%s'" % string)

        return os.path.abspath(string)
