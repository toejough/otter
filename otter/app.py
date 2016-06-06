"""Semantic actions, core to the library."""


class Writer:
    """Write from a stream or interruption."""

    def __init__(self, *, write_interactor, recorder_interactor):
        """init the state."""
        # set up the interactors
        self._recorder = recorder_interactor
        self._writer = write_interactor

    def _write(self, data, *, from_stream=False):
        """write & record the given data."""
        output = self._writer.write(data)
        self._recorder.record(data, from_stream=from_stream)
        return output

    def _reset(self):
        """reset the output state so that a new stream is obviously new."""
        if not self._recorder.is_reset():
            self._writer.reset()
            self._recorder.record_reset()

    def write_stream(self, prior_stream_data, data):
        """
        Write data from a stream.

        Takes the prior stream data, the new data, and write/record interactors.

        Returns the return from the write_interactor.
        """
        # if the last recorded output matches
        if self._recorder.last_output_matches(prior_stream_data):
            # just write the new data
            output = self._write(data, from_stream=True)
        # else, as long as there's new data to write,
        # reset the writer & write the whole stream
        elif data:
            self._reset()
            # write the old data, then the new data
            output = self._write(prior_stream_data + data, from_stream=True)
        # return what the writer returned
        return output

    def write_interruption(self, data):
        """interruption writer."""
        # if stream data was printed last and there is new data to print
        if data and self._recorder.last_from_stream:
            # reset the output
            self._reset()
        # write and record the non-stream output
        return self._write(data, from_stream=False)
