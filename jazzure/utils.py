import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
import random
import shutil

from R2Log import logger
from rich.emoji import Emoji
from rich.progress import ProgressColumn
from rich.text import Text

def print_banner() -> None:
    #banners = {"ansi": [], "raw": []}
    banners = {"ansi": []}
    banners_fldr = Path(__file__).parent / "assets"
    for file in banners_fldr.rglob("*.ansi"):
        content = file.read_text(encoding="utf-8")
        content += "                                                                                  [38;2;72;180;220mMade by pasdoue[0m\n\n"
        banners["ansi"].append(content)
    # banners["raw"].append("")
    category, values = random.choice(list(banners.items()))
    random_choice = values[0] if len(values) == 1 else random.choice(values)
    if category == "raw":
        logger.info(random_choice)
    else:
        sys.stdout.write(random_choice)

def binary_installed(binary_name: str) -> bool:
    """
        Simple minimalist code to check if a binary is installed
    """
    path = shutil.which(binary_name)
    return True if path is not None else False

def print_elapsed_time(start_time, format: str = "seconds") -> None:
    end = time.time()
    if format == "seconds":
        logger.info(f"Script took : {str(end - start_time)} seconds")
    elif format == "minutes":
        logger.info(f"Script took : {str((end - start_time)/60)} minutes")

def set_logger(level: int, logfile: bool = False) -> None:
    logger.setVerbosity(level)

    if logfile:
        log_file = Path.cwd() / "logs.txt"
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,  # 5 Mo
            backupCount=3,
            encoding="utf-8",
        )
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setLevel(logger.level)
        file_handler.setFormatter(formatter)
        # Add the file handler to the logger
        logger.addHandler(file_handler)


class HamsterBarColumn(ProgressColumn):
    def __init__(self, width=30):
        super().__init__()
        self.width = width

    def render(self, task):
        total = task.total or 1
        saxo_pos = int((task.completed / total) * (self.width - 1))
        # hamster stays behind
        hamster_pos = int(saxo_pos * 0.8)
        bar = []

        for i in range(self.width):
            if i == saxo_pos:
                bar.append(Emoji.replace(':saxophone:'))
            elif i == hamster_pos and saxo_pos > 0:
                bar.append(Emoji.replace(':hamster:'))
            elif i < saxo_pos:
                bar.append(Emoji.replace(':water_wave:'))
            else:
                bar.append("　")
        return Text(" ".join(bar))
