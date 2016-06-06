"""Watch the given outputs for their data."""


class Recorder:
    """Record output data."""

    def __init__(self):
        """init state."""
        self.last_from_stream = False
        self.output_record = ''
        self._max_output = 0

    def record(self, data, from_stream=False):
        """Record outputted data."""
        self.output_record += data
        self._max_output = max(self._max_output, len(data))
        self.output_record = self.output_record[-self._max_output:]
        # it doesn't matter if the source was a stream or not if there was no real data.
        if data:
            self.last_from_stream = from_stream
