from kata4_recursion import flatten


def test_flat_unchanged():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_nested():
    assert flatten([1, [2, [3, 4], 5], [[6]]]) == [1, 2, 3, 4, 5, 6]


def test_empty_and_empty_nests():
    assert flatten([]) == []
    assert flatten([[], [[]], []]) == []


def test_strings_stay_intact():
    assert flatten(["ab", ["cd", ["ef"]]]) == ["ab", "cd", "ef"]


def test_deeply_nested():
    assert flatten([[[[[1]]]], 2]) == [1, 2]
