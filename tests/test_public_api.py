from money_metrics import FourZeroOneK, DataManager, AppProfile


def test_import_and_use_public_api(tmp_path):
    plan = FourZeroOneK()
    plan.add_month(100, 0.01)
    dm = DataManager()
    dm.add_dataset("401k", plan.to_dict())
    profile = AppProfile(datasets=dm.all_datasets())
    path = tmp_path / "profile.json"
    profile.save_to_file(path)
    loaded = AppProfile.load_from_file(path)
    assert "401k" in loaded.datasets
