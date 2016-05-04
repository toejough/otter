"""Use case implementation functions."""


# [ Basic use cases ]
# when a new stream is started at a new line, the data is just printed.
# when a new stream is started mid-line, a new line is printed, then the new stream data is printed.
# when continuation data is sent, and the line only contains the prior data from the stream, the data is just printed.
# when continuation data is sent, and the line contains something other than the prior data from the stream, and it's at a new line, the prior data is printed as if starting a new stream at a new line, then the new data is printed.
# when continuation data is sent, and the line contains something other than the prior data from the stream, and it's mid line, the prior data is printed as if starting a new stream mid line, then the new data is printed.
# when data is sent, but not through a stream, and there is a new line, the data is printed
# when data is sent, but not through a stream, and there is not a new line, and the last thing to print was a stream, then a newline is printed and the data is printed
# when data is sent, but not through a stream, and there is not a new line, and the last thing to print was not a stream, the the data is printed.


# [ Use Cases ]
def start_new_stream_at_new_line(write, data):
    """
    Write initial stream data at a new line.

    Simply writes the data.
    """
    write(data)


def start_new_stream_mid_line(write, data):
    """
    start a new stream mid line.

    writes a new line first, then the data.
    """
    write('\n' + data)


def continue_stream_from_prior_data(write, data):
    """
    Continue a stream from prior data.

    writes the new data.
    """
    write(data)


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


def write_non_stream_at_new_line(write, data):
    """
    write non-stream data from a new line.

    just write the data
    """
    write(data)


def write_non_stream_mid_stream(write, data):
    """
    write non-stream data from mid-stream.

    write a new line then the data
    """
    write('\n' + data)


def write_non_stream_mid_line(write, data):
    """
    write non-stream data from mid-line.

    just write the data
    """
    write(data)
