"""Test streams."""


# [ Imports ]
from foot.libs import expect


# [ Implementations ]
class Stream:
    """A stream object."""

    def __init__(self):
        """obj init."""
        self.sink = None
        self.interrupted = False
        self.started = False
        self.data = ''

    def register_sink(self, sink):
        """Register the sink to send output to."""
        self.sink = sink
        sink.register_observer(self.observe_sink)

    def write(self, output):
        """Write the output to the sink."""
        self.data += output
        if self.interrupted:
            self.sink.write(self.data, self)
        else:
            self.sink.write(output, self)
        self.started = True
        self.interrupted = False
        if output.endswith('\n'):
            self.reset()

    def reset(self):
        """reset the stream."""
        self.sink.unregister_observer(self.observe_sink)
        self.sink = None
        self.interrupted = False
        self.started = False
        self.data = ''

    def observe_sink(self, output, writer):
        """observe a change in a sink."""
        new_interruption = False
        fresh_output = False
        post_interruption = False
        if writer is not self:
            if not self.interrupted:
                new_interruption = True
            self.interrupted = True
        elif not self.started:
            fresh_output = True
        elif self.interrupted:
            post_interruption = True
        return new_interruption or fresh_output or post_interruption


class Sink:
    """Test sink."""

    def __init__(self):
        """obj init."""
        self.on_newline = None
        self.observers = []
        self.output = ''
        self.last_output = None

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
        self.output += self.last_output


# [ Tests ]
def test_streams_start_on_new_line_unknown():
    """
    Test.

    Given prior state of output system (unknown)
    When a stream is begun
    Then it begins on a new line.
    """
    # Given
    sink = Sink()
    sink.on_newline = None

    # When
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # Then
    expect.equals(sink.output, "\nhi")


def test_streams_start_on_new_line_from_new_line():
    """
    Test.

    Given prior state of output system (new line)
    When a stream is begun
    Then it begins on a new line.
    """
    # Given
    sink = Sink()
    sink.on_newline = True

    # When
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # Then
    expect.equals(sink.output, "hi")


def test_streams_start_on_new_line_from_non_new_line():
    """
    Test.

    Given prior state of output system (not-new-line)
    When a stream is begun
    Then it begins on a new line.
    """
    # Given
    sink = Sink()
    sink.on_newline = False

    # When
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # Then
    expect.equals(sink.output, "\nhi")


def test_streams_output_to_a_sink():
    """
    Test.

    Given an existing stream.
    When data is printed to it.
    Then the data is printed to the sink.
    """
    # Given
    sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # When
    stream.write(' there')

    # Then
    expect.equals(sink.last_output, " there")


def test_other_outputs_are_interruptions_to_stream():
    """
    Test.

    Given a stream outputting to a sink.
    When the sink is called from another source
    Then the stream is interrupted.
    """
    # Given
    sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # When
    sink.write('hello!')

    # Then
    expect.equals(stream.interrupted, True)


def test_interruptions_to_stream_start_on_new_line():
    """
    Test.

    Given a started stream.
    When an interruption occurs
    Then the interruption starts on a new line.
    """
    # Given
    sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # When
    sink.write('interruption')

    # Then
    expect.equals(sink.last_output, '\ninterruption')


def test_output_to_stream_after_interruption_starts_on_new_line_and_reprints_stream():
    """
    Test.

    Given a stream with data printed to it.
    and an interruption has occurred
    When more data is printed to the stream
    Then the whole stream is reprinted on a new line.
    """
    # Given
    sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')
    sink.write('interruption')

    # When
    stream.write(' there')

    # Then
    expect.equals(sink.last_output, '\nhi there')


def test_outputting_newline_at_end_of_stream_output_resets_stream():
    """
    Test.

    Given a stream is set up.
    When it is written to with a newline at the end.
    Then it has no data and no registrations.
    """
    # Given
    sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # When
    stream.write(' there\n')

    # Then
    expect.equals(stream.data, '')
    expect.equals(stream.sink, None)
    expect.does_not_contain(sink.observers, stream.observe_sink)
