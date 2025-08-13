import pytest

from money_metrics.core.data_manager import DataManager


def test_add_and_get_dataset():
    manager = DataManager()
    data = [1, 2, 3]
    manager.add_dataset("prices", data)
    assert manager.get_dataset("prices") == data
    assert manager.get_dataset("unknown") is None


def test_remove_dataset():
    manager = DataManager()
    manager.add_dataset("prices", [1, 2, 3])
    manager.remove_dataset("prices")
    assert manager.get_dataset("prices") is None
    # Removing again should not raise an error
    manager.remove_dataset("prices")


def test_add_dataset_duplicate_name_raises():
    manager = DataManager()
    manager.add_dataset("prices", [1, 2, 3])
    with pytest.raises(ValueError):
        manager.add_dataset("prices", [4, 5, 6])
