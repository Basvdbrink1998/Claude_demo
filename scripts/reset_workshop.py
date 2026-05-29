"""
reset_workshop.py — Clean generated outputs before re-running the workshop.

Removes:
  - dashboard/   (rebuilt live in Step 3)
  - dry_run/     (produced by the dry run, not part of the live demo)

Keeps:
  - data/        (source data — never touched)
  - scripts/     (generation scripts)
  - storyline.md, speaker_notes.md, CLAUDE.md, etc.

Usage:
    python scripts/reset_workshop.py
"""

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

GENERATED = [
    REPO_ROOT / "dry_run",
]


def reset():
    removed = []
    skipped = []
    for path in GENERATED:
        if path.exists():
            shutil.rmtree(path)
            removed.append(path.name)
        else:
            skipped.append(path.name)

    print("Workshop reset complete.")
    if removed:
        print(f"  Removed: {', '.join(removed)}")
    if skipped:
        print(f"  Already clean: {', '.join(skipped)}")
    print("\nYou're ready to run the workshop from Step 0.")


if __name__ == "__main__":
    reset()
