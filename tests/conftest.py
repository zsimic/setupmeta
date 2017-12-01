import io
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import os
import sys

import setupmeta


TESTS = os.path.dirname(__file__)
PROJECT = os.path.dirname(TESTS)


def resouce(*relative_path):
    """ Full path for 'relative_path' """
    return os.path.join(TESTS, *relative_path)


def file_contents(*relative_path):
    full_path = resouce(*relative_path)
    with io.open(full_path, encoding='utf-8') as fh:
        return ''.join(fh.readlines()).strip()


class capture_output:
    """
    Context manager allowing to temporarily grab stdout/stderr output.
    Output is captured and made available only for the duration of the context.

    Sample usage:

    with capture_output() as logged:
        ... do something that generates output ...
        assert "some message" in logged
    """
    def __init__(self, stdout=True, stderr=True):
        self.old_out = sys.stdout
        self.old_err = sys.stderr
        sys.stdout = self.out_buffer = StringIO() if stdout else None
        sys.stderr = self.err_buffer = StringIO() if stderr else None

    def __repr__(self):
        return self.to_string()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        sys.stdout = self.old_out
        sys.stderr = self.old_err
        self.out_buffer = None
        self.err_buffer = None

    def __contains__(self, item):
        return item is not None and item in self.to_string()

    def __add__(self, other):
        return "%s %s" % (self, other)

    def to_string(self):
        result = ''
        if self.out_buffer:
            result += setupmeta.to_str(self.out_buffer.getvalue())
        if self.err_buffer:
            result += setupmeta.to_str(self.err_buffer.getvalue())
        return result