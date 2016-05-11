import otter
import sys

write = sys.stdout.write
def instant_flush(data):
    write(data)
    sys.stdout.flush()
sys.stdout.write = otter.Wrapped(instant_flush)
sys.stderr.write = otter.Wrapped(sys.stderr.write)

s1 = otter.Stream(writer=instant_flush)
s2 = otter.Stream(writer=instant_flush)
s3 = otter.Stream(writer=instant_flush)

s1.write('starting s1...')
s1.write('finishing s1.')

s2.write('starting s2')
print('hi there! ')
print('I am an interruptor.')
s2.write('...continuing s2...')

s3.write('staring s3...')
print('a non-ending interruption', end='')
print(' and another', end='')
s2.write('finishing s2')
s3.write('continuing s3...')
sys.stderr.write("err interruption")
s3.write('finishing s3')
