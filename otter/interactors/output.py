"""Shared output base."""


# [ Import ]
# [ -Python ]
# [ -Project ]
from . import mem_recorder


# [ Public ]
class Output:
    """Output class."""

    def __init__(self, writer):
        """init the state."""
        self._write = writer.write
        self._flush = writer.flush
        self._recorder = mem_recorder.get_recorder()

    def write(self, data, *, from_stream=False):
        """write the data to stdout."""
        output = self._write(data)
        self._flush()
        self._recorder.record(data, from_stream=from_stream)
        return output

    def reset(self):
        """reset the output."""
        if not self._recorder.is_reset():
            self.write('\n')

    def combine(self, prior_data, new_data):
        """combine two hunks of data."""
        return prior_data + new_data

    def last_output_matches(self, given_output):
        """last output matches."""
        return self._recorder.last_output_matches(given_output)

    def last_from_stream(self):
        """Return whether the last output was from a stream."""
        return self._recorder.last_from_stream
