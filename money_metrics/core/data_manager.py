class DataManager:
    """Simple in-memory data storage for graphing datasets.

    This class keeps the graph data separate from the UI components. Graph
    screens can query datasets by name when the user chooses to attach data to
    a graph.
    """

    def __init__(self):
        self._datasets = {}

    def add_dataset(self, name, data, replace=False):
        """Store a dataset under a given name.

        Parameters
        ----------
        name: str
            Identifier for the dataset.
        data: Any
            Data associated with the ``name``.
        replace: bool, optional
            If ``True``, overwrite an existing dataset with the same
            ``name``. If ``False`` (default), attempting to add a
            duplicate will raise :class:`ValueError`.
        """
        if not replace and name in self._datasets:
            raise ValueError(f"Dataset '{name}' already exists")
        self._datasets[name] = data

    def remove_dataset(self, name):
        """Remove a dataset if it exists."""
        self._datasets.pop(name, None)

    def get_dataset(self, name):
        """Retrieve a dataset by name.

        Returns ``None`` if the dataset is unknown.
        """
        return self._datasets.get(name)
