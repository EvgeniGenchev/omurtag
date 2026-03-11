from rich import print
from rich.prompt import Confirm
from pathlib import Path
from argparse import Namespace
from os import listdir
import shutil
from shutil import copytree, rmtree
from .utils import (
    get_data_directory,
    create_directory,
    replace_in_files,
)


def run(args: Namespace):
    data_directory = _ensure_data_directory()

    match args.mode:
        case "add":
            _add(args, data_dir=data_directory)
        case "list":
            _list(args, data_dir=data_directory)
        case "create":
            _create(args, data_dir=data_directory)
        case "remove":
            _delete(args, data_dir=data_directory)
        case "pull":
            print(
                "[yellow]'pull' is not yet implemented, coming soon![/yellow]"
            )
        case "sync":
            print(
                "[yellow]'sync' is not yet implemented, coming soon![/yellow]"
            )
        case _:
            print(args.mode)
            assert False  # this should never happen if argparse works


def _ensure_data_directory() -> str:
    try:
        return get_data_directory()
    except FileNotFoundError:
        return create_directory()  # this can raise but idk


def _ensure_template_exists(
    args, data_dir, template: str, print_flag=True
) -> bool:
    if template not in (templates := _list(args, data_dir, print_flag=False)):
        if print_flag:
            print("[red]Template not found![/red]")
            print("[orange1]Available templates:[/orange1]")
            for t in templates:
                print(f"\t{t}")
        return False
    return True


def _delete(args, data_dir):

    to_be_deleted = args.template_name

    if not _ensure_template_exists(
        args, data_dir, template=to_be_deleted, print_flag=True
    ):
        return

    try:
        dst = str(Path(data_dir) / Path(to_be_deleted))
        rmtree(dst)
    except FileNotFoundError:
        # TODO: asserts are striped in -0 so figure something else
        assert False  # THIS should not ever happen as it is checked
    except PermissionError:
        print("[red]Permission denied — folder may be partially deleted[/red]")


def _add(args, data_dir):
    src = args.input_file
    dst = str(Path(data_dir) / Path(src).stem)
    try:
        copytree(
            src,
            dst,
            dirs_exist_ok=True,
        )
    # TODO: figure these cases out
    except FileNotFoundError:
        assert False
    except PermissionError:
        pass
    except shutil.Error:
        pass
    except OSError:
        pass


def _create(args, data_dir):
    project_path = Path(args.project_name).resolve()
    template_name = args.type

    if not _ensure_template_exists(
        args, data_dir, template=template_name, print_flag=True
    ):
        return

    if project_path.exists():
        if not Confirm.ask(
            f"'{project_path}' already exists. Overwrite?",
            default=False,
        ):
            print("[red]Aborted.[/red]")
            return

    src = str(Path(data_dir) / template_name)
    dst = str(project_path)

    print(project_path.name)

    try:
        copytree(
            src,
            dst,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                ".git",
            ),
        )
        replace_in_files(dst, {"<*project*>": project_path.name})

        print(
            f"[green]Project '{project_path.name}' created at {project_path.parent}[/green]"
        )
    except PermissionError:
        print("[red]Permission denied[/red]")
    except shutil.Error as e:
        for failed_src, _, msg in e.args[0]:
            print(f"[red]Failed to copy {failed_src}: {msg}[/red]")
    except OSError as e:
        print(f"[red]OS error: {e}[/red]")


def _list(args, data_dir, print_flag=True):

    _ = args

    templates = listdir(data_dir)

    if print_flag:
        if not templates:
            print(f"[red]No templates found in {data_dir}[/red]")

        for t in templates:
            print(f"[orange1]{t}[/orange1]")

    return templates
