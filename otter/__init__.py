"""
Otter: restream your data.

Outputs a stream of data.
Watches the output.
Restreams the data if more is posted after an interruption has occurred.

Defaults to watching stdout and stderr, and printing to stdout.
"""


# [ Imports ]
# [ -Python ]
import sys
from unittest import TestCase
# [ -Project ]
from .app import Stream, Wrapped


# [ Pyflakes avoidance ]
assert Stream
assert Wrapped
