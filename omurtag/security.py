from pathlib import Path
from rich import print
import tomllib
import re

try:
    import requests as _requests
    HAS_REQUESTS = True
except ImportError:
    _requests = None  # type: ignore
    HAS_REQUESTS = False

from .utils import get_config_value

_BASE = "https://api.deps.dev/v3"
_ADV_URL = _BASE + "/advisories/{id}"

_STACK_FILES = {
    "python": ["pyproject.toml", "requirements.txt"],
    "npm": ["package.json"],
    "cargo": ["Cargo.toml"],
    "go": ["go.mod"],
    "maven": ["pom.xml", "build.gradle"],
}


def detect_stacks(project_path: str) -> list[str]:
    p = Path(project_path)
    return [
        stack
        for stack, files in _STACK_FILES.items()
        if any((p / f).exists() for f in files)
    ]


def _get(url: str):
    assert _requests is not None
    return _requests.get(url, timeout=10)


def _pkg_url(system: str, pkg: str, version: str, suffix: str = "") -> str:
    from urllib.parse import quote
    return (
        _BASE
        + f"/systems/{system}/packages/{quote(pkg, safe='')}/versions/{quote(version, safe='')}"
        + suffix
    )


def _advisories(system: str, pkg: str, version: str) -> list[dict]:
    if not version:
        return []
    resp = _get(_pkg_url(system, pkg, version))
    if resp.status_code != 200:
        return []
    keys = resp.json().get("advisoryKeys", [])
    result = []
    for k in keys:
        adv = _get(_ADV_URL.format(id=k["id"]))
        if adv.status_code == 200:
            result.append(adv.json())
    return result


def _transitive(system: str, pkg: str, version: str) -> list[tuple[str, str]]:
    if not version:
        return []
    resp = _get(_pkg_url(system, pkg, version, suffix=":dependencies"))
    if resp.status_code != 200:
        return []
    return [
        (n["versionKey"]["name"], n["versionKey"]["version"])
        for n in resp.json().get("nodes", [])
    ]


def _parse_version(constraint: str) -> str:
    s = constraint.strip()
    m = re.search(r"[><=!~^*]+\s*([0-9][^\s,;]*)", s)
    if m:
        return m.group(1)
    m = re.match(r"^([0-9][^\s,;]*)", s)
    return m.group(1) if m else ""


class DepScanner:
    system: str

    def scan(self, project_path: str, transitive: bool) -> dict[str, list]:
        raise NotImplementedError

    def _collect(
        self, direct: list[tuple[str, str]], transitive: bool
    ) -> dict[str, list]:
        seen: set[tuple[str, str]] = set()
        to_check: list[tuple[str, str]] = []
        for pkg, version in direct:
            if (pkg, version) not in seen:
                seen.add((pkg, version))
                to_check.append((pkg, version))
            if transitive:
                for tp, tv in _transitive(self.system, pkg, version):
                    if (tp, tv) not in seen:
                        seen.add((tp, tv))
                        to_check.append((tp, tv))
        return {pkg: _advisories(self.system, pkg, version) for pkg, version in to_check}


class PypiScanner(DepScanner):
    system = "pypi"

    def scan(self, project_path: str, transitive: bool) -> dict[str, list]:
        p = Path(project_path) / "pyproject.toml"
        if p.exists():
            with open(p, "rb") as f:
                data = tomllib.load(f)
            raw = data.get("project", {}).get("dependencies", [])
            direct = []
            for dep in raw:
                m = re.match(r"^([A-Za-z0-9_\-.]+)", dep)
                if not m:
                    continue
                name = m.group(1).lower().replace("-", "_")
                direct.append((name, _parse_version(dep)))
            return self._collect(direct, transitive)

        return {}


class MavenScanner(DepScanner):
    system = "maven"

    def scan(self, project_path: str, transitive: bool) -> dict[str, list]:
        try:
            from lxml import etree as ET  # pyright: ignore
        except ImportError:
            print("[yellow]lxml not installed, skipping Maven scan[/yellow]")
            return {}
        p = Path(project_path) / "pom.xml"
        if not p.exists():
            return {}
        tree = ET.parse(str(p), ET.XMLParser(recover=True))
        deps = tree.getroot().find("dependencies")
        if deps is None:
            return {}
        direct = []
        for dep in deps:
            try:
                gid = dep.find("groupId").text
                aid = dep.find("artifactId").text
                vn = dep.find("version")
                version = vn.text if vn is not None else ""
                direct.append((f"{gid}:{aid}", version or ""))
            except AttributeError:
                pass
        return self._collect(direct, transitive)


class NpmScanner(DepScanner):
    system = "npm"

    def scan(self, project_path: str, transitive: bool) -> dict[str, list]:
        import json
        p = Path(project_path) / "package.json"
        if not p.exists():
            return {}
        data = json.loads(p.read_text(encoding="utf-8"))
        direct = []
        for section in ("dependencies", "devDependencies"):
            for name, constraint in data.get(section, {}).items():
                version = _parse_version(str(constraint))
                if version:
                    direct.append((name, version))
        return self._collect(direct, transitive)


class CargoScanner(DepScanner):
    system = "cargo"

    def scan(self, project_path: str, transitive: bool) -> dict[str, list]:
        p = Path(project_path) / "Cargo.toml"
        if not p.exists():
            return {}
        with open(p, "rb") as f:
            data = tomllib.load(f)
        direct = []
        for section in ("dependencies", "dev-dependencies", "build-dependencies"):
            for name, constraint in data.get(section, {}).items():
                if isinstance(constraint, dict):
                    version = str(constraint.get("version", ""))
                else:
                    version = str(constraint)
                version = _parse_version(version)
                if version:
                    direct.append((name, version))
        return self._collect(direct, transitive)


class GoScanner(DepScanner):
    system = "go"

    def scan(self, project_path: str, transitive: bool) -> dict[str, list]:
        raise NotImplementedError


_SCANNERS: dict[str, DepScanner] = {
    "python": PypiScanner(),
    "maven": MavenScanner(),
    "npm": NpmScanner(),
    "cargo": CargoScanner(),
    "go": GoScanner(),
}


def _print_results(results: dict[str, list]) -> None:
    for pkg, advisories in results.items():
        if not advisories:
            print(f"  [green]+ {pkg}[/green]")
        else:
            print(f"  [red]! {pkg}[/red]")
            for adv in advisories:
                adv_id = adv.get("advisoryKey", {}).get("id", "?")
                score = adv.get("cvss3Score", "?")
                aliases = adv.get("aliases", [])
                print(f"    {adv_id} | cvss3: {score}")
                for alias in aliases:
                    print(f"      {alias}")


def security_check(project_path: str, stacks: list[str]) -> None:
    if not HAS_REQUESTS:
        print("[yellow]requests not installed, skipping security check[/yellow]")
        return
    transitive: bool = bool(get_config_value("transitive_deps", False))
    for stack in stacks:
        scanner = _SCANNERS.get(stack)
        if scanner is None:
            continue
        try:
            results = scanner.scan(project_path, transitive)
        except NotImplementedError:
            continue
        except Exception as e:
            print(f"[yellow]Security scan skipped ({stack}): {e}[/yellow]")
            continue
        print(f"[blue]Checking {stack} dependencies...[/blue]")
        _print_results(results)
