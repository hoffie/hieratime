import sys
import vim
from .parser import parse_lines
from .clock import Clock


def vim_refresh():
    new = parse_lines(vim.current.buffer[:])
    vim_update(new)
    msg("hiera refreshed")


def vim_clock_in():
    node = vim_node_under_cursor()
    if not node:
        sys.stderr.write("hiera: unable to map current line to node\n")
        return
    node.clocks.insert(0, Clock())
    root = node.get_root()
    vim_update(root)
    msg("hiera: clocked in")


def vim_clock_out():
    tree = vim_get_tree()
    try:
        clock = tree.get_running_clock()
    except Exception as e:
        error(e)
        return
    clock.finish()
    root = clock.get_root()
    vim_update(root)
    vim.current.window.cursor = (clock.lineidx, 999)
    msg("hiera: clocked out")


def vim_node_under_cursor():
    tree = vim_get_tree()
    lineidx = vim.current.window.cursor[0]
    return tree.node_by_line(lineidx)


def vim_update(new):
    new_s = str(new)
    if '\n'.join(vim.current.buffer) != new_s:
        vim.current.buffer[:] = new_s.split('\n')


def vim_get_tree():
    return parse_lines(vim.current.buffer[:])


def msg(msg):
    sys.stdout.write("hiera: " + msg + "\n")


def error(msg):
    sys.stderr.write("hiera: " + msg + "\n")
