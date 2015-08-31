from .clock import is_clock, Clock
from .node import is_text, Node


CHARSET = 'utf-8'


def parse_lines(lines):
    root = Node()
    cur = root
    lineidx = 0
    for line in lines:
        lineidx += 1
        line = line.strip().decode(CHARSET)
        if not line:
            continue
        if is_clock(line):
            clock = Clock.from_line(line, lineidx=lineidx)
            clock.parent = cur
            cur.clocks.append(clock)
            continue
        if is_text(line):
            if not cur.clocks:
                raise Exception("discarding text in line %d: %s" % (lineidx+1, line))
            cur.clocks[-1].notes.append(line.strip())
            continue
        node = Node.from_line(line, lineidx=lineidx)
        while node.level != cur.level + 1:
            cur = cur.parent
        node.parent = cur
        node.parent.children.append(node)
        cur = node
    return root
