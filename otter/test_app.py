"""application-level test cases."""


# [ Imports ]
# [ -Python ]
import sys
from unittest import TestCase
# [ -Project ]
from . import use_cases
from . import app


# [ Global ]
T = TestCase()
# disable protected-access warnings for tests.
# pylint: disable=protected-access


"""
manage application state:

* write function - default to stdout for streams,
   when stream is created without writer, it's stdout
   when stream is created with writer, it's the specified writer
   when stream.write is called, it calls the writer
  - is passed in for wrapped writers
   when wrapped is called, it calls the writer
* input data - passed in
* prior data - saved in stream
    when stream is created, it has a prior_data field
    when stream data is written, it is appended ot the prior data field
* line contents - saved in line tracker
    when stream.write is called, it calls the line tracker with its final line
    when wrapped is called, it calls the line tracker with its final line
* last writer - saved in write tracker
    when stream.write is called, it calls the write tracker to indicate a stream
    when wrapped is called, it calls the write tracker to indicate a non-stream

manage application entities:

* wrapper - wraps and tracks writers + handles non-stream writes
    when wrapper is called with a writer, wraps the writer
    when wrapper is called with a wrapped writer, wraps the writer
* wrapped
    wrapped includes attribute with original writer
    triggers the correct use cases
    when called with empty string, noop

* stream - tracks stream data + handles stream writes
    when stream is called with a wrapped writer, uses the writer
    triggers the correct use cases
    when called with empty string, noop
* line tracker - tracks and supplies the last line
    when line updated and retrieved, it's the last update
    when line updated several times, then retrieved, it's the last update
    when just retrieved and no line written, it's empty
* write tracker - tracks and supplies the last writer
    when write updated and retrieved, it's the last update
    when write updated selveral times, and retrieved, it's the last update
    when just retrieved and no write, it's 'stream'
    probably track "was stream" boolean state
"""


# [ Tests ]
def test_stream_default_write_func():
    """test."""
    # Given
    default_write_func = sys.stdout.write

    # When
    stream = app.Stream()

    # Then
    T.assertEqual(stream._writer, default_write_func)


def test_stream_given_write_func():
    """test."""
    # Given
    def given_write_func(x):
        """test func."""
        return x

    # When
    stream = app.Stream(given_write_func)

    # Then
    T.assertEqual(stream._writer, given_write_func)


def test_stream_write_calls_write_func():
    """test."""
    # Given
    called = False

    def tracking_write_func(x):
        """test func which tracks call."""
        nonlocal called
        called = True

    stream = app.Stream(tracking_write_func)

    # When
    stream.write("something")

    # Then
    T.assertTrue(called)


def test_stream_write_calls_wrapped_write_func():
    """test."""
    # Given
    wrapped_called = False
    raw_called = False

    def tracking_write_func(x):
        """test func which tracks call."""
        nonlocal raw_called
        raw_called = True

    def wrapped(x):
        """test func which tracks call."""
        nonlocal wrapped_called
        wrapped_called = True
    wrapped.writer = tracking_write_func

    stream = app.Stream(wrapped)

    # When
    stream.write('something')

    # Then
    T.assertTrue(raw_called)
    T.assertFalse(wrapped_called)


def test_prior_data_field():
    """test."""
    # Given
    stream = app.Stream(lambda x: x)
    data = 'should be stored in prior data'

    # When
    stream.write(data)

    # Then
    T.assertTrue(stream._prior_data.endswith(data))


def test_append_to_prior_data_field():
    """test."""
    # Given
    stream = app.Stream(lambda x: x)
    prior_data = 'should be stored in prior data'
    data = ' and so should this.'
    stream.write(prior_data)

    # When
    stream.write(data)

    # Then
    T.assertEqual(prior_data + data, stream._prior_data)


def test_stream_uses_default_line_tracker():
    """
    test application state.

    stream writes to default line tracker if none supplied.
    """
    # Given
    default_line_tracker = app.DEFAULT_LINE_TRACKER

    # When
    stream = app.Stream()

    # Then
    T.assertEqual(stream._line_tracker, default_line_tracker)


