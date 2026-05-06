from project import parse_perLine
from project import parsing
from project import analyzer


def test_parse_perLine():
    assert parse_perLine('2026-02-18 09:06:45 INFO user=12 action=logout') == ["2026-02-18", "09:06:45", "INFO", "12", None, "logout", None]
    assert parse_perLine('2026-02-18 09:12:19 WARNING user=15 msg="Disk almost full"') == ["2026-02-18", "09:12:19", "WARNING", "15", None, None, '"Disk almost full"']
    assert parse_perLine('2026-02-18 09:25:30 INFO user=15 action=logout') == ["2026-02-18", "09:25:30", "INFO", "15", None, "logout", None]
    assert parse_perLine('2026-02-18 09:17:25 WARNING user=22 msg="High memory usage"') == ["2026-02-18", "09:17:25", "WARNING", "22", None, None, '"High memory usage"']

    assert parse_perLine('2026-02-18 09:30:00 DEBUG user=12 action=login') is None
    assert parse_perLine('# Invalid lines below') is None
    assert parse_perLine('random text not matching format') is None
    assert parse_perLine('2026-02-18 09:32:55 INFO action=login') is None


def test_parsing():
    result1 = list(parsing("sample.log"))
    assert len(result1) == 31
    assert result1[0]["level"] == "INFO"
    assert result1[0]["user"] == "12"
    assert result1[0]["action"] == "login"
    assert result1[-1]["level"] == "ERROR"
    assert result1[-1]["code"] == "503"
    assert result1[-1]["msg"] == '"Service unavailable"'


def test_analyzer():
    result2 = analyzer(parsing("sample.log"))
    required = {"no_E", "no_W", "no_I", "error_msgs", "warning_msgs", "no_users"}
    assert required.issubset(result2.keys())
    assert result2["no_E"] == 9
    assert result2["no_W"] == 6
    assert result2["no_I"] == 16
    assert len(result2["error_msgs"]) == 3
    assert len(result2["warning_msgs"]) == 4
    assert result2["no_users"]["12"] == 5
