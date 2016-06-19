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

    def __init__(self):
        """Init the state."""
        self._write_stdout = StdOutWriter().write  # _write
        self._replacer = Replacer()  # _replace_stds
        self._resetter = Resetter()  # _reset_stream
        self._record_keeper = RecordKeeper

    def write_stream(self, stream_data):
        """actually write and record the data."""
        # Write
        # -last output
        last_output_matches = self._last_output_matches(stream_data)
        self._reset_stream(stream_data, last_output_matches)
        to_write = self._get_stream_data_to_write(last_output_matches, stream_data)
        # -last output
        self._write(to_write)
        # Write

        self._replace_stds()
        self._update_stream_output(stream_data)

    # Write stream
    def _data_startswith_last_output(self, data):
        """actually write and record the data."""
        # arg data
        # external data
        return data.startswith(self._record_keeper.last_output)

    def _last_output_matches(self, stream_data):
        """actually write and record the data."""
        # arg data
        # external data
        return self._record_keeper.last_output and self._data_startswith_last_output(stream_data)

    def _reset_stream(self, stream_data, last_output_matches):
        """actually write and record the data."""
        # internal
        # external
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
        # arg data
        # external data
        return stream_data[len(self._record_keeper.last_output):]
    # -get stream data to write

    def _write(self, to_write):
        """actually write and record the data."""
        # arg data
        # internal data
        self._resetter.write(to_write, self._write_stdout)

    def _replace_stds(self):
        """actually write and record the data."""
        self._replacer.replace_stds()

    def _update_stream_output(self, stream_data):
        """actually write and record the data."""
        self._record_keeper.last_output = stream_data
        self._record_keeper.last_from_stream = True
    # Write stream


class Replacer:
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
        self._record_keeper = RecordKeeper
        self._stds_replaced = False
        self._write_stdout = StdOutWriter().write  # write stdout
        self._write_stderr = StdErrWriter().write  # write stderr
        self._resetter = Resetter()  # reset interruption

    def replace_stds(self):
        """Write data to the device via the given output mechanism."""
        if self._stds_have_not_been_replaced():
            self._replace_stds()

    # replace_stds
    def _stds_have_not_been_replaced(self):
        """Write data to the device via the given output mechanism."""
        return not self._stds_replaced

    def _replace_stds(self):
        """replace the std streams."""
        # action
        self._replace(sys.stdout, 'write', self._write_std_out_interruption)
        self._replace(sys.stderr, 'write', self._write_std_err_interruption)
        # data
        self._stds_replaced = True

    # -replace stds
    def _write_std_out_interruption(self, data):
        """Actually write the data."""
        self._write_interruption(data, self._write_stdout)

    def _write_std_err_interruption(self, data):
        """Actually write the data."""
        self._write_interruption(data, self._write_stderr)

    # --write std out/err interruption
    def _write_interruption(self, data, write_func):
        """write an interruption."""
        # internal action
        self._reset_interruption(data)
        # external action
        self._resetter.write(data, write_func)
        # internal action
        self._update_interruption_output(data)

    # ---write interruption
    def _reset_interruption(self, data):
        """Actually write the data."""
        # internal
        # external
        if self._interruption_needs_reset(data):
            self._resetter.reset()

    # ----reset interruption
    def _interruption_needs_reset(self, data):
        """Actually write the data."""
        # arg data
        # external data
        return data and self._record_keeper.last_from_stream
    # ----reset interruption

    def _update_interruption_output(self, interruption_data):
        """actually write and record the data."""
        self._record_keeper.last_output = interruption_data
        self._record_keeper.last_from_stream = False
    # ---write interruption
    # --write std out/err interruption

    def _replace(self, parent, func_name, replacement):
        """watch the output."""
        setattr(parent, func_name, replacement)
    # -replace stds
    # replace_stds


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
        self._is_reset = False
        self._write_stdout = StdOutWriter().write  # _reset

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
        self._is_reset = is_reset
    # -write

    def reset(self):
        """Reset the device."""
        if self._is_not_reset():
            self._reset()

    # reset
    def _is_not_reset(self):
        """Reset the device."""
        return not self._is_reset

    def _reset(self):
        """Reset the device."""
        self.write('\n', self._write_stdout)
    # reset


class RecordKeeper:
    """Keep a record of the last output and its source."""

    last_output = ''
    last_from_stream = False
