"""Semantic actions, core to the library."""


def should_reset_before_interruption(data, last_from_stream):
    """interruption writer."""
    # if stream data was printed last and there is new data to print
    return data and last_from_stream
