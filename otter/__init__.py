"""
Otter: restream your data.

Outputs a stream of data.
Watches the output.
Restreams the data if more is posted after an interruption has occurred.

Defaults to watching stdout and stderr, and printing to stdout.
"""


# [ Imports ]
from unittest import TestCase


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
    start_new_stream_at_new_line(write, data)

    # Then
    T.assertEqual(data, write.written)


def start_new_stream_at_new_line(write, data):
    """
    Write initial stream data at a new line.

    Simply writes the data.
    """
    write(data)


def test_new_stream_mid_line():
    """test."""
    # Given
    data = 'mid-stream data'
    expected_written = '\n' + data
    write = Writer()

    # When
    start_new_stream_mid_line(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def start_new_stream_mid_line(write, data):
    """
    start a new stream mid line.

    writes a new line first, then the data.
    """
    write('\n' + data)


def test_continuation_from_prior_data():
    """test."""
    # Given
    data = 'continuation data'
    expected_written = data
    write = Writer()

    # When
    continue_stream_from_prior_data(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def continue_stream_from_prior_data(write, data):
    """
    Continue a stream from prior data.

    writes the new data.
    """
    write(data)


def test_continuation_from_new_line():
    """test."""
    # Given
    data = 'continuation data'
    prior_data = 'initial stream data '

    start_write = Writer()
    start_new_stream_at_new_line(start_write, prior_data)

    continue_write = Writer()
    continue_stream_from_prior_data(continue_write, data)

    expected_written = start_write.written + continue_write.written
    write = Writer()

    # When
    continue_stream_from_new_line(write, data, prior_data)

    # Then
    T.assertEqual(expected_written, write.written)


def continue_stream_from_new_line(
    write, data, prior_data,
    start_at_new_line=start_new_stream_at_new_line,
    continue_from_prior=continue_stream_from_prior_data
):
    """
    Continue a stream from a new line.

    restarts the stream with the prior data at the new line, then continues the stream from that data.
    """
    start_at_new_line(write, prior_data)
    continue_from_prior(write, data)


def test_continuation_from_mid_line():
    """test."""
    # Given
    data = 'continuation data'
    prior_data = 'initial stream data '

    start_write = Writer()
    start_new_stream_mid_line(start_write, prior_data)

    continue_write = Writer()
    continue_stream_from_prior_data(continue_write, data)

    expected_written = start_write.written + continue_write.written
    write = Writer()

    # When
    continue_stream_from_mid_line(write, data, prior_data)

    # Then
    T.assertEqual(expected_written, write.written)


def continue_stream_from_mid_line(
    write, data, prior_data,
    start_mid_line=start_new_stream_mid_line,
    continue_from_prior=continue_stream_from_prior_data
):
    """
    Continue a stream from a new line.

    restarts the stream with the prior data at the new line, then continues the stream from that data.
    """
    start_mid_line(write, prior_data)
    continue_from_prior(write, data)


def test_non_stream_at_new_line():
    """test."""
    # Given
    data = 'non-stream data'

    expected_written = data
    write = Writer()

    # When
    write_non_stream_at_new_line(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def write_non_stream_at_new_line(write, data):
    """
    write non-stream data from a new line.

    just write the data
    """
    write(data)


def test_non_stream_mid_stream():
    """test."""
    # Given
    data = 'non-stream data'

    expected_written = '\n' + data
    write = Writer()

    # When
    write_non_stream_mid_stream(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def write_non_stream_mid_stream(write, data):
    """
    write non-stream data from mid-stream.

    write a new line then the data
    """
    write('\n' + data)


# when data is sent, but not through a stream, and there is not a new line, and the last thing to print was not a stream, the the data is printed.
def test_non_stream_mid_line():
    """test."""
    # Given
    data = 'non-stream data'

    expected_written = data
    write = Writer()

    # When
    write_non_stream_mid_line(write, data)

    # Then
    T.assertEqual(expected_written, write.written)


def write_non_stream_mid_line(write, data):
    """
    write non-stream data from mid-line.

    just write the data
    """
    write(data)
