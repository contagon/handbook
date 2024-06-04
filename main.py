from md import HandbookDownloader
from tqdm import tqdm

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
urls = [f"{prefix}{u}" for u in urls]

converter = HandbookDownloader()

for u in tqdm(urls):
    converter.add_page(u)

converter.process_links()
converter.write_files("handbook")
# from pprint import pprint as print

# print(converter.cache)
