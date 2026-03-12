# 🔨 omurtag

A CLI tool for creating projects from templates.

## Installation

```bash
uv cache clean && uv tool uninstall omurtag && uv tool install .
```

If `omurtag` is not found after installing, run:

```bash
uv tool update-shell
```

## Usage

```bash
omurtag <command> [options]
```

## Commands

### `add` — Add a template

Add a local folder as a template.

```bash
omurtag add <path/to/folder>
```

### `remove` — Remove a template

Remove a template by name.

```bash
omurtag remove <template_name>
```

### `list` — List templates

List all available templates.

```bash
omurtag list
```

### `create` — Create a project

Generate a new project from a template. The project will be created at the given path, resolved relative to your current directory.

```bash
omurtag create <project_name> -t <template_name>
```

**Options:**

| Flag | Description |
|------|-------------|
| `-t`, `--type` | Template to use *(required)* |

**Examples:**

```bash
# Create project in current directory
omurtag create my_project -t python

# Create project two levels up
omurtag create ../../my_project -t python
```

### `pull` — Pull a template from Git

Fetch a template directly from a git repository and add it to your local templates.

```bash
omurtag pull <repo_url>
```

**Options:**

| Flag | Description |
|------|-------------|
| `-r`, `--recursive` | Clone submodules recursively |

**Examples:**

```bash
# Pull a template from GitHub
omurtag pull https://github.com/user/repo_omurtag_template.git

# Pull with submodules
omurtag pull https://github.com/user/repo_omurtag_template.git -r
```

**Requirements:**
- The repository URL must end with `_omurtag_template`
- The repository must be a valid git repository

### `sync` — Sync all templates

Download or update all template repositories mentioned in your configuration file.

```bash
omurtag sync
```

**How it works:**
1. Reads template URLs from your config file (`config.py`)
2. For each URL:
   - If the template doesn't exist locally, it pulls it
   - If the template exists locally, it updates it from the remote
3. Shows progress with a progress bar

**Configuration:**

Create a `config.py` file in one of these locations:
- `XDG_CONFIG_HOME/omurtag/config.py` (XDG compliant)
- `HOME/.omurtag/config.py`

Example `config.py`:

```python
templates = [
    "github:user/repo_omurtag_template",  # Expands to https://github.com/user/repo_omurtag_template
    "gitlab:user/repo_omurtag_template",  # Expands to https://gitlab.com/user/repo_omurtag_template
]
```

## Tips

- Use `omurtag list` to see all available templates before running `create`.
- `project_name` in `create` supports relative paths like `../` or `../../`.
- For `sync` and `pull` commands, make sure you have a valid `config.py` file in the correct location.
- Template repositories must end with `_omurtag_template` to be recognized by the `pull` command.
