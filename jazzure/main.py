import argparse
import asyncio
import time
from pathlib import Path

from R2Log import logger, console

from jazzure.az_cli.azcli import AzCLI, AzureCliCrawler
from jazzure.config.ToolConfig import __version__
from jazzure.utils import print_banner, set_logger, print_elapsed_time

def parse_args() -> argparse.Namespace:

    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument('--no-banner', action="store_true", default=False, help='Do not print banner')

    # Parse only known args first
    pre_args, remaining = pre_parser.parse_known_args()
    if not pre_args.no_banner:
        print_banner()

    parser = argparse.ArgumentParser(description='Azure recon', parents=[pre_parser]) #little hack to print banner on help menu. Do not return str because if so, the rest of help message wont print...
    parser.add_argument('--log-file', action="store_true", help='Log inside file the current run')
    parser.add_argument("--version", action="store_true", help="Print tool version")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbosity level (-v for verbose, -vv for advanced, -vvv for debug)")
    return parser.parse_args()

def entry_point():
    args = parse_args()
    set_logger(level=args.verbose, logfile=args.log_file)

    if args.version:
        logger.info(f"Version : {__version__}")
        exit(0)

    print(AzCLI.retrieve_online_versions())

    # crawler = AzureCliCrawler()
    # start = time.time()
    # asyncio.run(crawler.crawl())
    # print_elapsed_time(start_time=start, format="minutes")
    # crawler.save(AzureCliCrawler.OUTPUT_FILE)
    # logger.info(f"Groups :   {crawler.stats['groups']}")
    # logger.info(f"Commands : {crawler.stats['commands']}")
    # logger.info(f"Errors :   {crawler.stats['errors']}")
    # logger.info(f"Output :    {Path(AzureCliCrawler.OUTPUT_FILE).absolute()}")



def main():
    try:
        entry_point()
        return 0
    except (KeyboardInterrupt, EOFError):
        return 2
    except SystemExit as e:
        if e.code is not None:
            return int(e.code)
    except Exception as e:
        logger.error(f"It seems that something unexpected happened ...\n{e}")
        console.print_exception(show_locals=True, suppress=[])
    return 1
