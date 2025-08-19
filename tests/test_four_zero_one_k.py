import pytest

from money_metrics.core import FourZeroOneK, DataManager, AppProfile


def test_401k_add_modify_delete_and_profile(tmp_path):
    plan = FourZeroOneK()
    plan.add_month(100, 0.01)
    plan.add_month(100, 0.01)

    # balances should compound
    assert plan.entries[0].balance == pytest.approx(101.0)
    assert plan.entries[1].balance == pytest.approx((101.0 + 100) * 1.01)

    plan.modify_month(2, contribution=200)
    assert plan.entries[1].contribution == 200

    plan.delete_month(1)
    assert plan.entries[0].month == 1

    dm = DataManager()
    dm.add_dataset("401k", plan.to_dict())
    profile = AppProfile(datasets=dm.all_datasets())
    path = tmp_path / "profile.json"
    profile.save_to_file(path)
    loaded = AppProfile.load_from_file(path)
    assert "401k" in loaded.datasets
    assert loaded.datasets["401k"] == plan.to_dict()


def test_save_and_load_json(tmp_path):
    plan = FourZeroOneK()
    plan.add_month(100, 0.01)
    path = tmp_path / "401k.json"
    plan.save_to_json(path)
    loaded = FourZeroOneK.load_from_json(path)
    assert loaded.to_dict() == plan.to_dict()

