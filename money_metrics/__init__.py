"""MoneyMetrics package.

This top-level package re-exports the core classes so that users can
conveniently access them via ``import money_metrics``. Previously, the
core utilities such as :class:`~money_metrics.core.FourZeroOneK` were only
available through the :mod:`money_metrics.core` submodule, which made it
awkward for callers to build 401(k) datasets. By exposing the classes here
we provide a simpler interface for consumers of the library.
"""

from .core import DataManager, AppProfile, FourZeroOneK, Entry

__all__ = ["DataManager", "AppProfile", "FourZeroOneK", "Entry"]
