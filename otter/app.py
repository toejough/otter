"""The How of the application."""


import functools


def output_ends_with(data, *, recorder_interactor):
    """return the remembered data."""
    return data and recorder_interactor.output_record.endswith(data)


def write(data, *, write_interactor, recorder_interactor):
    """write & record the given data."""
    write_interactor.write(data)
    recorder_interactor.record(data, from_stream=True)


def reset(*, write_interactor, recorder_interactor):
    """reset the output state so that a new stream is obviously new."""
    if not write_interactor.is_reset(recorder_interactor.output_record):
        write_interactor.reset()


def replace(parent, func_name, replacement_writer, *, recorder_interactor):
    """watch the output from the function."""
    @functools.wraps(getattr(parent, func_name))
    def wrapped(data):
        """wrapped interruption writer."""
        # if stream data was printed last and there is new data to print
        prior_data = recorder_interactor.output_record
        if (
            data and
            prior_data and
            recorder_interactor.last_from_stream and
            not replacement_writer.is_reset(prior_data)
        ):
            # reset the output
            replacement_writer.reset()
        # write and record the non-stream output
        output = replacement_writer.write(data)
        recorder_interactor.record(data, from_stream=False)
        return output

    setattr(parent, func_name, wrapped)
