from __future__ import annotations

import sys
from pprint import pprint

from iron_python_learning.stages import run_all, run_stage


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] == "all":
        pprint(run_all(), sort_dicts=False)
        return 0

    try:
        stage_number = int(args[0])
    except ValueError:
        print("Usage: python -m iron_python_learning [all|1..10]")
        return 2

    pprint(run_stage(stage_number), sort_dicts=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
