import re
from datetime import datetime
from models import LogEntry

#203.0.113.7 - - [18/Nov/2026:14:02:11 +0000] "GET /api/items?page=2 HTTP/1.1" 200 5123 "https://example.com/" "Mozilla/5.0 (X11; Linux x86_64)"

"""
Parse each line with a compiled regular expression into a LogEntry dataclass with typed 
fields (ip: str, timestamp: datetime with time zone, method: str, 
path: str, status: int, size: int, referrer: str 
| None, user_agent: str | None).
"""

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+|-) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)


def parse(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    
    d = match.groupdict()
    return LogEntry(
        ip=d['ip'],
        timestamp=datetime.strptime(d['timestamp'], "%d/%b/y:%H:%M:%S %z"),
        method=d['method'],
        path=d['path'],
        status=int(d['status']),
        size=int(d['size']),
        referrer=None if d['referrer'] == "-" else d['referrer'],
        user_agent=None if d['user_agent'] == "-" else d['user_agent']
    )