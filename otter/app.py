"""app-layer code."""


# [ Imports ]
# [ -Python ]
import sys
# [ -Project ]
from . import use_cases


# [ Application ]
class Namespace:
    """a modifiable object."""

    pass


class LineTracker:
    """A line tracker."""

    def __init__(self):
        """Init the state."""
        self.last_line = ''

    def update(self, text):
        """Record the last line from the given text."""
        self.last_line = text.rsplit('\n', 1)[-1]

DEFAULT_LINE_TRACKER = LineTracker()
DEFAULT_SOURCE_TRACKER = Namespace()
DEFAULT_SOURCE_TRACKER.stream_wrote_last = False


class Stream:
    """A data stream."""

    def __init__(
        self,
        writer=sys.stdout.write,
        start_new_stream_at_new_line=use_cases.start_new_stream_at_new_line,
        start_new_stream_mid_line=use_cases.start_new_stream_mid_line,
        continue_stream_from_prior_data=use_cases.continue_stream_from_prior_data,
        continue_stream_from_new_line=use_cases.continue_stream_from_new_line,
        continue_stream_from_mid_line=use_cases.continue_stream_from_mid_line,
        line_tracker=DEFAULT_LINE_TRACKER,
        source_tracker=DEFAULT_SOURCE_TRACKER
    ):
        """Init the state."""
        while hasattr(writer, 'writer'):
            writer = writer.writer
        self._writer = writer
        self._prior_data = ''
        self._line_tracker = line_tracker
        self._source_tracker = source_tracker
        self.start_new_stream_at_new_line = start_new_stream_at_new_line
        self.start_new_stream_mid_line = start_new_stream_mid_line
        self.continue_stream_from_prior_data = continue_stream_from_prior_data
        self.continue_stream_from_new_line = continue_stream_from_new_line
        self.continue_stream_from_mid_line = continue_stream_from_mid_line

    def write(self, data):
        """write the given data via a use case."""
        if not data:
            pass
        elif not self._prior_data:
            if self._line_tracker.last_line == '':
                self.start_new_stream_at_new_line(self._tracked_write, data)
            else:
                self.start_new_stream_mid_line(self._tracked_write, data)
        else:
            if self._line_tracker.last_line == self._prior_data:
                self.continue_stream_from_prior_data(self._tracked_write, data)
            elif self._line_tracker.last_line == '':
                self.continue_stream_from_new_line(self._tracked_write, data, self._prior_data)
            else:
                self.continue_stream_from_mid_line(self._tracked_write, data, self._prior_data)

    def _tracked_write(self, data):
        """Write the given data."""
        self._writer(data)
        self._prior_data += data
        self._line_tracker.update(data)
        self._source_tracker.stream_wrote_last = True


class Wrapped:
    """A wrapped non-stream writer."""

    def __init__(
        self,
        writer,
        write_non_stream_at_new_line=use_cases.write_non_stream_at_new_line,
        write_non_stream_mid_line=use_cases.write_non_stream_mid_line,
        write_non_stream_mid_stream=use_cases.write_non_stream_mid_stream,
        line_tracker=DEFAULT_LINE_TRACKER,
        source_tracker=DEFAULT_SOURCE_TRACKER
    ):
        """init the state."""
        while isinstance(writer, type(self)):
            writer = writer.writer
        self.writer = writer
        self.write_non_stream_at_new_line = write_non_stream_at_new_line
        self.write_non_stream_mid_line = write_non_stream_mid_line
        self.write_non_stream_mid_stream = write_non_stream_mid_stream
        self.line_tracker = line_tracker
        self.source_tracker = source_tracker

    def __call__(self, data):
        """call the wrapped item."""
        if not data:
            pass
        elif self.line_tracker.last_line == '':
            self.write_non_stream_at_new_line(self._tracked_write, data)
        elif self.source_tracker.stream_wrote_last:
            self.write_non_stream_mid_stream(self._tracked_write, data)
        else:
            self.write_non_stream_mid_line(self._tracked_write, data)

    def _tracked_write(self, data):
        """a tracked write."""
        self.writer(data)
        self.line_tracker.update(data)
        self.source_tracker.stream_wrote_last = False
