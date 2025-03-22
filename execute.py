from handbook.downloader import HandbookDownloader
from handbook.sanitizer import LinkSanitizer
from handbook.filler import FillMissing
from handbook import const
import argparse
from pathlib import Path


def download(dir: Path):
    date = dir.stem
    print(f"------------ Starting {date} ------------")

    downloader = HandbookDownloader(dir)
    for page in const.PAGES:
        try:
            downloader.get_page(date, page)
        except Exception as e:
            print(f"----Failed to download {page}")
            print(e)


def sanitize(dir: Path, rm_links: bool):
    date = dir.stem
    print(f"------------ Sanitizing {date} ------------")

    sanitizer = LinkSanitizer(dir, rm_links)
    sanitizer.run()


def missing(dir: Path, fill: bool):
    missing = FillMissing(dir)
    for date in const.DATES:
        print(f"------------ Finding missing {date} ------------")
        missing.find_missing(date)

    print()
    perc = 100 * len(missing.missing) / (len(const.DATES) * len(const.PAGES))
    print()
    print(f"Missing {perc:.2f}% of links.")
    missing.save_missing()

    if fill:
        missing.fill()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir", default=Path("editions"), type=Path, help="Directory to save data."
    )
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

    # ------------------------- Run things ------------------------- #
    args.dir.mkdir(exist_ok=True)

    if args.operation == "missing":
        missing(args.dir, args.fill)

    elif args.operation == "download":
        if args.date == "all":
            dates = const.DATES[::-1]
        else:
            dates = [args.date]

        for d in dates:
            download(args.dir / d)

    elif args.operation == "sanitize":
        if args.date == "all":
            dates = const.DATES[::-1]
        else:
            dates = [args.date]

        for d in dates:
            sanitize(args.dir / d, args.rm_links)
