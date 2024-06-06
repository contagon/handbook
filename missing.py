import const
import os
import shutil


class FillMissing:
    def __init__(self):
        self.missing = []

    def find_missing(self, dir):
        # Figure our which files are missing
        for page in const.PAGES:
            filename = f"{dir}/{page}.md"
            if not os.path.exists(filename):
                self.missing.append(filename)
                print(f"---- {page}")

    def save_missing(self, dir):
        # Save the missing files
        with open("missing.txt", "w") as f:
            for filename in self.missing:
                f.write(f"{filename}\n")

    @staticmethod
    def fill():
        pass
