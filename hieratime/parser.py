from .clock import is_clock, Clock
from .node import is_text, Node


def parse_lines(lines):
    root = Node()
    cur = root
    lineidx = 0
    for line in lines:
        lineidx += 1
        line = line.strip()
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
        for _ in range(cur.level - node.level):
            cur = cur.parent
        cur.children.append(node)
        node.parent = cur
        cur = node
    return root
