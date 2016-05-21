"""The How of the application."""


from .components import output_watcher, writer


def get_observed_output():
    """return the remembered data."""
    return output_watcher.get_output()


def write(data):
    """write the given data."""
    writer.write(data)
    output_watcher.clear_interruption()


def reset():
    """reset the output state so that a new stream is obviously new."""
    writer.reset()


def watch_output_from(func):
    """watch the output from the function."""
    output_watcher.watch(func)
