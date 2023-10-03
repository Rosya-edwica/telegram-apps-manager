from typing import NamedTuple
import re
import subprocess

SUCCESS_EMOJI = '✅'
ERROR_EMOJI = '❌'
DIED_EMOJI = '☠️'

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
    status = re.sub(":|since", "", re.findall(":.*since", active_line)[0]).strip()
    if "failed" in status:
        status = f"{ERROR_EMOJI} {status}"
    elif "running" in status:
        status = f"{SUCCESS_EMOJI} {status}"
    elif "inactive" in status:
        status = f"{DIED_EMOJI} {status}"
    return ActiveStatus(
        StartTime=re.sub(";", "", re.findall(";.*", active_line)[0]).strip(),
        Status=status,
        Date=re.sub("since", "", re.findall("since.*MSK", active_line)[0]),
    )

def parse_logs(text: str) -> list[str]:
    logs = re.findall("\w+ \d+ .*", text)
    return [i + "\n" for i in logs]


def update_systemd_gpt_config(action: str):
    config = f"""
        [Unit]
        Description=(GPT-processing 2) App for processing positions by GPT for {action}
        After=network.target

        [Service]
        User=root
        Group=root
        WorkingDirectory=/root/go-gpt-processing_copy/
        ExecStart=/root/go-gpt-processing_copy/cmd/gpt_processing_2 {action}

        [Install]
        WantedBy=multi-user.target
    """
    subprocess.Popen(f"echo '{config}' > /etc/systemd/system/gpt_processing_1.service", shell=True)