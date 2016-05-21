"""Writer."""


from ..interactors import stdout_writer


def write(data):
    """write the data."""
    stdout_writer.write(data)


def reset():
    """reset the data."""
    stdout_writer.reset()
