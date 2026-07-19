from kata3_cli_summary import summarize


def test_summarize_basic():
    assert summarize([1.0, 2.0, 3.0, 4.0]) == {
        "count": 4,
        "total": 10.0,
        "mean": 2.5,
        "minimum": 1.0,
        "maximum": 4.0,
    }


def test_summarize_single():
    assert summarize([7.0]) == {
        "count": 1,
        "total": 7.0,
        "mean": 7.0,
        "minimum": 7.0,
        "maximum": 7.0,
    }


def test_summarize_empty():
    assert summarize([]) == {
        "count": 0,
        "total": 0,
        "mean": None,
        "minimum": None,
        "maximum": None,
    }
