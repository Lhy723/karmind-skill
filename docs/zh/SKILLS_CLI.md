# Skills CLI 安装

`karmind-skill` 支持通过 `npx skills add` 安装。仓库根目录包含合法的 `SKILL.md`，所以既可以从 GitHub 安装，也可以从本地 checkout 安装。

推荐在 LLM Wiki 项目目录中运行安装命令，让 skill 只对这个目录生效。除非你确定所有项目都需要这个能力，否则不要加 `-g` / `--global`。

## 从 GitHub 安装

从已发布的 GitHub 仓库安装：

```bash
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

常用参数：

- `--all`：安装所有 skill 到所有支持的 agent，并跳过确认。
- `-g` / `--global`：安装到用户级目录。
- `--copy`：复制文件，而不是软链接。
- `--skill karmind-skill`：只安装这个 skill。
- `--agent '*'`：安装到所有支持的 agent。

示例：

```bash
# 不推荐默认使用：用户级安装到所有支持的 agent
npx -y skills add Lhy723/karmind-skill -g --all

# 只预览仓库中有哪些 skill，不安装
npx -y skills add Lhy723/karmind-skill --list

# 只安装 karmind-skill
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

## 从本地目录安装

在本仓库根目录运行：

```bash
npx -y skills add . --list
npx -y skills add . --skill karmind-skill --agent '*' -y
```

开发时如果希望安装目录跟随当前仓库变化，可以使用默认软链接行为；如果希望安装一份独立副本，使用：

```bash
npx -y skills add . --skill karmind-skill --agent '*' -y --copy
```

## 兼容性检查

本仓库应能被 CLI 识别为一个 skill：

```bash
npx -y skills add . --list
```

预期能看到：

```text
Found 1 skill
karmind-skill
```

如果显示 `No valid skills found`，优先检查 `SKILL.md` frontmatter 是否是合法 YAML，尤其是 `description` 中包含冒号时必须加引号。