def test_stream_uses_given_line_tracker():
    """
    test application state.

    stream writes to given line tracker if supplied.
    """
    # Given
    given_line_tracker = object()

    # When
    stream = app.Stream(line_tracker=given_line_tracker)

    # Then
    T.assertEqual(stream._line_tracker, given_line_tracker)


def test_line_tracker_tracks_final_line():
    """test."""
    # Given
    line_tracker = app.DEFAULT_LINE_TRACKER

    # When
    for text, final_line in (
        ['foo', 'foo'],
        ['hey\n', ''],
        ['hey\nthere', 'there'],
    ):
        line_tracker.update(text)

        # Then
        T.assertEqual(line_tracker.last_line, final_line)


def test_stream_writes_to_line_tracker():
    """
    test application state.

    Line contents - saved in line tracker:
    When stream.write is called, it calls the line tracker's update function.
    """
    # Given
    data = 'some data\non multiple lines\n'

    class TestTracker:
        """test tracker."""

        def __init__(self):
            """init state."""
            self.called_with = None
            self.last_line = ''

        def update(self, data):
            """update."""
            self.called_with = data

    tracker = TestTracker()
    stream = app.Stream(lambda x: x, line_tracker=tracker)

    # When
    stream.write(data)

    # Then
    T.assertEqual(tracker.called_with, data)


def test_wrapper_wraps_writer():
    """
    test.

    when wrapper is called with a writer, wraps the writer.
    """
    # Given
    written_data = ''
    example_data = 'some data'

    def writer(data):
        """test writer."""
        nonlocal written_data
        written_data = data
    wrapped = app.Wrapped(writer)

    # When
    wrapped(example_data)

    # Then
    T.assertTrue(written_data.endswith(example_data))


def test_wrapped_has_original_attribute():
    """
    test.

    wrapped includes attribute with original writer
    """
    # Given
    def writer(data):
        """test writer."""
        pass

    # When
    wrapped = app.Wrapped(writer)

    # Then
    T.assertEqual(wrapped.writer, writer)


def test_wrapping_wrapped_writer():
    """
    test.

    wrapped wrapped writer is just the wrapped writer.
    """
    # Given
    def writer(data):
        """test writer."""
        pass
    wrapped = app.Wrapped(writer)

    # When
    wrapped_wrapped = app.Wrapped(wrapped)

    # Then
    T.assertEqual(wrapped_wrapped.writer, writer)


def test_wrapped_does_not_call_on_empty_string():
    """test."""
    # Given
    called = False

    def writer(data):
        """test writer."""
        nonlocal called
        called = True
    wrapped = app.Wrapped(writer)

    # When
    wrapped('')

    # Then
    T.assertFalse(called)


