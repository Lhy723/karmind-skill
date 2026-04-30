# Skills CLI Installation

`karmind-skill` supports installation through `npx skills add`. The repository root contains a valid `SKILL.md`, so it can be installed from GitHub or from a local checkout.

Run installation from the LLM Wiki project directory so the skill is scoped to that directory. Do not use `-g` / `--global` unless you intentionally want the skill available in every project.

## Install from GitHub

Install from the published GitHub repository:

```bash
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

Useful flags:

- `--all`: install all skills to all supported agents and skip prompts.
- `-g` / `--global`: install at user scope.
- `--copy`: copy files instead of symlinking.
- `--skill karmind-skill`: install only this skill.
- `--agent '*'`: install to all supported agents.

Examples:

```bash
# Not recommended by default: global install to all supported agents
npx -y skills add Lhy723/karmind-skill -g --all

# List available skills without installing
npx -y skills add Lhy723/karmind-skill --list

# Install only karmind-skill
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

## Install from a Local Checkout

Run this from the repository root:

```bash
npx -y skills add . --list
npx -y skills add . --skill karmind-skill --agent '*' -y
```

During development, the default symlink behavior is useful. To install a standalone copy:

```bash
npx -y skills add . --skill karmind-skill --agent '*' -y --copy
```

## Compatibility Check

The repository should be detected as one skill:

```bash
npx -y skills add . --list
```

Expected output includes:

```text
Found 1 skill
karmind-skill
```

If the CLI reports `No valid skills found`, check that `SKILL.md` frontmatter is valid YAML. In particular, quote `description` when it contains a colon.
