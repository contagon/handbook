from md import HandbookDownloader
from tqdm import tqdm
import argparse
import os
import datetime
import requests
from time import sleep

wayback_api = "https://archive.org/wayback/available?"

urls = [
    "0-introductory-overview",
    "1-work-of-salvation-and-exaltation",
    "2-supporting-individuals-and-families",
    "3-priesthood-principles",
    "4-leadership-in-the-church-of-jesus-christ",
    "5-general-and-area-leadership",
    "6-stake-leadership",
    "7",
    "8-elders-quorum",
    "9-relief-society",
    "10-aaronic-priesthood",
    "11-young-women",
    "12-primary",
    "13-sunday-school",
    "14-single-members",
    "15-seminaries-and-institutes",
    "16-living-the-gospel",
    "17-teaching-the-gospel",
    "18-priesthood-ordinances-and-blessings",
    "19-music",
    "20-activities",
    "21-ministering",
    "22-providing-for-temporal-needs",
    "23",
    "24",
    "25-temple-and-family-history-work",
    "26-temple-recommends",
    "27-temple-ordinances-for-the-living",
    "28",
    "29-meetings-in-the-church",
    "30-callings-in-the-church",
    "31",
    "32-repentance-and-membership-councils",
    "33-records-and-reports",
    "34-finances-and-audits",
    "35",
    "36-creating-changing-and-naming-new-units",
    "37-specialized-stakes-wards-and-branches",
    "38-church-policies-and-guidelines",
]
prefix = "https://www.churchofjesuschrist.org/study/manual/general-handbook/"
urls = [f"{prefix}{u}?lang=eng" for u in urls]

dates = [
    "2020-03",
    "2020-07",
    "2020-12",
    "2021-03",
    "2021-07",
    "2022-08",
    "2023-08",
    "2024-05",
]


def find_link(curr_date, url):
    # use wayback api to find closest snapshot
    next_date = dates[dates.index(curr_date) + 1]
    next_date = datetime.datetime.strptime(next_date, "%Y-%m")
    curr_date = datetime.datetime.strptime(curr_date, "%Y-%m")

    months_apart = (next_date - curr_date).days // 30
    # Make sure to start at start of next month as it might have come out mid-month of curr_date
    for i in range(1, months_apart):
        down_date_guess = curr_date + datetime.timedelta(days=i * 30)
        api = wayback_api + f"url={url}&timestamp={down_date_guess.strftime('%Y%m%d')}"
        ans = requests.get(api).json()

        if "closest" not in ans["archived_snapshots"]:
            continue

        down_date = ans["archived_snapshots"]["closest"]["timestamp"]
        down_date = datetime.datetime.strptime(down_date, "%Y%m%d%H%M%S")

        if down_date > curr_date:
            break

    if down_date > next_date:
        print(f"No snapshot found for {url} on {curr_date}")
        return None

    print(f"Found snapshot {down_date.strftime('%Y-%m-%d')} for {url.split('/')[-1]}")
    return down_date.strftime("%Y%m%d%H%M%S")


def download(date, dir):
    os.makedirs(dir, exist_ok=True)
    converter = HandbookDownloader()

    idx = dates.index(date)
    for u in urls:
        if idx == len(dates) - 1:
            link = u
        else:
            snapshot = find_link(date, u)
            if snapshot is None:
                continue
            link = f"https://web.archive.org/web/{snapshot}id_/{u}"

        converter.add_page(link)
        sleep(10)

    converter.process_links()
    converter.write_files(dir)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--date", default="2024-05", choices=dates)
    args.add_argument("--dir", default="handbook")
    args = vars(args.parse_args())

    download(**args)


# 20230909055210
