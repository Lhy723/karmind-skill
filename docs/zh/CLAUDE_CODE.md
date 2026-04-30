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
/plugin marketplace add karmind-local /path/to/karmind-skill
/plugin install karmind-skill@karmind-local
```

如果你移动了仓库路径，把上面的路径改成新的仓库根目录。

### 同步插件分发目录

`plugins/karmind-skill/` 是自包含插件目录，由根目录的 `SKILL.md`、`references/`、`scripts/`、`adapters/` 构建出来。修改这些源文件后运行：

```bash
python scripts/build_claude_plugin.py
```

## 手动安装

Claude Code 也可以从 `~/.claude/skills/<skill-name>/SKILL.md` 读取用户级 skill，或从项目内 `.claude/skills/<skill-name>/SKILL.md` 读取项目级 skill。

### 用户级安装

```bash
python scripts/install.py --target claude-user
```

等价的手动安装方式：

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/karmind-skill ~/.claude/skills/karmind-skill
```

### 项目级安装

```bash
python scripts/install.py --target project-claude --project .
```

## 用法

直接调用：

```text
/karmind-skill ingest new sources
```

或者自然语言描述任务：

```text
请使用 karmind-skill 维护当前目录的 LLM wiki，并处理新资料。
```

体检和修复：

```text
请使用 karmind-skill 做一次健康检查。
请使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```

如果 `.claude/skills` 目录是在 Claude Code 启动后才创建的，可能需要重启 Claude Code。
