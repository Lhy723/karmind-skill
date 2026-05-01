# Claude Code 安装

推荐优先使用 Claude Code plugin marketplace 安装。插件安装可以同时携带 skill、脚本和后续扩展配置，比手动复制 skill 目录更适合长期维护。

建议只在 LLM Wiki 项目目录中安装或启用这个插件/skill，不建议默认全局启用。

本仓库根目录包含 Claude Code plugin marketplace 所需文件：

```text
.claude-plugin/marketplace.json
plugins/karmind-skill/.claude-plugin/plugin.json
plugins/karmind-skill/skills/karmind-skill/SKILL.md
```

## 推荐：Plugin 安装

从 GitHub 安装：

```text
/plugin marketplace add karmind-skills Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

使用完整 GitHub URL：

```text
/plugin marketplace add karmind-skills https://github.com/Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

本地开发安装：

```text
/plugin marketplace add karmind-local <local-repo-path>
/plugin install karmind-skill@karmind-local
```

如果你移动了仓库路径，把上面的路径改成新的仓库根目录。

### 同步插件分发目录

`plugins/karmind-skill/` 是自包含插件目录，由根目录的 `SKILL.md`、`references/`、`scripts/`、`adapters/` 构建出来。这个命令只适用于开发者。

macOS / Linux：

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
cd /tmp/karmind-skill
python scripts/build_claude_plugin.py
```

Windows PowerShell：

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
Set-Location "$env:TEMP\karmind-skill"
python scripts/build_claude_plugin.py
```

## 备选：手动安装

Claude Code 也可以从 `~/.claude/skills/<skill-name>/SKILL.md` 读取用户级 skill，或从项目内 `.claude/skills/<skill-name>/SKILL.md` 读取项目级 skill。

推荐只在 LLM Wiki 项目目录中使用项目级轻量安装。

### 推荐：一键安装

在目标 wiki 项目目录运行：

macOS / Linux：

```bash
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | KARMIND_AGENT=claude bash
```

Windows PowerShell：

```powershell
$env:KARMIND_AGENT = "claude"; irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex; Remove-Item Env:KARMIND_AGENT
```

### 项目级安装

macOS / Linux：

```bash
mkdir -p .claude/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .claude/skills/karmind-skill
git -C .claude/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force ".claude\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".claude\skills\karmind-skill"
git -C ".claude\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

### 用户级安装

只有你明确希望所有 Claude Code 项目都能调用这个 skill 时，再安装到用户级目录。

macOS / Linux：

```bash
mkdir -p ~/.claude/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ~/.claude/skills/karmind-skill
git -C ~/.claude/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git "$HOME\.claude\skills\karmind-skill"
git -C "$HOME\.claude\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

## 更新

项目级安装：

```bash
git -C .claude/skills/karmind-skill pull --ff-only
```

用户级安装：

```bash
git -C ~/.claude/skills/karmind-skill pull --ff-only
```

## 用法

直接调用：

```text
/karmind-skill 编译新资料
```

或者自然语言描述任务：

```text
请使用 karmind-skill 维护当前目录的 LLM wiki，并处理新资料。
```

如果缓存中有多个 pending raw 文件，skill 会先询问处理方式，而不是默认只整理第一篇。

体检和修复：

```text
请使用 karmind-skill 做一次健康检查。
请使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```

如果 `.claude/skills` 目录是在 Claude Code 启动后才创建的，可能需要重启 Claude Code。
