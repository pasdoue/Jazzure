import asyncio
import json
from pathlib import Path
from typing import List, Union

import requests
from bs4 import BeautifulSoup
from R2Log import logger
from strip_ansi import strip_ansi


class AzCLI:

    RELEASE_NOTES_URL = "https://learn.microsoft.com/en-us/cli/azure/release-notes-azure-cli?view=azure-cli-latest"

    @classmethod
    def retrieve_online_versions(cls):
        res = []
        r = requests.get(cls.RELEASE_NOTES_URL, timeout=30)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        for p in soup.find_all("p"):
            if p.text.startswith("Version "):
                res.append(p.text.split(' ')[-1])
        logger.debug(f"Found all versions of az CLI : {','.join(res)}")
        return res


class AzureCliCrawler:

    OUTPUT_FILE = Path(__file__).parent / "azure_cli_commands.json"

    def __init__(self):
        self.commands = {}
        self.visited = set()
        self.stats = { "groups": 0, "commands": 0, "errors": 0 }

    @staticmethod
    async def run_az_help(path) -> tuple[int, str]:
        """
            Execute : az <path> --help
            :return return code & text from help
        """
        async with asyncio.Semaphore(10):
            command = ["az"] + path + ["--help"]
            # synchronous method
            # proc = subprocess.run( command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")

            #async method
            proc = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()

            return proc.returncode, stdout.decode()

    @staticmethod
    def get_sections(lines: str):
        """
             Transform help in dict :
             {
                 "Subgroups": [...],
                 "Commands": [...],
                 "Arguments": [...],
                 "Examples": [...],
                 ...
             }
        """
        sections = {}
        current_section = None
        current_lines = []

        for line in lines.splitlines():
            if line and line[0].isalpha():
                # save previous part
                if current_lines:
                    sections[current_section] = "\n".join(current_lines)
                    current_lines = []
                current_section = line.strip().replace(':','')
            elif current_section is not None:
                current_lines.append(line)
        # save previous part
        if current_lines:
            sections[current_section] = "\n".join(current_lines)
        return sections

    @staticmethod
    def parse_section(content: Union[List[str] | str]) -> List[str]:
        """
            Generic parser for section content
        """
        result = []
        content = content.splitlines() if isinstance(content, str) else content
        # Find first non-empty line
        first_line = next((line for line in content if line.strip()), None)
        if first_line is None:
            return []
        command_indent = len(first_line) - len(first_line.lstrip())
        commands = []
        for line in content:
            if not line.strip():
                continue
            indentation = len(line) - len(line.lstrip())
            if indentation == command_indent:
                # because Az CLI return some colors and ANSI strings, we need to remove it for effective parsing
                command = strip_ansi(line.strip().split(":", 1)[0]).strip()
                # remove every [Preview] or whatever
                if "[" in command:
                    command = strip_ansi(command.split("[")[0]).strip()
                commands.append(command)
        return commands

    @staticmethod
    def parse_subgroups(content: str) -> List[str]:
        """
            Example :
                Subgroups:
                    app       : Manage applications.
                    credential: Manage credentials.
            :return ["app", "credential"]
        """
        return AzureCliCrawler.parse_section(content=content.splitlines())

    @staticmethod
    def parse_commands(content: str) -> List[str]:
        """
            Example :
                Commands:
                    create : Create something.
                    delete : Delete something.
            :return ["create", "delete"]
        """
        return AzureCliCrawler.parse_section(content=content.splitlines())

    @staticmethod
    def parse_arguments(content: Union[List[str]|str]):
        arguments = []
        current = None

        def save_current():
            #TODO parse description to retrieve "Allowed values"
            nonlocal current
            if current is None:
                return
            current["description"] = " ".join( line.strip() for line in current["description"] if line.strip() )
            arguments.append(current)
            current = None

        content = content.splitlines() if isinstance(content, str) else content

        for line in content:
            if not line.strip():
                continue

            # Number of spaces before text
            indentation = len(line) - len(line.lstrip())
            stripped = line.strip()

            # Arg is a line beginning with "--" AND is not necessary indented
            if stripped.startswith("--") and indentation < 20:
                save_current()
                # Separate options & description parts
                if ":" in stripped:
                    option_part, description = stripped.split(":", 1)
                else:
                    option_part = stripped
                    description = ""

                tokens = option_part.split()

                option_names = []
                required = False
                special_mode = ""

                for token in tokens:
                    if token == "[Required]":
                        required = True
                    elif token == "[Preview]":
                        special_mode = "preview"
                    elif token == "[Deprecated]":
                        special_mode = "deprecated"
                    elif token.startswith("-"):
                        option_names.append(token)

                if not option_names:
                    continue

                current = {
                    "name": option_names[0],
                    "aliases": option_names[1:],
                    "required": required,
                    "special_mode": special_mode,
                    "description": [],
                }

                if description.strip():
                    current["description"].append(description.strip())

            # Line that continue the description
            elif current is not None:
                current["description"].append(stripped)
        save_current()
        return arguments

    @staticmethod
    def parse_examples(lines: Union[List[str]|str]) -> List[str]:
        """ Keep examples as text """
        examples = []
        current = []
        lines = lines.splitlines() if isinstance(lines, str) else lines
        for line in lines:
            # Keep orginal indentation
            if line.strip():
                current.append(line.rstrip())
            elif current:
                examples.append("\n".join(current))
                current = []
        if current:
            examples.append("\n".join(current))
        return examples

    @staticmethod
    def parse_help(path: List[str], help_text: str) -> dict:
        sections = AzureCliCrawler.get_sections(help_text)
        subgroups = AzureCliCrawler.parse_subgroups(sections.get("Subgroups", ""))
        commands = AzureCliCrawler.parse_commands(sections.get("Commands", ""))
        arguments_id = AzureCliCrawler.parse_arguments(sections.get("Id Arguments", ""))
        arguments = AzureCliCrawler.parse_arguments(sections.get("Arguments", ""))
        global_policy_arguments = AzureCliCrawler.parse_arguments(sections.get("Global Policy Arguments", ""))
        global_arguments = AzureCliCrawler.parse_arguments(sections.get("Global Arguments", ""))
        # find maybe other types of args
        other_args = []
        for section_name in list(sections.keys()):
            if not section_name in ["Subgroups", "Commands", "Arguments", "Id Arguments", "Global Policy Arguments", "Global Arguments"]:
                other_args.extend(AzureCliCrawler.parse_arguments(sections.get(section_name, [])))

        examples = AzureCliCrawler.parse_examples(sections.get("Examples", []))
        return {
            "path": path,
            "command": "az " + " ".join(path),
            "subgroups": subgroups,
            "commands": commands,
            "arguments": arguments,
            "arguments_id": arguments_id,
            "global_policy_arguments": global_policy_arguments,
            "global_arguments": global_arguments,
            "other_args" : other_args,
            "examples": examples,
            # Useful later to parse again without parsing az cli again
            "raw_help": help_text
        }

    async def crawl(self, path: Union[None|List[str]] = None):
        path = [] if path is None else path
        path_tuple = tuple(path)

        if path_tuple in self.visited:
            return
        self.visited.add(path_tuple)
        command_string = ("az" if not path else "az " + " ".join(path) )
        logger.info(f"{command_string}")
        returncode, help_text = await AzureCliCrawler.run_az_help(path)
        if returncode != 0:
            logger.error(f"Error1 detected on command '{command_string}' return code {returncode}")
            self.stats["errors"] += 1
            return
        parsed = AzureCliCrawler.parse_help(path, help_text)
        self.stats["groups"] += 1

        #async def process_command(command):
        for command in parsed.get("commands", []):
            command_path = path + [command]
            command_string = ("az "+ " ".join(command_path))
            logger.debug(f"[CMD] {command_string}")
            returncode, command_help = await AzureCliCrawler.run_az_help(command_path)
            # we should never hit this condition if parsing worked properly ! But left in case
            if returncode != 0:
                logger.error(f"Error2 detected on command '{command_string}' return code : {returncode}")
                self.stats["errors"] += 1
                self.commands[" ".join(command_path)] = {
                    "path": command_path,
                    "command": command_string,
                    "error": True,
                    "returncode": returncode,
                    "raw_help": command_help
                }
                continue
            command_data = AzureCliCrawler.parse_help(command_path, command_help)
            self.commands[" ".join(command_path)] = command_data
            self.stats["commands"] += 1
        # Subgroups
        workers = [ asyncio.create_task(self.crawl(path + [subgroup])) for subgroup in parsed.get("subgroups", []) ]
        await asyncio.gather(*workers)


    def save(self, filename: Path) -> None:
        output = {
            "metadata": {
                "command_count": self.stats["commands"],
                "group_count": self.stats["groups"],
                "error_count": self.stats["errors"]
            },
            "commands": self.commands
        }
        with filename.open("w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)









