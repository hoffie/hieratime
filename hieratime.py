import sys
import re
from math import floor
from datetime import datetime
from dateutil.parser import parse as parse_datetime

try:
    import vim
except ImportError:
    # vim will be missing in vim_* function calls, which is ok.
    # this module may be used outside of vim.
    pass

LEVELCHAR = '*'
DATETIME_FORMAT= '[%Y-%m-%d %a %H:%M]'
HEADING_RE = re.compile(r'^(?P<level>' + re.escape(LEVELCHAR) + r'+)\s*'
    '(?P<heading>.*?)(\s+:(?P<tags>[^:]+):)?\s*$')
CLOCK_RE = re.compile(r'^CLOCK:\s*\[(?P<start>[^\]]+)\](?:--(?:\[(?P<end>[^\]]+)])?.*)?')

class Node(object):
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

def indent(level, s):
    ret = []
    for line in s.strip().split('\n'):
        ret.append(level * ' ')
        ret.append(line)
        ret.append('\n')
    return ''.join(ret)


class Clock(object):
    parent = None

    def __init__(self, start=None, end=None, lineidx=None):
        self.start = start or datetime.now()
        self.end = end
        self.notes = []
        self.lineidx = lineidx

    def finish(self):
        self.end = datetime.now()

    @property
    def duration(self):
        if not self.start or not self.end:
            return None
        return self.end - self.start

    @classmethod
    def from_line(cls, line, lineidx=None):
        m = CLOCK_RE.match(line)
        start = (m.group("start"))
        end = (m.group("end"))
        if start:
            start = parse_datetime(m.group("start"), fuzzy=True)
        if end:
            end = parse_datetime(m.group("end"), fuzzy=True)
        return cls(start=start, end=end, lineidx=lineidx)

    def __str__(self):
        if not self.start:
            return ''
        ret = ['CLOCK: ']
        ret.append(self.start.strftime(DATETIME_FORMAT))
        ret.append('--')
        if self.end:
            ret.append(self.end.strftime(DATETIME_FORMAT))
            ret.append(' => ')
            ret.append(format_duration(self.duration))
            ret.append('\n')
        for note in self.notes:
            ret.append(note + '\n')
        return ''.join(ret)

class Text(str): pass

def is_text(line):
    return not HEADING_RE.match(line)

def is_clock(line):
    return CLOCK_RE.match(line)

def format_duration(d):
    sec = d.total_seconds()
    total_mins = floor(sec/60.)
    total_hours = floor(total_mins/60.)
    mins = total_mins % 60
    return '%d:%02d' % (total_hours, mins)

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

def vim_refresh():
    new = parse_lines(vim.current.buffer[:])
    vim_update(new)
    print("hiera refreshed")

def vim_clock_in():
    node = vim_node_under_cursor()
    if not node:
        sys.stderr.write("hiera: unable to map current line to node\n")
        return
    node.clocks.insert(0, Clock())
    root = get_root(node)
    vim_update(root)
    print("hiera: clocked in")

def vim_clock_out():
    tree = vim_get_tree()
    try:
        clock = get_running_clock(tree)
    except Exception as e:
        sys.stderr.write("hiera: %s\n" % e)
        return
    clock.finish()
    root = get_root(clock)
    vim_update(root)
    vim.current.window.cursor = (clock.lineidx, 999)
    print("hiera: clocked out")

def get_root(node):
    root = node
    while root.parent:
        root = root.parent
    return root

def get_running_clock(tree):
    todo = [tree]
    while todo:
        cur = todo.pop(0)
        for clock in cur.clocks:
            if not clock.end:
                return clock
        if tree.children:
            todo += cur.children
    raise Exception("unable to find a running clock")

def vim_update(new):
    new_s = str(new)
    if '\n'.join(vim.current.buffer) != new_s:
        vim.current.buffer[:] = new_s.split('\n')

def vim_get_tree():
    return parse_lines(vim.current.buffer[:])

def vim_node_under_cursor():
    tree = vim_get_tree()
    lineidx = vim.current.window.cursor[0]
    return tree.node_by_line(lineidx)
