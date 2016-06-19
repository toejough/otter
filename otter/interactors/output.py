"""Shared output base."""


# [ Import ]
# [ -Python ]
import sys


# [ Public ]
class OutputDevice:
    """The output device."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush
    _write_err = sys.stderr.write
    _flush_err = sys.stderr.flush

    def __new__(cls, *args, **kwargs):
        """Return singleton."""
        singleton = super().__new__(cls, *args, **kwargs)
        cls.__init__(singleton, *args, **kwargs)

        def return_singleton(cls, *args, **kwargs):
            """return singleton."""
            return singleton

        cls.__new__ = return_singleton

        return singleton

    # Data
    def __init__(self, initial_data=''):
        """Init the state."""
        self._is_reset = False
        self._last_output = initial_data
        self._last_from_stream = False
        self._stds_replaced = False

    def _set_reset(self, is_reset):
        """Write data to the device via the given output mechanism."""
        self._is_reset = is_reset

    def _get_new_stream_data(self, stream_data):
        """actually write and record the data."""
        return stream_data[len(self._last_output):]

    def _update_stream_output(self, stream_data):
        """actually write and record the data."""
        self._last_output = stream_data
        self._last_from_stream = True

    # Logic
    def _is_not_reset(self):
        """Reset the device."""
        return not self._is_reset

    def _stds_have_not_been_replaced(self):
        """Write data to the device via the given output mechanism."""
        return not self._stds_replaced

    def _last_output_matches(self, stream_data):
        """actually write and record the data."""
        return self._last_output and self._data_startswith_last_output(stream_data)

    def _stream_needs_reset(self, stream_data, last_output_matches):
        """actually write and record the data."""
        return stream_data and not last_output_matches

    # Branching
    def reset(self):
        """Reset the device."""
        if self._is_not_reset():
            self._reset()

    def _maybe_replace_stds(self):
        """Write data to the device via the given output mechanism."""
        if self._stds_have_not_been_replaced():
            self._replace_stds()

    def _reset_stream(self, stream_data, last_output_matches):
        """actually write and record the data."""
        if self._stream_needs_reset(stream_data, last_output_matches):
            self.reset()

    def _get_stream_data_to_write(self, last_output_matches, stream_data):
        """actually write and record the data."""
        if last_output_matches:
            to_write = self._get_new_stream_data(stream_data)
        else:
            to_write = stream_data
        return to_write

    # Action
    def _reset(self):
        """Reset the device."""
        self.old_write('\n')

    def old_write(self, data):
        """Write data to the device via the given output mechanism."""
        self._write(data)
        self._flush()
        self._set_reset(self._data_ends_with_reset(data))
        self._maybe_replace_stds()

    def old_write_stderr(self, data):
        """Write data to the device via the given output mechanism."""
        self._write_err(data)
        self._flush_err()
        self._set_reset(self._data_ends_with_reset(data))
        self._maybe_replace_stds()

    def write_stream(self, stream_data):
        """actually write and record the data."""
        last_output_matches = self._last_output_matches(stream_data)
        self._reset_stream(stream_data, last_output_matches)
        self.old_write(self._get_stream_data_to_write(last_output_matches, stream_data))
        self._update_stream_output(stream_data)

    # query
    def _data_ends_with_reset(self, data):
        """Write data to the device via the given output mechanism."""
        return data.endswith('\n')

    def _data_startswith_last_output(self, data):
        """actually write and record the data."""
        return data.startswith(self._last_output)

    # unexamined
    # [ Private ]
    # [ -Interactor ]
    def _write_std_out_interruption(self, data):
        """Actually write the data."""
        if data and self._last_from_stream:
            self.reset()
        self.old_write(data)
        self._last_output = data
        self._last_from_stream = False

    def _write_std_err_interruption(self, data):
        """Actually write the data."""
        if data and self._last_from_stream:
            self.reset()
        self.old_write_stderr(data)
        self._last_output = data
        self._last_from_stream = False

    def _replace_stds(self):
        """replace the std streams."""
        self._replace(sys.stdout, 'write', self._write_std_out_interruption)
        self._replace(sys.stderr, 'write', self._write_std_err_interruption)

    def _replace(self, parent, func_name, replacement):
        """watch the output."""
        setattr(parent, func_name, replacement)
