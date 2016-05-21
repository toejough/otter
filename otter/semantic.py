"""Semantic interactions with the library."""


from . import app


class Stream:
    """Stream."""

    def __init__(self):
        """init the state."""
        self.data = ''

    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output from any of the watched outputs.
        """
        if not data:
            pass
        else:
            self._write(data)

    def _write(self, data):
        """
        Actually write the data.

        Differs from self.write in that this does not filter out falsy input.
        """
        if app.get_observed_output.endswith(self.data):
            app.write(data)
        else:
            app.reset()
            app.write(self.data)
            app.write(data)
        self.data += data


def watch_output_from(func):
    """watch the output."""
    app.watch_output_from(func)
