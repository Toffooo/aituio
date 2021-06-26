from roboparse import Parser

from .routers.aet import AETStreamsRouter
from .routers.images import JobsImageRouter
from .routers.text import ImportantDatesRouter
from .web import Web

requests = Web()
parser = Parser()


def get_jobs_image(static: bool = False):
    if not static:
        router = JobsImageRouter("", "").get()
        response = requests.get(router.path)

        if response.status_code == 200:
            data = parser.load(response.content, router)
            return data.get("data-original"), True
        return None, False
    return (
        "https://static.tildacdn.com/tild6164-3065-4733-a235-323561363165/photo.png",
        True,
    )


def get_important_dates():
    router = ImportantDatesRouter("", "")
    response = requests.get(router.get().path)

    if response.status_code == 200:
        trs = parser.load(response.content, router.get())
        text = (
            trs.text.strip()
            .replace("Дата;", "")
            .replace("Событие ", "")
            .replace(";", ":")
        )
        return text, True
    return None, False


def get_aet_streams_links():
    router = AETStreamsRouter("", "")
    response = requests.get(router.get().path)
    links = []

    if response.status_code == 200:
        blocks = parser.load(response.content, router.get())

        for block in blocks:
            title = block.find("div", attrs={"field": "btitle"}).text.strip()

            if "Формат" in title:
                continue

            tlinks = []
            for _link in block.find("div", attrs={"class": "t859__row"}).find_all(
                "div"
            ):
                if _link.find("a") is None:
                    continue

                tlinks.append(
                    {
                        "link": _link.find("a").get("href"),
                        "title": _link.find("a").text.strip(),
                    }
                )
            links.append({"title": title.replace("    Подробнее", ""), "links": tlinks})

    return links
