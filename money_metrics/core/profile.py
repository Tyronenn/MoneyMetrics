import json
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AppProfile:
    """Serializable representation of a user's application setup.

    The profile stores datasets managed by :class:`DataManager` alongside a
    minimal description of the current graph screens. Profiles can be saved to
    and loaded from JSON files, allowing them to be shared between users or
    re-used later.
    """

    datasets: Dict[str, Any] = field(default_factory=dict)
    screens: List[Dict[str, Any]] = field(default_factory=list)
    version: int = 1

    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "datasets": self.datasets,
            "screens": self.screens,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppProfile":
        version = data.get("version", 1)
        datasets = data.get("datasets", {})
        screens = data.get("screens", [])
        profile = cls(datasets=datasets, screens=screens)
        profile.version = version
        return profile

    # ------------------------------------------------------------------
    def save_to_file(self, path: str) -> None:
        """Write the profile to ``path`` as JSON."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> "AppProfile":
        """Load a profile from ``path``."""
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data)

    # ------------------------------------------------------------------
    @classmethod
    def from_window(cls, window) -> "AppProfile":
        """Create a profile from the current state of a main window."""
        datasets = window.data_manager.all_datasets()
        screens: List[Dict[str, Any]] = []
        for graph in window.graph_screens:
            screens.append({
                "title": graph.windowTitle(),
                "dataset": getattr(graph, "dataset_name", None),
            })
        return cls(datasets=datasets, screens=screens)
