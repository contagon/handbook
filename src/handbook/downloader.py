from bs4 import BeautifulSoup
import requests
from markdownify import MarkdownConverter
from markdownify import ATX, UNDERSCORE
import re
import datetime
from . import const
from time import sleep
from pathlib import Path


class HandbookConverter(MarkdownConverter):
    def convert_td(self, el, text, convert_as_inline):
        """Handle tables with bullet points in them via html breaks and bullet points characters"""
        colspan = 1
        if "colspan" in el.attrs:
            colspan = int(el["colspan"])

        text = text.strip().replace("\n", "<br/>")  # replace newlines with breaks
        text = re.sub(r"(?<!\\)\*", "•", text)  # replace asterisks with bullet points

        return " " + text + " |" * colspan

    def convert_img(self, el, text, convert_as_inline):
        """Don't bother with images"""
        return ""

    def convert_a(self, el, text, convert_as_inline):
        """Handle links to adaption/optional resources differently"""
        if not text and el.get("href").startswith(
            "/study/manual/general-handbook/0-introductory-overview"
        ):
            return "[[AO]](0-introductory-overview.md#02-adaptation-and-optional-resources)"

        return super().convert_a(el, text, convert_as_inline)


class HandbookDownloader:
    def __init__(self, dir: Path):
        self.converter = HandbookConverter(
            heading_style=ATX, strong_em_symbol=UNDERSCORE
        )
        self.dir = dir
        self.dir.mkdir(exist_ok=True)

    def convert(self, soup):
        # Remove extra header in body of tables
        for row in soup.find_all("tbody"):
            for extra in row.find_all("p", {"class": "label"}):
                extra.decompose()

        # Remove footnotes
        # To my knowledge, the only page with footnotes is 30.8
        for a in soup.find_all("a", {"class": "note-ref"}):
            a.decompose()

        # Remove images
        for img in soup.select('div[class*="imageWrapper-"]'):
            img.decompose()
        for img in soup.select('span[class*="imageWrapper-"]'):
            img.decompose()

        text = self.converter.convert_soup(soup).strip()
        text = re.sub(r"\n\s*\n", "\n\n", text)  # remove extra newlines

        text = re.sub(
            r"^ +([\w#])", r"\1", text, flags=re.MULTILINE
        )  # remove leading spaces

        # Some of the headers are missing header titles ##
        def add_title(match):
            num = len(match.group(1).split("."))
            return f"{match.group(1)}\n\n{'#'*num} {match.group(3)}"

        text = re.sub(
            "^(\d{1,2}(\.?\d{0,2}){0,3})\n\n([^#]+?)",
            add_title,
            text,
            flags=re.MULTILINE,
        )

        # merge number and header
        text = re.sub(
            "(\d{1,2}(\.?\d{0,2}){0,3})\n\n(#+) (.*)",
            r"\3 \1 \4",
            text,
        )

        # Some of the headers don't start on a new line
        text = re.sub("([^\n#])(#+ (\d{1,2}(\.?\d{0,2}){0,3}))", r"\1\n\n\2", text)

        return text

    def get_page(self, date, page):
        # download page
        filename = self.dir / f"{page}.md"

        if filename.exists():
            print(f"{filename} already exists, skipping")
            return

        print(f"{filename}")

        url, delay = self.find_link(date, page)
        if url is None:
            return
        response = requests.get(url)
        sleep(delay)
        soup = BeautifulSoup(response.content, "html.parser")
        print("----Downloaded")

        body = soup.find("div", {"class": "body"})

        # Save & clean title
        header = body.find("header")
        final = self.convert(header)
        final += "\n\n"

        # Save & clean body
        text = body.find("div", {"class": "body-block"})
        text = self.convert(text)
        final += text

        with open(filename, "w") as f:
            f.write(final)

        print("----Saved")

    def find_link(self, curr_date, page):
        url = f"{const.PREFIX}{page}?lang=eng"

        if curr_date == const.DATES[-1]:
            print("----Current version, no need for wayback machine")
            return url, 0.1

        # use wayback api to find closest snapshot
        next_date = const.DATES[const.DATES.index(curr_date) + 1]
        next_date = datetime.datetime.strptime(next_date, "%Y-%m")
        curr_date = datetime.datetime.strptime(curr_date, "%Y-%m") + datetime.timedelta(
            days=30
        )

        # Iterate backwards by month till we find something, since we prefer newer snapshots
        months_apart = (next_date - curr_date).days // 30
        for i in reversed(range(0, months_apart + 1)):
            down_date = None
            down_date_guess = curr_date + datetime.timedelta(days=i * 30)
            api = (
                const.WAYBACK_API
                + f"url={url}&timestamp={down_date_guess.strftime('%Y%m%d')}"
            )
            ans = requests.get(api).json()
            sleep(const.WAYBACK_DELAY)

            if "closest" not in ans["archived_snapshots"]:
                continue

            down_date = ans["archived_snapshots"]["closest"]["timestamp"]
            down_date = datetime.datetime.strptime(down_date, "%Y%m%d%H%M%S")

            if curr_date < down_date and down_date < next_date:
                print(f"----Found snapshot {down_date.strftime('%Y-%m-%d')}")
                return (
                    f"https://web.archive.org/web/{down_date.strftime('%Y%m%d%H%M%S')}id_/{url}",
                    const.WAYBACK_DELAY,
                )

        print("----No snapshot found, skipping")
        return None, None
