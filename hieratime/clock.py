import re
from math import floor
from datetime import datetime
from dateutil.parser import parse as parse_datetime
from .base_node import BaseNode

CLOCK_RE = re.compile(r'^CLOCK:\s*\[(?P<start>[^\]]+)\](?:--(?:\[(?P<end>[^\]]+)])?.*)?')
DATETIME_FORMAT = '[%Y-%m-%d %a %H:%M]'


def is_clock(line):
    return CLOCK_RE.match(line)


def format_duration(d):
    sec = d.total_seconds()
    total_mins = floor(sec/60.)
    total_hours = floor(total_mins/60.)
    mins = total_mins % 60
    return '%d:%02d' % (total_hours, mins)


class Clock(BaseNode):
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
