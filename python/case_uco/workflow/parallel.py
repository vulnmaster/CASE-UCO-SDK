"""Optional process-per-partition scheduler.

Process-pool parallelism is specified and **off by default**. The sequential
engine in ``engine.py`` is the 2.0.1 path. A 2.1 increment may call
:func:`run_partitions` with ``enabled=True``.
"""

from __future__ import annotations

from typing import Any, Callable


def run_partitions(
    items_by_key: dict[str, list[dict[str, Any]]],
    worker: Callable[[str, list[dict[str, Any]]], Any],
    *,
    enabled: bool = False,
    max_workers: int | None = None,
) -> dict[str, Any]:
    """Run ``worker(key, items)`` per partition.

    When ``enabled`` is false (default) this is a sequential loop. Live
    ``ProcessPoolExecutor`` is 2.1 and must stay opt-in.
    """
    if not enabled:
        return {key: worker(key, items) for key, items in items_by_key.items()}
    # 2.1: ProcessPoolExecutor. Parent merges state only. Not wired to engine.run().
    raise NotImplementedError(
        "Process-per-partition is a 2.1 opt-in. Sequential run_partitions(enabled=False) is the 2.0.1 path."
    )
