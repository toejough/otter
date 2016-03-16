"""testing otter out."""


import otter
import sys


otter.use_stds()

stream = otter.DefaultStream()
print('hey', end='')
stream.write('starting... ending at once\n')
stream = otter.DefaultStream()
stream.write('starting ... ')
print('interruption')
stream.write(' ending later')
stream.write(' and later.\nNew midstream ...')
print('interruption')
print('second interruption', end='')
print('third interruption', end='')
stream.write(' and finish\n')

stream = otter.DefaultStream()
print('non interruption', end='')
stream.write('starting another ... ')
stream2 = otter.DefaultStream()
stream2.write('starting the second one ... ')
stream3 = otter.DefaultStream()
stream3.write('starting the third one ... ')
stream.write('done.')
stream2.write('done with #2')
print('interruption', end='')
sys.stderr.write("err interruption\n")
stream3.write('done with #3')


stream = otter.DefaultStream()
stream.write('starting ... ')
sys.stderr.write('err interruption')
stream.write(' ending later\n')
