"""
Otter - output interruption library.

Allows you to define output streams with the following characteristics:
    * streams start on a new line.
    * streams output to a sink.
    * other outputs to the sink constitute an interruption to the stream.  Streams observe the sink to know when it is called.
    * interruptions to a stream start on a new line.
    * output to the stream after an interruption starts on a new line, and reprints the entire stream so far, adding the new output.
    * writing to a stream with output which ends in a new line resets the stream, including data and registrations.
    * writing to a stream with output which contains a newline resets the data to only what is after the final newline, but retains registrations.
    * streams can observe multple sinks.
"""


import sys


class FunctionSink:
    """Function sink."""

    def __init__(self, func):
        """obj init."""
        self.on_newline = None
        self.observers = []
        self.last_output = None
        self.func = func
        self.other_sinks = []

    def register_observer(self, observer):
        """register an observer."""
        self.observers.append(observer)

    def unregister_observer(self, observer):
        """unregister an observer."""
        if observer in self.observers:
            self.observers.remove(observer)

    def write(self, output, writer=None):
        """write the output.  Also notify observers."""
        needs_newline = False
        for observer in self.observers:
            if observer(output, writer):
                needs_newline = True
        if needs_newline and not self.on_newline:
            self.last_output = '\n' + output
        else:
            self.last_output = output
        self.func(self.last_output)
        if output:
            self.on_newline = output.endswith('\n')
        for sink in self.other_sinks:
            sink.on_newline = self.on_newline


class Stream:
    """A stream object."""

    def __init__(self):
        """obj init."""
        self.sink = None
        self.interrupted = False
        self.started = False
        self.data = ''
        self.other_sinks = []

    def register_sink(self, sink):
        """Register the sink to send output to."""
        if self.sink is None:
            self.sink = sink
        else:
            self.other_sinks.append(sink)
        sink.register_observer(self.observe_sink)

    def write(self, output):
        """Write the output to the sink."""
        if output:
            self.data += output
            if self.interrupted:
                self.sink.write(self.data, self)
            else:
                self.sink.write(output, self)
            self.started = True
            self.interrupted = False
            if output.endswith('\n'):
                self.reset()
            if '\n' in self.data:
                _, new = self.data.rsplit('\n', 1)
                self.data = new

    def reset(self):
        """reset the stream."""
        self.sink.unregister_observer(self.observe_sink)
        self.sink = None
        for sink in self.other_sinks:
            sink.unregister_observer(self.observe_sink)
        self.other_sinks = []
        self.interrupted = False
        self.started = False
        self.data = ''

    def observe_sink(self, output, writer):
        """observe a change in a sink."""
        new_interruption = False
        fresh_output = False
        post_interruption = False
        if output and self.data:
            if writer is not self:
                if not self.interrupted:
                    new_interruption = True
                self.interrupted = True
            elif not self.started:
                fresh_output = True
            elif self.interrupted:
                post_interruption = True
        return new_interruption or fresh_output or post_interruption


DEFAULT_SINKS = []
_STD_SINKS = []


def DefaultStream():
    """Get the default stream."""
    stream = Stream()
    for sink in DEFAULT_SINKS:
        stream.register_sink(sink)
    return stream


def use_stds():
    """Use the standard out/err streams as the default sinks."""
    global DEFAULT_SINKS
    global _STD_SINKS

    if _STD_SINKS:
        DEFAULT_SINKS = _STD_SINKS
    else:
        original_stdout_write = sys.stdout.write

        def write_and_flush(output):
            """write and flush."""
            original_stdout_write(output)
            sys.stdout.flush()

        std_out_sink = FunctionSink(write_and_flush)
        std_err_sink = FunctionSink(sys.stderr.write)

        std_out_sink.other_sinks.append(std_err_sink)
        std_err_sink.other_sinks.append(std_out_sink)

        sys.stdout.write = std_out_sink.write
        sys.stderr.write = std_err_sink.write

        DEFAULT_SINKS = _STD_SINKS = [std_out_sink, std_err_sink]
