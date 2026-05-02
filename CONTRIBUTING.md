# Contributing

## Dev setup

```bash
uv tool install --reinstall .
bash run-test.sh
```

## Code contributions

**Keep PRs small.** Under 100 lines changed is ideal. One thing per PR.

**AI is fine**, but you are responsible for what you submit. Review it, test it, understand it.

**Commits must follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).**
PRs with non-conforming commits will be ignored.

```
feat: add cargo dependency scanning
fix: handle empty replace_dict in replace_in_files
docs: update configuration section
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

## Adding a command

1. Implement in `omurtag/commands.py`
2. Add `case "name":` in `run()` match block
3. Add subparser in `omurtag/__main__.py`
4. Add integration test in `run-test.sh`
5. Update `docs/docs-content.jsx` and `README.md`

## Template contributions

Submit a template via the template submission issue template.

Rules:
- Repo name must end with `_omurtag_template`
- No API keys, secrets, `.env` files, or local config committed
- Include `omurtag.toml` with name, description, stack, and author
- Test it with `omurtag pull` and `omurtag create` before submitting
