"""Semantic actions, core to the library."""


def write_stream(prior_stream_data, data, last_output_matches):
    """
    Write data from a stream.

    Takes the prior stream data, the new data, and write/record interactors.

    Returns the return from the write_interactor.
    """
    # if the last recorded output matches
    if last_output_matches:
        # just write the new data
        output = {
            'data': data,
            'do reset': False,
        }
    # else, as long as there's new data to write,
    # reset the writer & write the whole stream
    elif data:
        output = {
            'data': prior_stream_data + data,
            'do reset': True,
        }
    # return what the writer returned
    return output


def should_reset_before_interruption(data, last_from_stream):
    """interruption writer."""
    # if stream data was printed last and there is new data to print
    return data and last_from_stream
