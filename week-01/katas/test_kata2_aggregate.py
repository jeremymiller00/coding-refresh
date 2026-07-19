from kata2_aggregate import top_categories, total_by_category

ROWS = [
    {"category": "books", "amount": "12.50"},
    {"category": "food", "amount": "3"},
    {"category": "books", "amount": "7.25"},
    {"category": "travel", "amount": "100"},
]


def test_total_by_category():
    totals = total_by_category(ROWS)
    assert totals == {"books": 19.75, "food": 3.0, "travel": 100.0}


def test_total_empty():
    assert total_by_category([]) == {}


def test_top_categories_orders_by_total_desc():
    assert top_categories(ROWS, 2) == [("travel", 100.0), ("books", 19.75)]


def test_top_categories_tie_breaks_by_name():
    rows = [
        {"category": "beta", "amount": "5"},
        {"category": "alpha", "amount": "5"},
    ]
    assert top_categories(rows, 2) == [("alpha", 5.0), ("beta", 5.0)]


def test_top_categories_respects_n():
    assert len(top_categories(ROWS, 1)) == 1
