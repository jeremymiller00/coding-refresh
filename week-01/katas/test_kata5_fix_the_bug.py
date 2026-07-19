from kata5_fix_the_bug import collect


def test_independent_calls_do_not_share_state():
    first = collect(1)
    second = collect(2)
    assert first == [1]
    assert second == [2]  # fails while the mutable-default bug is present


def test_caller_supplied_list_is_used():
    bucket: list[int] = []
    result = collect(9, bucket)
    assert result is bucket
    assert bucket == [9]
