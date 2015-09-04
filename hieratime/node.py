import re
from datetime import timedelta
from .base_node import BaseNode
from .format import indent
from .clock import format_duration

LEVELCHAR = '*'
HEADING_RE = re.compile(r'^(?P<level>' + re.escape(LEVELCHAR) + r'+)\s*'
    '(?P<heading>.*?)(\s+:(?P<tags>[^:]+):)?\s*$')
COMMENT_RE = re.compile(r'^\s*#')


def is_autotext(line):
    return COMMENT_RE.match(line)


def is_text(line):
    return not HEADING_RE.match(line)


class NoRunningClockError(Exception): pass


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
        if self.clocks:
            duration = timedelta()
            for clock in self.clocks:
                if clock.end:
                    duration += clock.duration
            ret.append(indent(self.level + 1,
                '# CLOCK-SUMMARY: ' + format_duration(duration)))
        for clock in self.clocks:
            ret.append(indent(self.level + 1, unicode(clock)))
        ret += [unicode(node) for node in self.children]
        return u"".join(ret)

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
        for clock in self.clock_iterator():
            if not clock.end:
                return clock
        raise NoRunningClockError("unable to find a running clock")

    def clock_iterator(self):
        todo = [self]
        while todo:
            cur = todo.pop(0)
            for clock in cur.clocks:
                yield clock
            if cur.children:
                todo += cur.children
