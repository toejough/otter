"""Semantic actions, core to the library."""


class Writer:
    """Write from a stream or interruption."""

    def __init__(self, *, recorder_interactor):
        """init the state."""
        # set up the interactors
        self._recorder = recorder_interactor

    def write_stream(self, prior_stream_data, data):
        """
        Write data from a stream.

        Takes the prior stream data, the new data, and write/record interactors.

        Returns the return from the write_interactor.
        """
        # if the last recorded output matches
        if self._recorder.last_output_matches(prior_stream_data):
            # just write the new data
            output = {
                'to write': data,
                'to record': data,
                'from stream': True,
                'do reset': False,
            }
        # else, as long as there's new data to write,
        # reset the writer & write the whole stream
        elif data:
            output = {
                'to write': prior_stream_data + data,
                'to record': prior_stream_data + data,
                'from stream': True,
                'do reset': True,
            }
        # return what the writer returned
        return output

    def write_interruption(self, data):
        """interruption writer."""
        # if stream data was printed last and there is new data to print
        output = {
            'to write': data,
            'to record': data,
            'from stream': False,
            'do reset': data and self._recorder.last_from_stream
        }
        return output
