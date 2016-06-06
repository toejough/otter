"""Watch the given outputs for their data."""


class Recorder:
    """Record output data."""

    def __init__(self):
        """init state."""
        self.last_from_stream = False
        self._output_record = ''
        self._max_output = 0

    def record(self, data, from_stream=False):
        """Record outputted data."""
        self._output_record += data
        self._max_output = max(self._max_output, len(data))
        self._output_record = self._output_record[-self._max_output:]
        # it doesn't matter if the source was a stream or not if there was no real data.
        if data:
            self.last_from_stream = from_stream

    def record_reset(self):
        """Record a reset, explicitly."""
        self._output_record += '\n'

    def last_output_matches(self, given_output):
        """Return True if the last output matches the given output."""
        return given_output and self._output_record.endswith(given_output)

    def is_reset(self):
        """return whether the output record indicates a reset was done last."""
        return self._output_record and self._output_record.endswith('\n')