def test_wrapped_triggers_use_cases():
    """test."""
    # Given
    # the use cases
    non_stream_at_new_line_called = False
    non_stream_mid_stream_called = False
    non_stream_mid_line_called = False

    def non_stream_at_new_line(write, data):
        """test use case."""
        nonlocal non_stream_at_new_line_called
        non_stream_at_new_line_called = True

    def non_stream_mid_stream(write, data):
        """test use case."""
        nonlocal non_stream_mid_stream_called
        non_stream_mid_stream_called = True

    def non_stream_mid_line(write, data):
        """test use case."""
        nonlocal non_stream_mid_line_called
        non_stream_mid_line_called = True

    line_tracker = app.Namespace()
    source_tracker = app.Namespace()

    wrapped = app.Wrapped(
        None,
        write_non_stream_at_new_line=non_stream_at_new_line,
        write_non_stream_mid_stream=non_stream_mid_stream,
        write_non_stream_mid_line=non_stream_mid_line,
        line_tracker=line_tracker,
        source_tracker=source_tracker
    )

    # When
    # Then
    T.assertEqual(wrapped.write_non_stream_at_new_line, non_stream_at_new_line)
    T.assertEqual(wrapped.write_non_stream_mid_line, non_stream_mid_line)
    T.assertEqual(wrapped.write_non_stream_mid_stream, non_stream_mid_stream)

    # When
    # the wrapped is called
    non_stream_at_new_line_called = False
    non_stream_mid_stream_called = False
    non_stream_mid_line_called = False
    line_tracker.last_line = ''
    source_tracker.stream_wrote_last = False
    wrapped('foo')

    # Then
    # the appropriate use case is called
    T.assertTrue(non_stream_at_new_line_called)
    T.assertFalse(non_stream_mid_stream_called)
    T.assertFalse(non_stream_mid_line_called)

    # When
    # the wrapped is called
    non_stream_at_new_line_called = False
    non_stream_mid_stream_called = False
    non_stream_mid_line_called = False
    line_tracker.last_line = ''
    source_tracker.stream_wrote_last = True
    wrapped('foo')

    # Then
    # the appropriate use case is called
    T.assertTrue(non_stream_at_new_line_called)
    T.assertFalse(non_stream_mid_stream_called)
    T.assertFalse(non_stream_mid_line_called)

    # When
    # the wrapped is called
    non_stream_at_new_line_called = False
    non_stream_mid_stream_called = False
    non_stream_mid_line_called = False
    line_tracker.last_line = 'stuff'
    source_tracker.stream_wrote_last = False
    wrapped('foo')

    # Then
    # the appropriate use case is called
    T.assertFalse(non_stream_at_new_line_called)
    T.assertFalse(non_stream_mid_stream_called)
    T.assertTrue(non_stream_mid_line_called)

    # When
    # the wrapped is called
    non_stream_at_new_line_called = False
    non_stream_mid_stream_called = False
    non_stream_mid_line_called = False
    line_tracker.last_line = 'stuff'
    source_tracker.stream_wrote_last = True
    wrapped('foo')

    # Then
    # the appropriate use case is called
    T.assertFalse(non_stream_at_new_line_called)
    T.assertTrue(non_stream_mid_stream_called)
    T.assertFalse(non_stream_mid_line_called)


def test_wrapped_default_use_cases():
    """test."""
    # Given
    wrapped = app.Wrapped(None)

    # When
    # Then
    T.assertEqual(wrapped.write_non_stream_at_new_line, use_cases.write_non_stream_at_new_line)
    T.assertEqual(wrapped.write_non_stream_mid_line, use_cases.write_non_stream_mid_line)
    T.assertEqual(wrapped.write_non_stream_mid_stream, use_cases.write_non_stream_mid_stream)


def test_non_stream_uses_default_line_tracker():
    """
    test application state.

    non_stream writes to default line tracker if none supplied.
    """
    # Given
    default_line_tracker = app.DEFAULT_LINE_TRACKER

    # When
    wrapped = app.Wrapped(None)

    # Then
    T.assertEqual(wrapped.line_tracker, default_line_tracker)


def test_non_stream_uses_given_line_tracker():
    """
    test application state.

    non_stream writes to given line tracker if supplied.
    """
    # Given
    given_line_tracker = object()

    # When
    wrapped = app.Wrapped(None, line_tracker=given_line_tracker)

    # Then
    T.assertEqual(wrapped.line_tracker, given_line_tracker)


def test_line_tracker_starts_empty():
    """test."""
    # Given
    line_tracker = app.LineTracker()

    # When
    # Then
    T.assertEqual(line_tracker.last_line, '')


def test_non_stream_writes_to_line_tracker():
    """
    test application state.

    Line contents - saved in line tracker:
    When wrapped is called, it calls the line tracker's update function.
    """
    # Given
    data = 'some data\non multiple lines\n'

    class TestTracker:
        """test tracker."""

        def __init__(self):
            """init state."""
            self.called_with = None
            self.last_line = ''

        def update(self, data):
            """update."""
            self.called_with = data

    tracker = TestTracker()
    wrapped = app.Wrapped(lambda x: x, line_tracker=tracker)

    # When
    wrapped(data)

    # Then
    T.assertEqual(tracker.called_with, data)


