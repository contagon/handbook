from . import const
import shutil
from pathlib import Path


class FillMissing:
    def __init__(self, dir: Path):
        self.missing = []
        self.dir = dir

    def find_missing(self, date: str):
        dir = self.dir / date

        # Figure our which files are missing
        for page in const.PAGES:
            filename = dir / f"{page}.md"
            if not filename.exists():
                self.missing.append(filename)
                print(page)

    def save_missing(self, file: str = "missing.md"):
        # Save the missing files
        with open(self.dir / file, "w") as f:
            for filename in self.missing:
                f.write(f"{filename}\n")

    def fill(self):
        # Forward pass for fill in
        for i in range(1, len(const.DATES)):
            prev = const.DATES[i - 1]
            curr = const.DATES[i]

            for prev_file in (self.dir / prev).iterdir():
                if not (curr_file := self.dir / curr / prev_file.name).exists():
                    shutil.copy(prev_file, curr_file)
                    print(f"---- Copied {prev_file.name} from {prev} to {curr}")

        # Backward pass for fill in
        for i in range(len(const.DATES) - 2, -1, -1):
            prev = const.DATES[i + 1]
            curr = const.DATES[i]

            for prev_file in (self.dir / prev).iterdir():
                if not (curr_file := self.dir / curr / prev_file.name).exists():
                    shutil.copy(prev_file, curr_file)
                    print(f"---- Copied {prev_file.name} from {prev} to {curr}")
