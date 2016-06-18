"""Shared output base."""


# [ Import ]
# [ -Python ]
import sys


# [ Public ]
class OutputDevice:
    """The output device."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush

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
        self._last_output = initial_data
        self._last_from_stream = False
        self._stds_replaced = False

    def reset(self):
        """Reset the device."""
        if not self._is_reset:
            self.old_write('\n')

    def old_write(self, data):
        """Write data to the device via the given output mechanism."""
        self._write(data)
        self._flush()
        self._is_reset = data.endswith('\n')
        if not self._stds_replaced:
            self._replace_stds()

    # [ Private ]
    # [ -Internal ]
    def write_stream(self, stream_data):
        """actually write and record the data."""
        last_output_matches = self._last_output and stream_data.startswith(self._last_output)
        if stream_data and not last_output_matches:
            self.reset()
        if last_output_matches:
            to_write = stream_data[len(self._last_output):]
        else:
            to_write = stream_data
        self.old_write(to_write)
        self._last_output = stream_data
        self._last_from_stream = True

    # [ Private ]
    # [ -Interactor ]
    def write_interruption(self, data):
        """Actually write the data."""
        if data and self._last_from_stream:
            self.reset()
        self.old_write(data)
        self._last_output = data
        self._last_from_stream = False

    def _replace_stds(self):
        """replace the std streams."""
        self._replace(sys.stdout, 'write')
        self._replace(sys.stderr, 'write')

    def _replace(self, parent, func_name):
        """watch the output."""
        write = InterruptionWriter(output_device=self).write
        setattr(parent, func_name, write)


class InterruptionWriter:
    """Interruption Writer."""

    def __init__(self, *, output_device=OutputDevice()):
        """init the state."""
        # initial state.
        self._output_device = output_device

    # [ Public ]
    # [ -Internal ]
    def write(self, data):
        """write the data."""
        return self._output_device.write_interruption(data)
