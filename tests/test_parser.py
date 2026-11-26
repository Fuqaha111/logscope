from datetime import timezone
from logscope.parser import parse

line = '203.0.113.7 - - [18/Nov/2026:14:02:11 +0000] "GET /api/items?page=2 HTTP/1.1" 200 5123 "https://example.com/" "Mozilla/5.0 (X11; Linux x86_64)"'


def test_parse_fields():
    e = parse(line)
    assert e.ip == "203.0.113.7"
    assert e.method == "GET"
    assert e.path == "/api/items?page=2"


def test_status_size_are_ints():
    e = parse(line)
    assert e.size == 5123 and isinstance(e.size, int)
    assert e.status == 200 and isinstance(e.status, int)
    

def test_faulty_inputs():
    e = parse("This is a false input")
    assert e == None