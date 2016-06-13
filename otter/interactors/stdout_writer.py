"""stdout interactor."""


# [ Import ]
# [ -Python ]
import sys
# [ -Project ]
from . import output


# [ Public ]
def get_outputter():
    """return the output interactor."""
    return output.Output(sys.stdout)
