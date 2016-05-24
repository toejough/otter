"""Watch the given outputs for their data."""


import sys


class Recorder:
    """Record output data."""

    def __init__(self):
        """init state."""
        self.last_from_stream = False
        self.output_record = None
        self._max_output = 0

    def set_singleton(self):
        """Replace the parent module with self."""
        sys.modules[__name__] = self

    def record(self, data, from_stream=False):
        """Record outputted data."""
        if not self.output_record:
            self.output_record = data
        else:
            self.output_record += data
            self._max_output = max(self._max_output, len(data))
            self.output_record = self.output_record[-self._max_output:]
        self.last_from_stream = from_stream

# FIXME pull recorder out into in-memory-indexable-data interactor

# set singleton
Recorder().set_singleton()
