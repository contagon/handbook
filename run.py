from scraper.downloader import HandbookDownloader
from scraper.sanitizer import LinkSanitizer
from scraper.filler import FillMissing
from scraper import const
import argparse
import os


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


def sanitize(date, rm_links):
    print(f"------------ Sanitizing {date} ------------")
    os.makedirs(date, exist_ok=True)

    sanitizer = LinkSanitizer(date, rm_links)
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
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help="Type of operation to perform", dest="operation"
    )

    # ------------------------- Downloader ------------------------- #
    download_parser = subparsers.add_parser("download")
    download_parser.add_argument(
        "--date",
        default=const.DATES[-1],
        choices=const.DATES + ["all"],
        help="Date to download.",
    )

    # ------------------------- Filler ------------------------- #
    missing_parser = subparsers.add_parser("missing")
    missing_parser.add_argument(
        "--fill",
        action="store_true",
        help="If missing files should be filled. Otherwise creates a file of missing links.",
    )

    # ------------------------- Sanitizer ------------------------- #
    sanitize_parser = subparsers.add_parser("sanitize")
    sanitize_parser.add_argument(
        "--date",
        default=const.DATES[-1],
        choices=const.DATES + ["all"],
        help="Date to sanitize.",
    )
    sanitize_parser.add_argument(
        "--rm-links", action="store_true", help="Remove links."
    )

    args = parser.parse_args()

    if args.operation == "missing":
        missing(args.fill)

    elif args.operation == "download":
        if args.date == "all":
            for date in const.DATES[::-1]:
                download(date)
        else:
            download(args.date)

    elif args.operation == "sanitize":
        if args.date == "all":
            for date in const.DATES[::-1]:
                sanitize(date, args.rm_links)
        else:
            sanitize(args.date, args.rm_links)