def test_stream_write_tracking():
    """
    test.

    when stream.write is called, it calls the write tracker to indicate a stream.
    """
    # Given
    # stream & tracker
    source_tracker = app.Namespace()
    source_tracker.stream_wrote_last = False
    stream = app.Stream(writer=lambda x: x, source_tracker=source_tracker)

    # When
    stream.write('something')

    # Then
    T.assertTrue(source_tracker.stream_wrote_last)


def test_non_stream_write_tracking():
    """
    test.

    when non_stream.write is called, it calls the write tracker to indicate a stream.
    """
    # Given
    # stream & tracker
    source_tracker = app.Namespace()
    source_tracker.stream_wrote_last = True
    wrapped = app.Wrapped(writer=lambda x: x, source_tracker=source_tracker)

    # When
    wrapped('something')

    # Then
    T.assertFalse(source_tracker.stream_wrote_last)


def test_stream_use_cases():
    """test."""
    # Given
    # the use cases
    start_new_stream_at_new_line_called = False
    start_new_stream_mid_line_called = False
    continue_stream_from_prior_data_called = False
    continue_stream_from_new_line_called = False
    continue_stream_from_mid_line_called = False

    def start_new_stream_at_new_line(write, data):
        """test use case."""
        nonlocal start_new_stream_at_new_line_called
        start_new_stream_at_new_line_called = True

    def start_new_stream_mid_line(write, data):
        """test use case."""
        nonlocal start_new_stream_mid_line_called
        start_new_stream_mid_line_called = True

    def continue_stream_from_prior_data(write, data):
        """test use case."""
        nonlocal continue_stream_from_prior_data_called
        continue_stream_from_prior_data_called = True

    def continue_stream_from_new_line(write, data, prior_data):
        """test use case."""
        nonlocal continue_stream_from_new_line_called
        continue_stream_from_new_line_called = True

    def continue_stream_from_mid_line(write, data, prior_data):
        """test use case."""
        nonlocal continue_stream_from_mid_line_called
        continue_stream_from_mid_line_called = True

    line_tracker = app.Namespace()
    source_tracker = app.Namespace()
    source_tracker.stream_wrote_last = False

    stream = app.Stream(
        None,
        start_new_stream_at_new_line=start_new_stream_at_new_line,
        start_new_stream_mid_line=start_new_stream_mid_line,
        continue_stream_from_prior_data=continue_stream_from_prior_data,
        continue_stream_from_new_line=continue_stream_from_new_line,
        continue_stream_from_mid_line=continue_stream_from_mid_line,
        line_tracker=line_tracker,
        source_tracker=source_tracker
    )

    # When
    # Then
    T.assertEqual(stream.start_new_stream_at_new_line, start_new_stream_at_new_line)
    T.assertEqual(stream.start_new_stream_mid_line, start_new_stream_mid_line)
    T.assertEqual(stream.continue_stream_from_prior_data, continue_stream_from_prior_data)
    T.assertEqual(stream.continue_stream_from_new_line, continue_stream_from_new_line)
    T.assertEqual(stream.continue_stream_from_mid_line, continue_stream_from_mid_line)

    # When
    # the stream is called
    start_new_stream_at_new_line_called = False
    start_new_stream_mid_line_called = False
    continue_stream_from_prior_data_called = False
    continue_stream_from_new_line_called = False
    continue_stream_from_mid_line_called = False
    line_tracker.last_line = ''
    stream._prior_data = ''
    stream.write('foo')

    # Then
    # the appropriate use case is called
    T.assertTrue(start_new_stream_at_new_line_called)
    T.assertFalse(start_new_stream_mid_line_called)
    T.assertFalse(continue_stream_from_prior_data_called)
    T.assertFalse(continue_stream_from_new_line_called)
    T.assertFalse(continue_stream_from_mid_line_called)

    # When
    # the stream is called
    start_new_stream_at_new_line_called = False
    start_new_stream_mid_line_called = False
    continue_stream_from_prior_data_called = False
    continue_stream_from_new_line_called = False
    continue_stream_from_mid_line_called = False
    line_tracker.last_line = 'something in the line'
    stream._prior_data = ''
    stream.write('foo')

    # Then
    # the appropriate use case is called
    T.assertFalse(start_new_stream_at_new_line_called)
    T.assertTrue(start_new_stream_mid_line_called)
    T.assertFalse(continue_stream_from_prior_data_called)
    T.assertFalse(continue_stream_from_new_line_called)
    T.assertFalse(continue_stream_from_mid_line_called)

    # When
    # the stream is called
    start_new_stream_at_new_line_called = False
    start_new_stream_mid_line_called = False
    continue_stream_from_prior_data_called = False
    continue_stream_from_new_line_called = False
    continue_stream_from_mid_line_called = False
    line_tracker.last_line = 'prior data'
    stream._prior_data = 'prior data'
    stream.write('foo')

    # Then
    # the appropriate use case is called
    T.assertFalse(start_new_stream_at_new_line_called)
    T.assertFalse(start_new_stream_mid_line_called)
    T.assertTrue(continue_stream_from_prior_data_called)
    T.assertFalse(continue_stream_from_new_line_called)
    T.assertFalse(continue_stream_from_mid_line_called)

    # When
    # the stream is called
    start_new_stream_at_new_line_called = False
    start_new_stream_mid_line_called = False
    continue_stream_from_prior_data_called = False
    continue_stream_from_new_line_called = False
    continue_stream_from_mid_line_called = False
    line_tracker.last_line = ''
    stream._prior_data = 'prior data'
    stream.write('foo')

    # Then
    # the appropriate use case is called
    T.assertFalse(start_new_stream_at_new_line_called)
    T.assertFalse(start_new_stream_mid_line_called)
    T.assertFalse(continue_stream_from_prior_data_called)
    T.assertTrue(continue_stream_from_new_line_called)
    T.assertFalse(continue_stream_from_mid_line_called)

    # When
    # the stream is called
    start_new_stream_at_new_line_called = False
    start_new_stream_mid_line_called = False
    continue_stream_from_prior_data_called = False
    continue_stream_from_new_line_called = False
    continue_stream_from_mid_line_called = False
    line_tracker.last_line = 'some other text'
    stream._prior_data = 'prior data'
    stream.write('foo')

    # Then
    # the appropriate use case is called
    T.assertFalse(start_new_stream_at_new_line_called)
    T.assertFalse(start_new_stream_mid_line_called)
    T.assertFalse(continue_stream_from_prior_data_called)
    T.assertFalse(continue_stream_from_new_line_called)
    T.assertTrue(continue_stream_from_mid_line_called)


def test_stream_does_not_call_on_empty_string():
    """test."""
    # Given
    called = False

    def writer(data):
        """test writer."""
        nonlocal called
        called = True
    stream = app.Stream(writer=writer)

    # When
    stream.write('')

    # Then
    T.assertFalse(called)


def test_stream_default_use_cases():
    """test."""
    # Given
    stream = app.Stream()

    # When
    # Then
    T.assertEqual(stream.start_new_stream_at_new_line, use_cases.start_new_stream_at_new_line)
    T.assertEqual(stream.start_new_stream_mid_line, use_cases.start_new_stream_mid_line)
    T.assertEqual(stream.continue_stream_from_prior_data, use_cases.continue_stream_from_prior_data)
    T.assertEqual(stream.continue_stream_from_new_line, use_cases.continue_stream_from_new_line)
    T.assertEqual(stream.continue_stream_from_mid_line, use_cases.continue_stream_from_mid_line)


# pylint: enable=protected-access
