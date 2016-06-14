"""Watch the given outputs for their data."""


# Classes
class Recorder:
    """Record output data."""

    def __new__(cls):
        """Return a new instance of the class."""
        singleton = super().__new__(cls)

        def return_singleton(cls):
            """Return the singleton."""
            cls.__init__(singleton)
            return singleton

        cls.__new__ = return_singleton

        return cls.__new__(cls)

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

    def last_output_matches(self, given_output):
        """Return True if the last output matches the given output."""
        return given_output and self._output_record.endswith(given_output)

    def is_reset(self):
        """return whether the output record indicates a reset was done last."""
        return self._output_record and self._output_record.endswith('\n')
