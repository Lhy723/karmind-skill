#!/usr/bin/env python3
"""Install karmind-skill into common agent skill directories."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


SKILL_NAME = "karmind-skill"
EXCLUDE_NAMES = {
    ".git",
    ".agents",
    ".claude",
    ".opencode",
    ".trae",
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    ".venv",
    "dist",
    "build",
}


def source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def user_targets() -> dict[str, Path]:
    home = Path.home()
    return {
        "codex-user": home / ".agents" / "skills" / SKILL_NAME,
        "generic-user": home / ".agents" / "skills" / SKILL_NAME,
        "claude-user": home / ".claude" / "skills" / SKILL_NAME,
        "opencode-user": home / ".config" / "opencode" / "skills" / SKILL_NAME,
        "trae-user": home / ".trae" / "skills" / SKILL_NAME,
    }


def project_targets(project: Path) -> dict[str, Path]:
    return {
        "project-agents": project / ".agents" / "skills" / SKILL_NAME,
        "project-claude": project / ".claude" / "skills" / SKILL_NAME,
        "project-opencode": project / ".opencode" / "skills" / SKILL_NAME,
        "project-trae": project / ".trae" / "skills" / SKILL_NAME,
    }


def all_targets(project: Path | None) -> dict[str, Path]:
    targets = user_targets()
    if project:
        targets.update(project_targets(project.resolve()))
    return targets


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def copy_skill(src: Path, dst: Path, force: bool, symlink: bool) -> None:
    src = src.resolve()
    dst = dst.expanduser().resolve()

    if dst.exists() or dst.is_symlink():
        if not force:
            raise FileExistsError(f"{dst} already exists. Use --force to replace it.")
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        else:
            shutil.rmtree(dst)

    dst.parent.mkdir(parents=True, exist_ok=True)

    if symlink:
        dst.symlink_to(src, target_is_directory=True)
        return

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored: set[str] = set()
        directory_path = Path(directory).resolve()
        for name in names:
            item = directory_path / name
            if name in EXCLUDE_NAMES:
                ignored.add(name)
            elif is_relative_to(item, dst):
                ignored.add(name)
        return ignored

    shutil.copytree(src, dst, ignore=ignore)


def copy_trae_project_rules(src: Path, project: Path, force: bool) -> Path:
    dst = project / ".trae" / "rules" / "project_rules.md"
    if dst.exists() and not force:
        raise FileExistsError(f"{dst} already exists. Use --force to replace it.")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src / "adapters" / "trae_project_rules.md", dst)
    return dst


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install karmind-skill into agent skill directories.")
    parser.add_argument("--target", action="append", help="Install target. Repeat for multiple targets.")
    parser.add_argument("--project", type=Path, help="Project root for project-* targets.")
    parser.add_argument("--force", action="store_true", help="Replace an existing installed copy.")
    parser.add_argument("--symlink", action="store_true", help="Symlink instead of copying.")
    parser.add_argument("--list-targets", action="store_true", help="List supported targets and exit.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    project = args.project.resolve() if args.project else None
    targets = all_targets(project)

    if args.list_targets:
        print("User targets:")
        for name, path in user_targets().items():
            print(f"- {name}: {path}")
        print("Project targets:")
        for name in project_targets(Path("<project>")):
            print(f"- {name}: <project>/{project_targets(Path('<project>'))[name].relative_to(Path('<project>'))}")
        print("Notes:")
        print("- project-trae also writes <project>/.trae/rules/project_rules.md")
        return 0

    selected = args.target or ["generic-user"]
    if any(name.startswith("project-") for name in selected) and project is None:
        print("error: --project is required for project-* targets", file=sys.stderr)
        return 2

    unknown = [name for name in selected if name not in targets]
    if unknown:
        print(f"error: unknown target(s): {', '.join(unknown)}", file=sys.stderr)
        print("Run with --list-targets to see valid targets.", file=sys.stderr)
        return 2

    src = source_root()
    if not (src / "SKILL.md").exists():
        print(f"error: {src} does not look like a skill root", file=sys.stderr)
        return 2

    for name in selected:
        dst = targets[name]
        copy_skill(src, dst, force=args.force, symlink=args.symlink)
        mode = "symlinked" if args.symlink else "copied"
        print(f"{mode} {src} -> {dst}")
        if name == "project-trae":
            assert project is not None
            rules_path = copy_trae_project_rules(src, project, args.force)
            print(f"copied {src / 'adapters' / 'trae_project_rules.md'} -> {rules_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
