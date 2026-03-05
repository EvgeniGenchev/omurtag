# 🔨 omurtag

A CLI tool for creating projects from templates.

## Installation

```bash
uv tool install .
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

Fetch a template directly from a git repository.

```bash
omurtag pull <repo_url>
```

## Tips

- Use `omurtag list` to see all available templates before running `create`.
- `project_name` in `create` supports relative paths like `../` or `../../`.
