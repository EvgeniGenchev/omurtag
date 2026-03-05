import argparse
from rich_argparse import RichHelpFormatter
from omurtag import run

PROG = "omurtag"
DESCRIPTION = """
omurtag is a tool that helps your create projects from templates
"""


def main():
    parser = argparse.ArgumentParser(
        prog=PROG, formatter_class=RichHelpFormatter, description=DESCRIPTION
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # -- add mode --
    add_parser = subparsers.add_parser("add", help="Add new template folder")
    add_parser.add_argument(
            "input_file",
            type=str,
            help="Your project dependency template",
            )

    # -- remove mode --
    remove_parser = subparsers.add_parser("remove", help="Remove a template folder")
    remove_parser.add_argument(
            "template_name",
            type=str,
            help="Remove the provided template from the list"
            )
    
    # -- create mode --
    create_parser = subparsers.add_parser("create", help="Generate a project based on an available template")
    create_parser.add_argument("project_name",
            type=str,
            help="Your project name"
            )

    create_parser.add_argument(
            "-t",
            "--type",
            type=str,
            help="Project type you want to generate. If unsure what projects are supported use \"omurtag list\"",
            required=True
            )

    # -- list mode --
    list_parser = subparsers.add_parser('list', help="List template names and their technology stack, if present")
    list_parser.add_argument('--verbose', action='store_true')

    # -- pull mode --
    # TODO: need to implement 
    # pull_parser = 
    subparsers.add_parser('pull', help="[upcoming] Pull a template from a git repository and add it to your local templates")
    # pull_parser.add_argument("link", 
    #                          type=str,
    #                          help="The link of the template git repo.")

    args = parser.parse_args()

    run(args)

if __name__ == "__main__":
    main()
