from dataclasses import dataclass

from agbot.services.orm import AETResult, ENTResult, Schedule, User


@dataclass
class Orm:
    user: User = User
    ent: ENTResult = ENTResult
    aet: AETResult = AETResult
    dates: Schedule = Schedule
