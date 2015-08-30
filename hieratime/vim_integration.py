import sys
import vim
from .parser import parse_lines
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
    new_s = str(new)
    if '\n'.join(vim.current.buffer) != new_s:
        vim.current.buffer[:] = new_s.split('\n')


def get_tree():
    return parse_lines(vim.current.buffer[:])


def msg(msg):
    sys.stdout.write("hiera: " + msg + "\n")


def error(msg):
    sys.stderr.write("hiera: " + msg + "\n")
