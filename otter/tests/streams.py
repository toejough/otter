"""Test streams."""


# [ Imports ]
from foot.libs import expect


# [ Implementations ]
def start_stream(output, state, sink):
    """Start a stream."""
    if state['on newline']:
        sink(output)
    else:
        sink('\n' + output)
    return {
        'sink': sink
    }


def write_stream(output, stream):
    """Write to a stream."""
    stream['sink'](output)


# [ Tests ]
def test_streams_start_on_new_line_unknown():
    """
    Test.

    Given prior state of output system (unknown)
    When a stream is begun
    Then it begins on a new line.
    """
    # Given
    output_state = {'on newline': None}
    printed = None

    def sink(output):
        """a test output function."""
        nonlocal printed
        printed = output

    # When
    start_stream("hi", output_state, sink)

    # Then
    expect.equals(printed, "\nhi")


def test_streams_start_on_new_line_from_new_line():
    """
    Test.

    Given prior state of output system (new line)
    When a stream is begun
    Then it begins on a new line.
    """
    # Given
    output_state = {'on newline': True}
    printed = None

    def sink(output):
        """a test output function."""
        nonlocal printed
        printed = output

    # When
    start_stream("hi", output_state, sink)

    # Then
    expect.equals(printed, "hi")


def test_streams_start_on_new_line_from_non_new_line():
    """
    Test.

    Given prior state of output system (not-new-line)
    When a stream is begun
    Then it begins on a new line.
    """
    # Given
    output_state = {'on newline': False}
    printed = None

    def sink(output):
        """a test output function."""
        nonlocal printed
        printed = output

    # When
    start_stream("hi", output_state, sink)

    # Then
    expect.equals(printed, "\nhi")


def test_streams_output_to_a_sink():
    """
    Test.

    Given an existing stream.
    When data is printed to it.
    Then the data is printed to the sink.
    """
    # Given
    output_state = {'on newline': False}
    printed = None

    def sink(output):
        """a test output function."""
        nonlocal printed
        printed = output
    stream = start_stream("hi", output_state, sink)

    # When
    write_stream(' there', stream)

    # Then
    expect.equals(printed, ' there')


def test_other_outputs_are_interruptions_to_stream():
    """
    Test.

    Given a stream outputting to a sink.
    When the sink is called from another source
    Then the stream is interrupted.
    """
    # Given
    output_state = {'on newline': False}
    printed = None

    def sink(output):
        """a test output function."""
        nonlocal printed
        printed = output
    stream = start_stream("hi", output_state, sink)

    # When
    sink('foo')

    # Then
    expect.equals(stream['is interrupted'], True)
