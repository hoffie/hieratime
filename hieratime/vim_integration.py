import sys
import vim
from difflib import SequenceMatcher
from .parser import parse_lines, CHARSET
from .clock import Clock
from .node import NoRunningClockError


def refresh():
    new = parse_lines(vim.current.buffer[:])
    update(new)
    msg("refreshed")


def clock_in():
    tree = get_tree()
    try_clock_out(tree)
    node = node_under_cursor(tree)
    if not node:
        error("unable to map current line to node")
        return
    node.clocks.insert(0, Clock())
    root = node.get_root()
    update(root)
    msg("clocked in")

def try_clock_out(tree=None):
    tree = tree or get_tree()
    try:
        clock = tree.get_running_clock()
    except NoRunningClockError:
        return
    clock.finish()


def clock_out():
    tree = get_tree()
    try:
        clock = tree.get_running_clock()
    except NoRunningClockError as e:
        error(e)
        return
    clock.finish()
    root = clock.get_root()
    update(root)
    vim.current.window.cursor = (clock.lineidx, 999)
    msg("clocked out")


def node_under_cursor(tree=None):
    tree = tree or get_tree()
    lineidx = vim.current.window.cursor[0]
    return tree.node_by_line(lineidx)


def update(new):
    new = unicode(new).encode(CHARSET).split('\n')
    diff = SequenceMatcher(a=vim.current.buffer, b=new)
    offset = 0
    for action, i1, i2, j1, j2 in diff.get_opcodes():
        if action == 'replace':
            vim.current.buffer[i1 + offset:i2 + offset] = new[j1:j2]
            offset -= i2 - i1 - (j2 - j1)
        elif action == 'insert':
            vim.current.buffer[i1 + offset:i2 + offset] = new[j1:j2]
            offset += j2 - j1
        elif action == 'delete':
            del vim.current.buffer[i1 + offset:i2 + offset]
            offset -= i2 - i1


def get_tree():
    return parse_lines(vim.current.buffer[:])


def msg(msg):
    sys.stdout.write("hiera: " + msg + "\n")


def error(msg):
    sys.stderr.write("hiera: " + str(msg) + "\n")
