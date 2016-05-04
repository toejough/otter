"""Test the use cases."""


# [ Imports ]
# [ -Python ]
from unittest import TestCase
# [ -Project ]
from . import use_cases


# [ Helpers ]
T = TestCase()


class Writer:
    """
    test writer.

    Call an instance to proxy writing.
    """

    def __init__(self):
        """init state."""
        self.written = ''

    def __call__(self, data):
        """call the writer."""
        self.written += data


# [ Use Cases ]
def test_example():
    """test."""
    # Given
    # When
    # Then
    pass


# [ Basic use cases ]
# when a new stream is started at a new line, the data is just printed.
# when a new stream is started mid-line, a new line is printed, then the new stream data is printed.
# when continuation data is sent, and the line only contains the prior data from the stream, the data is just printed.
# when continuation data is sent, and the line contains something other than the prior data from the stream, and it's at a new line, the prior data is printed as if starting a new stream at a new line, then the new data is printed.
# when continuation data is sent, and the line contains something other than the prior data from the stream, and it's mid line, the prior data is printed as if starting a new stream mid line, then the new data is printed.
# when data is sent, but not through a stream, and there is a new line, the data is printed
# when data is sent, but not through a stream, and there is not a new line, and the last thing to print was a stream, then a newline is printed and the data is printed
# when data is sent, but not through a stream, and there is not a new line, and the last thing to print was not a stream, the the data is printed.


def test_new_stream_new_line():
    """test."""
    # Given
    data = 'initial stream data'
    write = Writer()

    # When
    use_cases.start_new_stream_at_new_line(write, data)

    # Then
    T.assertEqual(data, write.written)


def test_new_stream_mid_line():
    """test."""
    # Given
    data = 'mid-stream data'
    expected_written = '\n' + data
    write = Writer()

    # When
    use_cases.start_new_stream_mid_line(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def test_continuation_from_prior_data():
    """test."""
    # Given
    data = 'continuation data'
    expected_written = data
    write = Writer()

    # When
    use_cases.continue_stream_from_prior_data(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def test_continuation_from_new_line():
    """test."""
    # Given
    data = 'continuation data'
    prior_data = 'initial stream data '

    start_write = Writer()
    use_cases.start_new_stream_at_new_line(start_write, prior_data)

    continue_write = Writer()
    use_cases.continue_stream_from_prior_data(continue_write, data)

    expected_written = start_write.written + continue_write.written
    write = Writer()

    # When
    use_cases.continue_stream_from_new_line(write, data, prior_data)

    # Then
    T.assertEqual(expected_written, write.written)


def test_continuation_from_mid_line():
    """test."""
    # Given
    data = 'continuation data'
    prior_data = 'initial stream data '

    start_write = Writer()
    use_cases.start_new_stream_mid_line(start_write, prior_data)

    continue_write = Writer()
    use_cases.continue_stream_from_prior_data(continue_write, data)

    expected_written = start_write.written + continue_write.written
    write = Writer()

    # When
    use_cases.continue_stream_from_mid_line(write, data, prior_data)

    # Then
    T.assertEqual(expected_written, write.written)


def test_non_stream_at_new_line():
    """test."""
    # Given
    data = 'non-stream data'

    expected_written = data
    write = Writer()

    # When
    use_cases.write_non_stream_at_new_line(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def test_non_stream_mid_stream():
    """test."""
    # Given
    data = 'non-stream data'

    expected_written = '\n' + data
    write = Writer()

    # When
    use_cases.write_non_stream_mid_stream(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def test_non_stream_mid_line():
    """test."""
    # Given
    data = 'non-stream data'

    expected_written = data
    write = Writer()

    # When
    use_cases.write_non_stream_mid_line(write, data)

    # Then
    T.assertEqual(expected_written, write.written)
