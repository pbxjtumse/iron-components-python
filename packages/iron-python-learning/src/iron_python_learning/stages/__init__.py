from __future__ import annotations

from importlib import import_module
from typing import Any

_STAGE_MODULES = {
    1: "stage_01_basics",
    2: "stage_02_object_model",
    3: "stage_03_type_system",
    4: "stage_04_functions_modules",
    5: "stage_05_oop_dataclass",
    6: "stage_06_collections_iterators",
    7: "stage_07_errors_context",
    8: "stage_08_io_serialization",
    9: "stage_09_concurrency_async",
    10: "stage_10_component_project",
}


def run_stage(number: int) -> dict[str, Any]:
    module_name = _STAGE_MODULES.get(number)
    if module_name is None:
        raise ValueError(f"Unknown stage: {number}")

    module = import_module(f"iron_python_learning.stages.{module_name}")
    return module.demo()


def run_all() -> dict[str, dict[str, Any]]:
    return {f"stage_{number:02d}": run_stage(number) for number in sorted(_STAGE_MODULES)}


__all__ = ["run_all", "run_stage"]
