"""
Semantic actions, core to the library.

In Clean Architecture terms - the business logic.
"""


import functools


def _write(data, *, from_stream=False, write_interactor, recorder_interactor):
    """write & record the given data."""
    output = write_interactor.write(data)
    recorder_interactor.record(data, from_stream=from_stream)
    return output


def _reset(*, write_interactor, recorder_interactor):
    """reset the output state so that a new stream is obviously new."""
    if not write_interactor.is_reset(recorder_interactor.output_record):
        write_interactor.reset()


def write_from_stream(prior_stream_data, data, *, write_interactor, recorder_interactor):
    """
    Write data from a stream.

    Takes the prior stream data, the new data, and write/record interactors.

    Returns the return from the write_interactor.
    """
    # set up the write function
    write = functools.partial(
        _write,
        from_stream=True,
        write_interactor=write_interactor,
        recorder_interactor=recorder_interactor
    )
    # if the last recorded output matches
    if prior_stream_data and recorder_interactor.output_record.endswith(prior_stream_data):
        # write the new data
        output = write(data)
    else:
        # reset the writer if there's really data to write
        if data:
            _reset(
                write_interactor=write_interactor,
                recorder_interactor=recorder_interactor
            )
        # write the old data, then the new data
        output = write(prior_stream_data + data)
    # return what the writer returned
    return output


def write_interruption(data, *, write_interactor, recorder_interactor):
    """interruption writer."""
    # if stream data was printed last and there is new data to print
    if (
        data and
        # recorder_interactor.output_record and
        recorder_interactor.last_from_stream
    ):
        # reset the output
        _reset(
            write_interactor=write_interactor,
            recorder_interactor=recorder_interactor
        )
    # write and record the non-stream output
    return _write(
        data,
        from_stream=False,
        write_interactor=write_interactor,
        recorder_interactor=recorder_interactor
    )
