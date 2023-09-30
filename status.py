from typing import NamedTuple
import re

class ActiveStatus(NamedTuple):
    Status: str
    StartTime: str
    Date: str

class Status(NamedTuple):
    ActiveStatus: ActiveStatus
    Logs: list[str]


def parse_status_info() -> Status:
    with open("status_info.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    return Status(
        ActiveStatus=parse_active_status(text),
        Logs=parse_logs(text)
    )


def parse_active_status(text: str) -> ActiveStatus:
    active_line = re.findall("Active:.*", text)[0]
    return ActiveStatus(
        StartTime=re.sub(";", "", re.findall(";.*", active_line)[0]).strip(),
        Status=re.sub(":|since", "", re.findall(":.*since", active_line)[0]).strip(),
        Date=re.sub("since", "", re.findall("since.*MSK", active_line)[0]),
    )

def parse_logs(text: str) -> list[str]:
    logs = re.findall("\w+ \d+ .*", text)
    return [i + "\n" for i in logs]
