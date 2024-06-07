from download import HandbookDownloader
from sanitize import LinkSanitizer
from missing import FillMissing
import argparse
import os
import const


def download(date):
    print(f"------------ Starting {date} ------------")
    os.makedirs(date, exist_ok=True)

    downloader = HandbookDownloader(date)
    for page in const.PAGES:
        try:
            downloader.get_page(date, page)
        except Exception as e:
            print(f"----Failed to download {page}")
            print(e)


def sanitize(date):
    print(f"------------ Sanitizing {date} ------------")
    os.makedirs(date, exist_ok=True)

    sanitizer = LinkSanitizer(date)
    sanitizer.run()


def missing(fill):
    missing = FillMissing()
    for date in const.DATES:
        print(f"------------ Finding missing {date} ------------")
        missing.find_missing(date)

    print()
    perc = 100 * len(missing.missing) / (len(const.DATES) * len(const.PAGES))
    print()
    print(f"Missing {perc:.2f}% of links.")
    missing.save_missing("missing.md")

    if fill:
        missing.fill()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--kind",
        choices=["sanitize", "download", "missing"],
        required=True,
        help="What to do",
    )
    args.add_argument(
        "--date",
        default=const.DATES[-1],
        choices=const.DATES + ["all"],
        help="Date to work on. Doesn't apply to fill.",
    )
    args.add_argument(
        "--fill",
        action="store_true",
        help="If missing links should be filled. Otherwise creates a file of missing links.",
    )
    args = args.parse_args()

    func = locals()[args.kind]

    if args.kind == "missing":
        func(args.fill)
        quit()

    if args.date == "all":
        for date in const.DATES[::-1]:
            func(date)
    else:
        func(args.date)
