"""Shared output base."""


# [ Import ]
# [ -Python ]
import sys


# [ Public ]
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

    def set_reset(self, data):
        """write the data via the write func."""
        # should be the only direct setter of _is_reset
        self._is_reset = self._data_ends_with_reset(data)

    # set_reset
    def _data_ends_with_reset(self, data):
        """Write data to the device via the given output mechanism."""
        return data.endswith('\n')
    # set_reset

    def reset(self, writer):
        """Reset the device."""
        if self._is_not_reset():
            self._reset(writer)

    # reset
    def _is_not_reset(self):
        """Reset the device."""
        # should be the only direct getter of _is_reset
        return not self._is_reset

    def _reset(self, writer):
        """Reset the device."""
        writer.write('\n')
    # reset


class BaseStdWriter:
    """The output device."""

    _resetter = Resetter()

    def write(self, data):
        """write to stdout."""
        self._write(data)
        self._flush()
        self._record_reset(data)

    # write
    def _write(self, data):
        """write."""
        raise NotImplementedError

    def _flush(self):
        """flush."""
        raise NotImplementedError

    def _record_reset(self, data):
        """write to stdout."""
        self._resetter.set_reset(data)
    # write

    def reset(self):
        """reset stdout."""
        self._resetter.reset(self)


class StdOutWriter(BaseStdWriter):
    """The output device."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush


class StdErrWriter(BaseStdWriter):
    """The output device."""

    _write = sys.stderr.write
    _flush = sys.stderr.flush


class OutputDevice:
    """The output device."""

    def __init__(self, *, writer=StdOutWriter()):
        """Init the state."""
        self._writer = writer  # 2
        self._replacer = Replacer()  # _replace_stds
        self._record_keeper = RecordKeeper  # 4

    def write_stream(self, stream_data):
        """actually write and record the data."""
        self._write(stream_data)
        self._replace_stds()
        self._update_stream_output(stream_data)

    # Write stream
    def _write(self, stream_data):
        """actually write and record the data."""
        last_output = self._get_last_output()
        last_output_matches = self._last_output_matches(stream_data, last_output)
        self._reset_stream(stream_data, last_output_matches)
        to_write = self._get_stream_data_to_write(last_output_matches, stream_data, last_output)
        self._write_new_data(to_write)

    # -write
    def _get_last_output(self):
        """get the last output."""
        return self._record_keeper.last_output

    def _last_output_matches(self, stream_data, last_output):
        """actually write and record the data."""
        return last_output and self._data_starts_with(stream_data, last_output)

    # --last_output_matches
    def _data_starts_with(self, data, last_output):
        """actually write and record the data."""
        return data.startswith(last_output)
    # --last_output_matches

    def _reset_stream(self, stream_data, last_output_matches):
        """actually write and record the data."""
        if self._stream_needs_reset(stream_data, last_output_matches):
            self._reset()

    # --reset stream
    def _stream_needs_reset(self, stream_data, last_output_matches):
        """actually write and record the data."""
        return stream_data and not last_output_matches

    def _reset(self):
        """reset the stream."""
        self._writer.reset()
    # --reset stream

    def _get_stream_data_to_write(self, last_output_matches, stream_data, last_output):
        """actually write and record the data."""
        if last_output_matches:
            to_write = self._get_new_stream_data(stream_data, last_output)
        else:
            to_write = stream_data
        return to_write

    # --get stream data to write
    def _get_new_stream_data(self, stream_data, last_output):
        """actually write and record the data."""
        return stream_data[len(last_output):]
    # --get stream data to write

    def _write_new_data(self, to_write):
        """write the new data."""
        self._writer.write(to_write)
    # -write

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
        self._stdout_writer = StdOutWriter()  # write stdout
        self._stderr_writer = StdErrWriter()  # write stderr

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
        self._set_stds_replaced()

    # -replace stds
    def _write_std_out_interruption(self, data):
        """Actually write the data."""
        self._write_interruption(data, self._stdout_writer)

    def _write_std_err_interruption(self, data):
        """Actually write the data."""
        self._write_interruption(data, self._stderr_writer)

    # --write std out/err interruption
    def _write_interruption(self, data, writer):
        """write an interruption."""
        self._reset_interruption(data, writer)
        writer.write(data)
        self._update_interruption_output(data)

    # ---write interruption
    def _reset_interruption(self, data, writer):
        """Actually write the data."""
        if self._interruption_needs_reset(data):
            writer.reset()

    # ----reset interruption
    def _interruption_needs_reset(self, data):
        """Actually write the data."""
        return data and self._get_last_from_stream()

    # -----interruption needs reset
    def _get_last_from_stream(self):
        """last from stream."""
        return self._record_keeper.last_from_stream
    # -----interruption needs reset
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

    def _set_stds_replaced(self):
        """set stds replaced."""
        self._stds_replaced = True
    # -replace stds
    # replace_stds


class RecordKeeper:
    """Keep a record of the last output and its source."""

    last_output = ''
    last_from_stream = False
