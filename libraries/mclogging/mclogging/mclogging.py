import sys
from pathlib import Path

from loguru import logger


TIME_FORMAT = "{time:YYYY-MM-DD at HH:mm:ss}"

LOGS_PATH = Path("/logs")


def markup(text: str, color: str) -> str:
    return f"<{color}>{text}</{color}>"


def green(text: str) -> str:
    return markup(text, "green")


def level(text: str) -> str:
    return markup(text, "level")


def cyan(text: str) -> str:
    return markup(text, "cyan")


def setup_logs(component: str):
    stdout_format = f"{green(TIME_FORMAT)} | {cyan(component)} | {level('{level}')} | {level('{message}')}"
    file_format = f"{TIME_FORMAT} | {component} | {'{level}'} | {'{message}'}"

    logger.configure(handlers=[])
    logger.add(
        LOGS_PATH / f"{component}-{{time}}.log",
        rotation="500 MB",
        compression="zip",
        level="DEBUG",
        format=file_format,
        colorize=True,
    )
    logger.add(
        sys.stdout,
        level="DEBUG",
        format=stdout_format,
        colorize=True,
    )
