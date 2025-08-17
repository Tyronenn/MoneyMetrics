from money_metrics.core.profile import AppProfile


def test_profile_round_trip(tmp_path):
    profile = AppProfile(
        datasets={"numbers": [1, 2, 3]},
        screens=[{"title": "Graph 1", "dataset": "numbers"}],
    )
    path = tmp_path / "profile.json"
    profile.save_to_file(path)
    loaded = AppProfile.load_from_file(path)

    assert loaded.datasets == profile.datasets
    assert loaded.screens == profile.screens
