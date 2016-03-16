"""Test streams."""


# [ Imports ]
from foot.libs import expect
from otter import FunctionSink, Stream


# [ Implementations ]
def Sink():
    """test sink."""
    return FunctionSink(lambda o: o)


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
    expect.equals(sink.last_output, "\nhi")


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
    expect.equals(sink.last_output, "hi")


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
    expect.equals(sink.last_output, "\nhi")


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


def test_outputting_newline_in_stream_output_partially_resets_stream():
    """
    Test.

    Given a stream is set up.
    When it is written to with a newline in the iddle.
    Then it has the same registrations but only teh data after the final newline in the data.
    """
    # Given
    sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.write('hi')

    # When
    stream.write(' there\nhow are')

    # Then
    expect.equals(stream.data, 'how are')
    expect.equals(stream.sink, sink)
    expect.contains(sink.observers, stream.observe_sink)


def test_observing_multiple_sinks():
    """
    Test.

    Given a stream observing a second sink
    When data is written to that sink
    Then the stream is interrupted.
    """
    # Given
    sink = Sink()
    other_sink = Sink()
    stream = Stream()
    stream.register_sink(sink)
    stream.register_sink(other_sink)
    stream.write('hi')

    # When
    other_sink.write('interruption')

    # Then
    expect.equals(stream.interrupted, True)

    # When
    stream.write(' there')
    sink.write('other interruption')

    # Then
    expect.equals(stream.interrupted, True)

    # When
    stream.write(' folks')

    # Then
    expect.equals(sink.last_output, '\nhi there folks')
