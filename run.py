from download import HandbookDownloader
from sanitize import LinkSanitizer
from missing import FillMissing
import argparse
import os
import const


def download(date):
    print(f"-------- Starting {date} --------")
    os.makedirs(date, exist_ok=True)

    downloader = HandbookDownloader(date)
    for page in const.PAGES:
        try:
            downloader.get_page(date, page)
        except Exception as e:
            print(f"----Failed to download {page}")
            print(e)


def sanitize(date):
    print(f"-------- Sanitizing {date} --------")
    os.makedirs(date, exist_ok=True)

    sanitizer = LinkSanitizer(date)
    sanitizer.run()


def missing(_date):
    missing = FillMissing()
    for date in const.DATES:
        print(f"-------- Finding missing {date} --------")
        missing.find_missing(date)

    print()
    print("-------- Saving missing --------")
    missing.save_missing("missing.md")

    missing.fill()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--kind", choices=["sanitize", "download", "missing"])
    args.add_argument("--date", default="2024-05", choices=const.DATES + ["all"])
    args = args.parse_args()

    func = locals()[args.kind]

    if args.kind == "missing" and args.date != "2024-05":
        raise ValueError("Missing always runs on all dates.")

    if args.date == "all":
        for date in const.DATES[::-1]:
            func(date)
    else:
        func(args.date)
