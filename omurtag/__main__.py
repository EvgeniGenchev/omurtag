import argparse
from rich.console import Console
from rich_argparse import RichHelpFormatter
from omurtag import run

PROG = "omurtag"
DESCRIPTION = """
TEST omurtag is a tool that helps your create projects from templates
"""
RichHelpFormatter.console = Console(force_terminal=True)


def main():
    parser = argparse.ArgumentParser(
        prog=PROG,
        formatter_class=RichHelpFormatter,
        description=DESCRIPTION,
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # -- add mode --
    add_parser = subparsers.add_parser(
        "add",
        help="Add new template folder",
        formatter_class=RichHelpFormatter,
    )
    add_parser.add_argument(
        "input_file",
        type=str,
        help="Your project dependency template",
    )

    # -- remove mode --
    remove_parser = subparsers.add_parser(
        "remove",
        help="Remove a template folder",
        formatter_class=RichHelpFormatter,
    )
    remove_parser.add_argument(
        "template_name",
        type=str,
        help="Remove the provided template from the list",
    )

    # -- create mode --
    create_parser = subparsers.add_parser(
        "create",
        help="Generate a project based on an available template",
        formatter_class=RichHelpFormatter,
    )
    create_parser.add_argument(
        "project_name", type=str, help="Your project name", nargs="?"
    )

    create_parser.add_argument(
        "-t",
        "--type",
        type=str,
        help='Project type you want to generate. If unsure what projects are supported use "omurtag list"',
        required=False,
        default=None,
    )

    # -- list mode --
    list_parser = subparsers.add_parser(
        "list",
        help="List template names and their technology stack, if present",
        formatter_class=RichHelpFormatter,
    )
    list_parser.add_argument("--verbose", action="store_true")

    # -- pull mode --
    pull_parser = subparsers.add_parser(
        "pull",
        help="Pull a template from a git repository and add it to your local templates",
        formatter_class=RichHelpFormatter,
    )
    pull_parser.add_argument(
        "-b",
        "--branch",
        type=str,
        help="The branch of the template git repo.",
        required=False,
        default=None,
    )

    pull_parser.add_argument(
        "link",
        type=str,
        help="The http link of the template git repo.",
    )

    pull_parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
    )

    # -- sync mode --
    subparsers.add_parser(
        "sync",
        help="Downlaod/Update all the template repositories mentioned in the config file.",
        formatter_class=RichHelpFormatter,
    )
    args = parser.parse_args()

    run(args)


if __name__ == "__main__":
    main()
