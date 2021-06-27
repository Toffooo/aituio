import time

from agbot.services.db_conn import engine, session
from agbot.services.orm import ENTResult, AETResult, BaseModel, Schedule, base
from aitu_data_extractors.site import (
    get_aet_streams_links,
    get_important_dates,
)


def create_ent_results():
    print("ENT REULTS IS RUNNING")
    ENTResult.truncate()
    ENTResult.create(
        category="ICT",
        faculty="Comp. Scince",
        score="93",
        year=2020
    )
    ENTResult.create(
        category="ICT",
        faculty="Big Data Analysis",
        score="93",
        year=2020
    )
    ENTResult.create(
        category="ICT",
        faculty="Industrial Automation",
        score="93",
        year=2020
    )
    ENTResult.create(
        category="ICT",
        faculty="Media Tech.",
        score="93",
        year=2020
    )
    ENTResult.create(
        category="ICT",
        faculty="Software Engeneering",
        score="93",
        year=2020
    )
    ENTResult.create(
        category="Security",
        faculty="Cyber Security",
        score="83",
        year=2020
    )
    ENTResult.create(
        category="Management",
        faculty="IT Management",
        score="110",
        year=2020
    )
    ENTResult.create(
        category="Management",
        faculty="IT Management(с квотой)",
        score="76",
        year=2020
    )
    ENTResult.create(
        category="Journalism",
        faculty="Digital Journalism(с квотой)",
        score="98",
        year=2020
    )
    ENTResult.create(
        category="Journalism",
        faculty="Digital Journalism",
        score="98",
        year=2020
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
        create_ent_results()
        scrape_important_date()
        scrape_aet_stream_links()
        time.sleep(42600)
