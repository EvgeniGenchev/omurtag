from rich import print


class TemplateConfig:
    def __init__(self, link: str, branch: str | None = None) -> None:
        self.branch = branch
        self.host: str
        self.path: str
        self.parse_link(link)

    def parse_link(self, template_url: str):
        template_url = template_url.strip()

        parts = template_url.split(" ", 1)
        base = parts[0]
        if len(parts) == 2:
            modifier = parts[1]
            if modifier.startswith("branch="):
                self.branch = modifier.replace("branch=", "")

        base = base.removesuffix(".git")

        if base.startswith("https://") or base.startswith("http://"):
            base = base.split("://", 1)[1]
            slash_idx = base.index("/")
            self.host = base[:slash_idx]
            self.path = base[slash_idx+1:]

        elif ":" in base:
            self.host, self.path = base.split(":", 1)

        elif "/" in base:
            slash_idx = base.index("/")
            self.host = base[:slash_idx]
            self.path = base[slash_idx + 1:]

        else:
            print(f"[red]{template_url} is not a valid template URL![/red]")
            exit(1)

        if "/" not in self.path:
            print(
                f"[red]Error: invalid format [cyan]'{template_url}'[/cyan], "
                f"expected 'host:user/repo'[/red]"
            )
            exit(1)


    @property
    def url(self) -> str:
        assert self.host
        if "." in self.host:
            return f"https://{self.host}/{self.path}"
        else:
            return f"https://{self.host}.com/{self.path}"



_url = "https://github.com/EvgeniGenchev/repo"
assert (TemplateConfig("https://github.com/EvgeniGenchev/repo").url) == _url
assert (TemplateConfig("https://github.com/EvgeniGenchev/repo.git").url) == _url
assert (TemplateConfig("github:EvgeniGenchev/repo.git").url) == _url
assert (TemplateConfig("github:EvgeniGenchev/repo").url) == _url 
assert (TemplateConfig("github.com:EvgeniGenchev/repo").url) == _url
