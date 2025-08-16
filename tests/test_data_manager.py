import pytest

from money_metrics.core import DataManager


def test_add_dataset_duplicate_raises():
    dm = DataManager()
    dm.add_dataset("sample", [1])

    with pytest.raises(ValueError):
        dm.add_dataset("sample", [2])


def test_add_dataset_replace_overwrites():
    dm = DataManager()
    dm.add_dataset("sample", [1])

    dm.add_dataset("sample", [2], replace=True)

    assert dm.get_dataset("sample") == [2]


def test_add_dataset_stores_copy():
    dm = DataManager()
    data = [1, 2, 3]
    dm.add_dataset("numbers", data)
    # mutate original data after adding
    data.append(4)

    # stored dataset should not be affected
    assert dm.get_dataset("numbers") == [1, 2, 3]


def test_get_dataset_returns_copy():
    dm = DataManager()
    dm.add_dataset("numbers", [1, 2, 3])

    retrieved = dm.get_dataset("numbers")
    # mutate retrieved dataset
    retrieved.append(4)

    # internal dataset remains unchanged
    assert dm.get_dataset("numbers") == [1, 2, 3]

