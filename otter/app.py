"""Semantic actions, core to the library."""


def should_restart_stream(data, last_output_matches):
    """
    Write data from a stream.

    Takes the prior stream data, the new data, and write/record interactors.

    Returns the return from the write_interactor.
    """
    return data and not last_output_matches


def should_reset_before_interruption(data, last_from_stream):
    """interruption writer."""
    # if stream data was printed last and there is new data to print
    return data and last_from_stream
