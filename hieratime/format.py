def indent(level, s):
    ret = []
    for line in s.strip().split('\n'):
        ret.append(level * ' ')
        ret.append(line)
        ret.append('\n')
    return ''.join(ret)
