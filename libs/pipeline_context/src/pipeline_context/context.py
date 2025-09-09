from __future__ import annotations
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Dict, Optional
import hashlib, time, json

@dataclass(frozen=True)
class ProcessingContext:
    file_id: str
    path: Path
    mime_type: str
    size_bytes: int
    sha256: str
    started_at: float = field(default_factory=time.time)
    meta: Dict[str, Any] = field(default_factory=dict, compare=False)  # mutable bag

    def with_meta(self, **kv) -> "ProcessingContext":
        """Return a new ctx with shallow-copied meta + updates (keeps immutability)."""
        new_meta = {**self.meta, **kv}
        return replace(self, meta=new_meta)

    def child(self, *, scope: str, **kv) -> "ProcessingContext":
        """Useful later for per-chunk/phase contexts."""
        return self.with_meta(parent_file_id=self.file_id, scope=scope, **kv)

    def to_json(self) -> str:
        d = self.__dict__.copy()
        d["path"] = str(self.path)
        return json.dumps(d, default=str)
