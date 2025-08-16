import copy


class DataManager:
    """Simple in-memory data storage for graphing datasets.

    This class keeps the graph data separate from the UI components. Graph
    screens can query datasets by name when the user chooses to attach data to
    a graph.  The manager defends its internal state by storing and returning
    copies of datasets so that callers cannot accidentally mutate what is
    stored.
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

        Notes
        -----
        A deep copy of ``data`` is stored to prevent external modification of
        the internal dataset after it has been added.
        """
        if not replace and name in self._datasets:
            raise ValueError(f"Dataset '{name}' already exists")
        # Store a copy so future modifications to the original object do not
        # alter the stored dataset.
        self._datasets[name] = copy.deepcopy(data)

    def remove_dataset(self, name):
        """Remove a dataset if it exists."""
        self._datasets.pop(name, None)

    def get_dataset(self, name):
        """Retrieve a dataset by name.

        Returns
        -------
        Any or ``None``
            A deep copy of the dataset or ``None`` if the dataset is unknown.
        """
        data = self._datasets.get(name)
        return None if data is None else copy.deepcopy(data)
