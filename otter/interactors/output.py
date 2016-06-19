"""Shared output base."""


# [ Import ]
# [ -Python ]
import sys


# [ Public ]
class StdOutWriter:
    """The output device."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush

    def write(self, data):
        """write to stdout."""
        self._write(data)
        self._flush()


class StdErrWriter:
    """The output device."""

    _write = sys.stderr.write
    _flush = sys.stderr.flush

    def write(self, data):
        """write to stderr."""
        self._write(data)
        self._flush()


class OutputDevice:
    """The output device."""

    def __new__(cls, *args, **kwargs):
        """Return singleton."""
        singleton = super().__new__(cls, *args, **kwargs)
        cls.__init__(singleton, *args, **kwargs)

        def return_singleton(cls, *args, **kwargs):
            """return singleton."""
            return singleton

        cls.__new__ = return_singleton

        return singleton

    def __init__(self, initial_data=''):
        """Init the state."""
        self._write_stdout = StdOutWriter().write
        self._writer = Writer()
        self._resetter = Resetter()

    def write_stream(self, stream_data):
        """actually write and record the data."""
        last_output_matches = self._last_output_matches(stream_data)
        self._reset_stream(stream_data, last_output_matches)
        to_write = self._get_stream_data_to_write(last_output_matches, stream_data)
        self._writer.write_and_replace_stds(to_write, self._write_stdout)
        self._update_stream_output(stream_data)

    # Write stream
    def _last_output_matches(self, stream_data):
        """actually write and record the data."""
        return self._writer.last_output and self._data_startswith_last_output(stream_data)

    # -last output matches
    def _data_startswith_last_output(self, data):
        """actually write and record the data."""
        return data.startswith(self._writer.last_output)
    # -last output matches

    def _reset_stream(self, stream_data, last_output_matches):
        """actually write and record the data."""
        if self._stream_needs_reset(stream_data, last_output_matches):
            self._resetter.reset()

    # -reset stream
    def _stream_needs_reset(self, stream_data, last_output_matches):
        """actually write and record the data."""
        return stream_data and not last_output_matches
    # -reset stream

    def _get_stream_data_to_write(self, last_output_matches, stream_data):
        """actually write and record the data."""
        if last_output_matches:
            to_write = self._get_new_stream_data(stream_data)
        else:
            to_write = stream_data
        return to_write

    # -get stream data to write
    def _get_new_stream_data(self, stream_data):
        """actually write and record the data."""
        return stream_data[len(self._writer.last_output):]
    # -get stream data to write

    def _update_stream_output(self, stream_data):
        """actually write and record the data."""
        self._writer.last_output = stream_data
        self._writer.last_from_stream = True
    # Write stream


class Writer:
    """The output device."""

    def __new__(cls, *args, **kwargs):
        """Return singleton."""
        singleton = super().__new__(cls, *args, **kwargs)
        cls.__init__(singleton, *args, **kwargs)

        def return_singleton(cls, *args, **kwargs):
            """return singleton."""
            return singleton

        cls.__new__ = return_singleton

        return singleton

    def __init__(self, initial_data=''):
        """Init the state."""
        self.last_output = initial_data
        self.last_from_stream = False
        self._stds_replaced = False
        self._write_stdout = StdOutWriter().write
        self._write_stderr = StdErrWriter().write
        self.writer = PlainWriter()
        self._resetter = Resetter()

    # also called internally by ---write std out/err interruption
    def write_and_replace_stds(self, data, write_func):
        """write the data via the write func."""
        self.writer.write(data, write_func)
        self._maybe_replace_stds()

    # write and replace
    def _maybe_replace_stds(self):
        """Write data to the device via the given output mechanism."""
        if self._stds_have_not_been_replaced():
            self._replace_stds()

    # -maybe replace stds
    def _stds_have_not_been_replaced(self):
        """Write data to the device via the given output mechanism."""
        return not self._stds_replaced

    def _replace_stds(self):
        """replace the std streams."""
        self._replace(sys.stdout, 'write', self._write_std_out_interruption)
        self._replace(sys.stderr, 'write', self._write_std_err_interruption)

    # --replace stds
    def _write_std_out_interruption(self, data):
        """Actually write the data."""
        self._write_interruption(data, self._write_stdout)

    def _write_std_err_interruption(self, data):
        """Actually write the data."""
        self._write_interruption(data, self._write_stderr)

    # ---write std out/err interruption
    def _write_interruption(self, data, write_func):
        """write an interruption."""
        self._reset_interruption(data)
        self.writer.write(data, write_func)
        self._update_interruption_output(data)

    # ----write interruption
    def _reset_interruption(self, data):
        """Actually write the data."""
        if self._interruption_needs_reset(data):
            self._resetter.reset()

    # -----reset interruption
    def _interruption_needs_reset(self, data):
        """Actually write the data."""
        return data and self.last_from_stream
    # -----reset interruption

    def _update_interruption_output(self, interruption_data):
        """actually write and record the data."""
        self.last_output = interruption_data
        self.last_from_stream = False
    # ----write interruption
    # ---write std out/err interruption

    def _replace(self, parent, func_name, replacement):
        """watch the output."""
        setattr(parent, func_name, replacement)
    # --replace stds
    # -maybe replace stds
    # write


class PlainWriter:
    """The output device."""

    def __new__(cls, *args, **kwargs):
        """Return singleton."""
        singleton = super().__new__(cls, *args, **kwargs)
        cls.__init__(singleton, *args, **kwargs)

        def return_singleton(cls, *args, **kwargs):
            """return singleton."""
            return singleton

        cls.__new__ = return_singleton

        return singleton

    def __init__(self, initial_data=''):
        """Init the state."""
        self.is_reset = False

    def write(self, data, write_func):
        """write the data via the write func."""
        write_func(data)
        self._set_reset(self._data_ends_with_reset(data))

    # -write
    def _data_ends_with_reset(self, data):
        """Write data to the device via the given output mechanism."""
        return data.endswith('\n')

    def _set_reset(self, is_reset):
        """Write data to the device via the given output mechanism."""
        self.is_reset = is_reset


class Resetter:
    """The output device."""

    def __new__(cls, *args, **kwargs):
        """Return singleton."""
        singleton = super().__new__(cls, *args, **kwargs)
        cls.__init__(singleton, *args, **kwargs)

        def return_singleton(cls, *args, **kwargs):
            """return singleton."""
            return singleton

        cls.__new__ = return_singleton

        return singleton

    def __init__(self, initial_data=''):
        """Init the state."""
        self._write_stdout = StdOutWriter().write
        self._writer = PlainWriter()

    def reset(self):
        """Reset the device."""
        if self._is_not_reset():
            self._reset()

    # reset
    def _is_not_reset(self):
        """Reset the device."""
        return not self._writer.is_reset

    def _reset(self):
        """Reset the device."""
        self._writer.write('\n', self._write_stdout)
    # reset
