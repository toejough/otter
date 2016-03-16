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
