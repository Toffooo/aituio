import time

from agbot.services.db_conn import engine, session
from agbot.services.orm import AETResult, BaseModel, Schedule, base
from aitu_data_extractors.site import (
    get_aet_streams_links,
    get_important_dates,
)


def scrape_important_date():
    dates, _ = get_important_dates()
    Schedule.truncate()
    print("TRUNCATONG DATES")

    Schedule.create(descr=dates)
    print("DATES RECORDED")


def scrape_aet_stream_links():
    items = get_aet_streams_links()
    AETResult.truncate()
    print("TRUNCATING STREAM LINKS")

    for item in items:
        AETResult.create(
            title=item["title"],
            first_exam_link=item["links"][0]["link"],
            second_exam_link=item["links"][1]["link"],
        )
    print("ACTUAL DATA RECORDED")


if __name__ == "__main__":
    base.metadata.create_all(engine)
    BaseModel.set_session(session)

    while True:
        print("SERVICE HAS BEEN STARTED | PRESS CTRL + C TO EXIT")
        scrape_important_date()
        scrape_aet_stream_links()
        time.sleep(42600)
