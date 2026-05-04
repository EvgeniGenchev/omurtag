# omurtag

A builder for a builder. Scaffold projects from personal templates, with a security audit on every create.

<img width="1200" height="720" alt="omurtag" src="https://github.com/user-attachments/assets/3a54bdf0-ad7b-4373-89bd-9ac4c2378db1" />


## Install

```bash
curl -fsSL https://evgeni-genchev.com/omurtag/install.sh | sh
```

Or directly:

```bash
uv tool install omurtag
# or
pip install omurtag
```

If `omurtag` is not found after installing:

```bash
uv tool update-shell
```

## Commands

```
omurtag {add,remove,create,list,pull,sync,search,audit}

  add      Add a local folder as a template
  remove   Remove a template by name
  create   Generate a project from a template
  list     List templates with stack info
  pull     Pull a template from a git repo
  sync     Download/update all templates from config
  search   Browse and pull from the community template list
  audit    Run a security audit on any project directory
```

### Examples

```bash
# browse community templates and pull interactively
omurtag search

# pull a template from GitHub
omurtag pull github:EvgeniGenchev/fastapi_frontend_omurtag_template

# pull a specific branch
omurtag pull github:user/repo_omurtag_template --branch dev

# list available templates
omurtag list
omurtag list --verbose

# create a project (interactive if no args)
omurtag create
omurtag create ~/projects/myapp --type fastapi_frontend

# add a local folder as a template
omurtag add ~/my_template_folder

# remove a template
omurtag remove fastapi_frontend

# sync all templates from config
omurtag sync

# audit any project directory
omurtag audit
omurtag audit ~/projects/myapp
```

## Configuration

Config file location: `$XDG_CONFIG_HOME/omurtag/config.py` or `~/.omurtag/config.py`

```python
templates = [
    "github:EvgeniGenchev/fastapi_frontend_omurtag_template",
    "gitlab:user/my_project_omurtag_template",
    "codeberg.org:user/tool_omurtag_template",
    "https://codeberg.org/user/repo_omurtag_template.git",
]

# optional
transitive_deps = False  # scan transitive deps on create (slower)
show_desc  = True        # show description in list
show_stack = True        # show stack in list
```

## Creating templates

Any folder can be a template. Use `omurtag add <folder>` to register a local one. To host it so others can pull it, name the repo with a `_omurtag_template` suffix.

**Placeholders** use the `<*name*>` syntax. On `omurtag create`, every placeholder is replaced in file contents, filenames, and directory names. `<*project*>` is always set to the project name. Any other placeholders are prompted for interactively at create time.

**Security audit** runs automatically on every `create`. omurtag detects the stack from marker files (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.) and checks direct dependencies for known CVEs via [deps.dev](https://deps.dev). Opt in to transitive scanning with `transitive_deps = True` in config.

An optional **`omurtag.sh`** at the template root is a post-create setup script. After the project is created, omurtag shows its contents and asks whether to run it in the project directory. It is never copied into created projects.

An optional **`omurtag.toml`** at the template root provides metadata shown in `omurtag list`. It is never copied into created projects.

```toml
[template]
name        = "my-service"
description = "Minimal Python service"
stack       = ["python"]
author      = "you"
```

## Available templates

- [fastapi-frontend](https://github.com/EvgeniGenchev/fastapi_frontend_omurtag_template) — FastAPI backend with Jinja2 HTML frontend
- [jupyter-notebook](https://github.com/EvgeniGenchev/jupyter_notebook_omurtag_template) — Jupyter notebook project with uv
- [neovim-plugin](https://github.com/EvgeniGenchev/neovim_plugin_omurtag_template) — Neovim plugin boilerplate
- [tool-website](https://github.com/EvgeniGenchev/tool_website_omurtag_template) — Single-page tool website with docs, about, and donate pages
- [static-html-website](https://github.com/EvgeniGenchev/static_html_website_omurtag_template) — Static HTML/CSS website
- [typst-coursework](https://github.com/grexdin/typst_coursework_omurtag_template) — Typst coursework document template

Full list: [evgeni-genchev.com/omurtag/templates.json](https://evgeni-genchev.com/omurtag/templates.json)

---

## Dev install

```bash
uv cache clean && uv tool uninstall omurtag && uv tool install .
```

## License

[BSD-3-Clause](LICENSE)
