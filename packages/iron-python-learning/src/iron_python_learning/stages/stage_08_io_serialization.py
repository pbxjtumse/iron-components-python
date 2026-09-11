from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


@dataclass(frozen=True)
class UserProfile:
    user_id: str
    roles: list[str]


def demo() -> dict[str, object]:
    profile = UserProfile("u-1001", ["admin", "developer"])

    with TemporaryDirectory() as directory:
        path = Path(directory) / "profile.json"
        path.write_text(json.dumps(asdict(profile), ensure_ascii=False), encoding="utf-8")
        loaded = json.loads(path.read_text(encoding="utf-8"))

    return {
        "topic": "pathlib, json, dataclass serialization",
        "serialized_keys": sorted(loaded.keys()),
        "roles": loaded["roles"],
    }
