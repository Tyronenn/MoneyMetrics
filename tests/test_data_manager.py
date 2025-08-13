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

