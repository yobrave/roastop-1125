"""rop6 affection audit: carry the roast from entry.txt to the output slot."""
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

CAP = 140


@dataclass
class Roast:
    words: str = ""
    count: int = 0
    carries: bool = False
    notes: list = field(default_factory=list)

    def inspect(self, body: str):
        self.words = body.strip()
        self.count = len(self.words)
        self.notes.append(f"count={self.count}")
        if self.words and not self.words.isspace() and self.count <= CAP:
            self.carries = True
            self.notes.append("within cap")
        else:
            self.notes.append("over cap or empty")

    def deposit(self, folder: Path):
        if self.carries:
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "entry.txt").write_bytes(self.words.encode("utf-8"))
            self.notes.append("deposited")


def boot() -> int:
    yard = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "rop6_out")
    roast = Roast()
    roast.inspect(Path(__file__).resolve().parent.joinpath("entry.txt").read_text(encoding="utf-8"))
    roast.deposit(yard)
    print("VERDICT", json.dumps({"carries": roast.carries, "count": roast.count, "cap": CAP, "notes": roast.notes}))
    return 0 if roast.carries else 1


if __name__ == "__main__":
    sys.exit(boot())
