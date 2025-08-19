# Financial Component Requirements

The 401(k) implementation establishes behaviour that future financial
components (HSAs, brokerage accounts, home values, vehicles, savings accounts,
bonds, stocks, crypto currencies, etc.) should follow:

1. **Persistent storage** – user supplied data is stored in a local JSON file
   as soon as it is created.
2. **Immediate feedback** – newly created datasets are shown on screen in a
   tabular view without additional user interaction.
3. **Drag and drop graphing** – parameters can be graphed by dragging a table
   column onto the plot. Dropping the same column again removes it.
4. **Interactive tables** – tables support scrolling, column reordering,
   in-place editing of values and column renaming.
5. **Dynamic updates** – any change made by the user is reflected instantly in
   both the table and related graphs.
6. **Shareable profiles** – the entire application state, including datasets
   and screen configuration, can be saved to a profile JSON file and reloaded
   later.
7. **Automated tests** – pytest tests cover these behaviours to guard against
   regressions.

These guidelines ensure consistency across all future financial datasets
supported by MoneyMetrics.
