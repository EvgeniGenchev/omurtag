from rich import print
from rich.prompt import Confirm
from tqdm.rich import tqdm
from pathlib import Path
from argparse import Namespace
from os import listdir
from git import Repo, cmd, exc
import shutil
from shutil import copytree, rmtree
from .utils import (
    get_data_directory,
    create_directory,
    replace_in_files,
    config_exist,
    get_config_file,
)

from tqdm import TqdmExperimentalWarning
import warnings

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

def run(args: Namespace):
    data_directory: str = _ensure_data_directory()

    if config_exist() is None:
        print("[red] No configuration file found!\n[/red]")
        print(
            " Please create a [yellow]config.py[/yellow] at one of the following locations: \n\
        XDG_CONFIG_HOME/omurtag \n\
        HOME/.omurtag"
        )
        exit(1)

    match args.mode:
        case "add":
            _add(
                args,
                data_dir=data_directory,
            )
        case "list":
            _list(
                args,
                data_dir=data_directory,
            )
        case "create":
            _create(
                args,
                data_dir=data_directory,
            )
        case "remove":
            _delete(
                args,
                data_dir=data_directory,
            )
        case "pull":
            _pull(
                args,
                data_dir=data_directory,
            )
            # print(
            #     "[yellow]'pull' is not yet implemented, coming soon![/yellow]"
            # )
        case "sync":
            _sync(
                args,
                data_dir=data_directory,
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
    args, data_dir: str, template: str, print_flag=True
) -> bool:
    if template not in (templates := _list(args, data_dir, print_flag=False)):
        if print_flag:
            print("[red]Template not found![/red]")
            print("[orange1]Available templates:[/orange1]")
            for t in templates:
                print(f"\t{t}")
        return False
    return True


def _delete(args, data_dir: str):

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


def _add(args, data_dir: str):
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


def _create(args, data_dir: str):
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
            print("[red] Command aborted.[/red]")
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


def _list(args, data_dir: str, print_flag=True):

    _ = args

    try:
        templates = listdir(data_dir)
    except FileNotFoundError:
        if print_flag:
            print(f"[red]No templates found in {data_dir}[/red]")
        exit(1)

    if print_flag:
        for t in templates:
            print(f"[orange1]{t}[/orange1]")

    return templates

def _pull(args, data_dir: str, ignore_error=False):
    url = args.link
    
    recursive = args.recursive

    if recursive:
        print("[yellow]Warning: recursive submodule download is not implemented![/yellow]")

    try:
        cmd.Git().ls_remote(url)
    except exc.GitCommandError:
        print(f"[red] {url} is not valid .git URL![/red]")
        if not ignore_error:
            exit(1)
        else:
            return

    # checks if the path.name contains _omurtag_template
    if not str(url).endswith("_omurtag_template"):
        print(f"[red] {url} is not valid omurtag template URL![/red]")
        if not ignore_error:
            exit(1)
        else:
            return

    # checks if the path.name without _omurtag_template is in data_dir
    templates = _list(args, data_dir=data_dir, print_flag=False)

    project_name = Path(url).stem.replace("_omurtag_template", "")

    if project_name in templates:
        if not Confirm.ask(
            f"[cyan]'{project_name}'[/cyan] already exists. Do you want to update?",
            default=False,
        ):
            print("[red] Update aborted.[/red]")
            return
        else:
            _update_template(
                project_name,
                data_dir=data_dir,
            )
            return

    # git downloads it to data_dir
    try:
        Repo.clone_from(url, Path(data_dir) / project_name)
        print(f"[green]✓ Cloned '{project_name}' successfully.[/green]")
    except exc.GitCommandError as e:
        print(f"[red]Clone failed: {e}[/red]")
        if not ignore_error:
            exit(1)


def _update_template(template_name, data_dir):

    template_path = Path(data_dir) / template_name

    if not _ensure_template_exists(
        None,
        data_dir=data_dir,
        template=template_name,
        print_flag=False,
    ):
        print(
            f"[red]No template named {template_name} found in {data_dir}[/red]"
        )
        return

    # checks if there is .git inside
    if not ".git" in listdir(template_path):
        print(f"[red]Template {template_name} is not a git repository![/red]")
        return

    repo = Repo(template_path)
    # chekcs the status:
    fetch_info = repo.remotes.origin.pull()
    for info in fetch_info:
        if info.flags & info.HEAD_UPTODATE:
            print("[orange1]󰚰 Already up to date![/orange1]")
        else:
            print(f"[green]{template_name} has been updated[/green]")


def parse_link(template_url: str) -> str:
    # TODO: support "host:repo branch=dev"
    # TODO: support "host:repo run=scirpt.sh"
    if ":" in template_url and not template_url.startswith("http"):
        host, path = template_url.split(":", 1)
        if "/" not in path:
            print(
                f"[red]Error: invalid format [cyan]'{template_url}'[/cyan], expected 'host:user/repo'[/red]"
            )
            exit(1)
        if "." in host:
            return f"https://{host}/{path}"
        else:
            return f"https://{host}.com/{path}"

    return template_url


def _sync(args, data_dir):
    _ = args
    urls = get_config_file()
    templates = _list(
        None,
        data_dir=data_dir,
        print_flag=False,
    )
    # for url in urls:
    for url in tqdm(urls, desc="Syncing templates"):
        url = parse_link(url)
        template_name = str(Path(url).stem).replace("_omurtag_template", "")
        print(f"[blue]{template_name}:[/blue]")
        if template_name not in templates:
            pull_args = Namespace(
                link=url,
                recursive=True,
            )
            _pull(
                pull_args,
                data_dir=data_dir,
                ignore_error=True,
            )
        else:
            _update_template(
                template_name=template_name,
                data_dir=data_dir,
            )
