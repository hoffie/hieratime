import re
from .base_node import BaseNode
from .format import indent

LEVELCHAR = '*'
HEADING_RE = re.compile(r'^(?P<level>' + re.escape(LEVELCHAR) + r'+)\s*'
    '(?P<heading>.*?)(\s+:(?P<tags>[^:]+):)?\s*$')


def is_text(line):
    return not HEADING_RE.match(line)


class Node(BaseNode):
    parent = None

    def __init__(self, level=0, heading="", tags=None, lineidx=None):
        self.children = []
        self.tags = tags or []
        self.clocks = []
        self.level = level
        self.heading = heading
        self.lineidx = lineidx

    @classmethod
    def from_line(cls, line, lineidx):
        m = HEADING_RE.match(line)
        level = len(m.group("level"))
        heading = m.group("heading")
        tags = []
        if m.group("tags"):
            tags = m.group("tags").split(',')
        return cls(level=level, heading=heading, tags=tags, lineidx=lineidx)

    def __str__(self):
        ret = []
        if self.level:
            ret.append(self.level * LEVELCHAR + ' ' + self.heading)
        if self.tags:
            ret.append(' :' + ','.join(self.tags) + ':')
        if ret:
            ret.append('\n')
        for clock in self.clocks:
            ret.append(indent(self.level + 1, str(clock)))
        ret += [str(node) for node in self.children]
        return "".join(ret)

    def node_by_line(self, lineidx):
        todo = [self]
        best_node = None
        best_distance = None
        while todo:
            cur = todo.pop(0)
            if cur.children:
                todo += cur.children

            if not cur.lineidx:
                continue

            distance = lineidx - cur.lineidx
            if distance == 0:
                # won't get any better :)
                return cur
            if distance > 0 and (not best_distance or distance < best_distance):
                # area after a heading; and we are better than any previous
                # matches
                best_distance = distance
                best_node = cur

        return best_node

    def get_running_clock(self):
        todo = [self]
        while todo:
            cur = todo.pop(0)
            for clock in cur.clocks:
                if not clock.end:
                    return clock
            if cur.children:
                todo += cur.children
        raise Exception("unable to find a running clock")
