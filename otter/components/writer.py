"""Writer."""


from ..interactors import stdout_writer


def write(data, *, write_interactor=stdout_writer):
    """write the data."""
    write_interactor.write(data)


def reset(*, write_interactor=stdout_writer):
    """reset the data."""
    write_interactor.reset()


def is_reset(prior_data, *, write_interactor=stdout_writer):
    """return whether the prior data indicates a reset was done last."""
    return write_interactor.is_reset(prior_data)
