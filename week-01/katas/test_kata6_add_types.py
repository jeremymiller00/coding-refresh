from kata6_add_types import most_common, word_counts


def test_word_counts():
    assert word_counts("The cat, the hat. The CAT!") == {"the": 3, "cat": 2, "hat": 1}


def test_word_counts_empty():
    assert word_counts("   ") == {}


def test_most_common_orders_by_count_then_name():
    text = "b b a a c"
    assert most_common(text, 2) == [("a", 2), ("b", 2)]


def test_most_common_respects_n():
    assert most_common("a a b c", 1) == [("a", 2)]
