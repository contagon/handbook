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
                print(page)

    def save_missing(self, file):
        # Save the missing files
        with open(file, "w") as f:
            for filename in self.missing:
                f.write(f"{filename}\n")

    @staticmethod
    def fill():
        # Forward pass for fill in
        for i in range(1, len(const.DATES)):
            prev = const.DATES[i - 1]
            curr = const.DATES[i]

            for filename in os.listdir(prev):
                if not os.path.exists(f"{curr}/{filename}"):
                    shutil.copy(f"{prev}/{filename}", f"{curr}/{filename}")
                    print(f"---- Copied {filename} from {prev} to {curr}")

        # Backward pass for fill in
        for i in range(len(const.DATES) - 2, -1, -1):
            prev = const.DATES[i + 1]
            curr = const.DATES[i]

            for filename in os.listdir(prev):
                if not os.path.exists(f"{curr}/{filename}"):
                    shutil.copy(f"{prev}/{filename}", f"{curr}/{filename}")
                    print(f"---- Copied {filename} from {prev} to {curr}")
