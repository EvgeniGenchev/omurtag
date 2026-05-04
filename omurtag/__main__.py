import argparse
from rich.console import Console
from rich import print
from rich_argparse import RichHelpFormatter
from omurtag import run

PROG = "omurtag"
DESCRIPTION = """
omurtag is a tool that helps you create projects from templates
"""
RichHelpFormatter.console = Console(force_terminal=True)


def main():
    parser = argparse.ArgumentParser(
        prog=PROG,
        formatter_class=RichHelpFormatter,
        description=DESCRIPTION,
    )
    parser.add_argument("-v","--version", action="store_true")

    subparsers = parser.add_subparsers(dest="mode")

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

    # -- search mode --
    subparsers.add_parser(
        "search",
        help="Browse and pull templates from the community list.",
        formatter_class=RichHelpFormatter,
    )

    audit_parser = subparsers.add_parser(
        "audit",
        help="Run a security audit on the current directory.",
        formatter_class=RichHelpFormatter,
    )
    
    audit_parser.add_argument(
        "path",
        type=str,
        help="Your project directory.",
        default=".",
        nargs="?",
    )
    audit_parser.add_argument(
        "--short",
        action="store_true",
        help="Show package name, version, and status only (no CVE details).",
    )
    audit_parser.add_argument(
        "--only-vulnerable",
        action="store_true",
        dest="only_vulnerable",
        help="Hide packages with no known advisories.",
    )

    args = parser.parse_args()

    if not args.version and args.mode is None:
        parser.error("a mode is required")

    if args.version:
        version = __import__("importlib").metadata.version("omurtag")
        print(f"[blue]V{version}[/blue]")

        exit(0)

    run(args)


if __name__ == "__main__":
    main()
