
"""
0123456789
^^^^^^^^^^
"""

def safe_get(iterable_, index, default=' '):
    if 0 < index < len(iterable_):
        return iterable_[index]
    else:
        return default

test_str = '0123456789'

camera = -9
maxwidth = 15


line = []
for i in range(maxwidth):
    line.append(safe_get(test_str, i+camera))

print('|' + ''.join(line) + '|')

