"""Watch the given outputs for their data."""


import sys


class Watcher:
    """Watch the given outputs for their data."""

    def __init__(self):
        """init state."""
        self._wrapped = []
        self._interrupted = False

    def set_singleton(self):
        """Replace the parent module with self."""
        sys.modules[__name__] = self

    def _record_output(self, data):
        """Record outputted data."""
        self._output_record += data

    def _wrap(self, func):
        """wrap the function call, and watch its contents."""
        def wrapper(data):
            """wrap."""
            self._record_output(data)
            self._interrupted = True
            return func(data)

        return wrapper

    def watch(self, parent, func_name):
        """watch a function's output."""
        func = getattr(parent, func_name)
        if func not in self.wrapped:
            wrapped = self._wrap(func)
            setattr(parent, func_name, wrapped)
            self._wrapped.append(wrapped)

    def get_output(self):
        """return the output record."""
        return self._output_record

    def clear_interruption(self):
        """clear interruption status."""
        self._interrupted = False


# set singleton
Watcher().set_singleton()
