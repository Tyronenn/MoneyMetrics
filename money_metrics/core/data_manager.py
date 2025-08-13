class DataManager:
    """Simple in-memory data storage for graphing datasets.

    This class keeps the graph data separate from the UI components. Graph
    screens can query datasets by name when the user chooses to attach data to
    a graph.
    """

    def __init__(self):
        self._datasets = {}

    def add_dataset(self, name, data):
        """Store a dataset under a given name."""
        self._datasets[name] = data

    def remove_dataset(self, name):
        """Remove a dataset if it exists."""
        self._datasets.pop(name, None)

    def get_dataset(self, name):
        """Retrieve a dataset by name.

        Returns ``None`` if the dataset is unknown.
        """
        return self._datasets.get(name)
