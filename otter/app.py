"""The How of the application."""


from .components import writer, recorder
from .interactors import stdout_writer


def get_recorded_output():
    """return the remembered data."""
    return recorder.output_record


def write(data, *, write_interactor=stdout_writer):
    """write the given data."""
    writer.write(data, write_interactor=write_interactor)
    recorder.record(data, from_stream=True)


def reset(*, write_interactor=stdout_writer):
    """reset the output state so that a new stream is obviously new."""
    writer.reset(write_interactor=write_interactor)


def replace(parent, func_name, replacement_writer):
    """watch the output from the function."""
    def wrapped(data):
        """wrapped interruption writer."""
        if data:
            return write_interruption(data, replacement_writer)

    setattr(parent, func_name, wrapped)


def write_interruption(data, interruption_writer):
    """write interruption."""
    prior_data = recorder.output_record
    if recorder.last_from_stream and prior_data and not interruption_writer.is_reset(prior_data):
        interruption_writer.reset()
    output = interruption_writer.write(data)
    recorder.record(data, from_stream=False)
    return output


def is_reset(*, write_interactor=stdout_writer):
    """return whether the output source is already reset."""
    return writer.is_reset(
        recorder.output_record,
        write_interactor=write_interactor
    )
