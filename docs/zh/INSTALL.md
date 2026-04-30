# 安装指南

推荐只在需要维护 LLM Wiki 的项目目录中启用这个 skill，不建议默认全局安装。它会扫描已有文档、维护 `raw/`、更新 `wiki/`，更适合作为某个 wiki 目录的专用能力。

## 推荐：Claude Code Plugin

Claude Code 用户推荐优先使用 plugin marketplace：

```text
/plugin marketplace add karmind-skills Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

更多说明见 [CLAUDE_CODE.md](CLAUDE_CODE.md)。

## Skills CLI

如果你的 agent 支持 `skills` CLI，在目标 wiki 项目目录运行：

```bash
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

更多说明见 [SKILLS_CLI.md](SKILLS_CLI.md)。

## 项目级 Agent 安装

如果不使用 plugin marketplace 或 `skills` CLI，可以用内置脚本安装到当前项目的 agent skill 目录。

Codex / 通用 agent：

```bash
python scripts/install.py --target project-agents --project .
```

Claude Code 项目级 skill：

```bash
python scripts/install.py --target project-claude --project .
```

OpenCode：

```bash
python scripts/install.py --target project-opencode --project .
```

Trae：

```bash
python scripts/install.py --target project-trae --project .
```

查看所有支持的安装目标：

```bash
python scripts/install.py --list-targets
```

## 可选：用户级安装

只有你明确希望所有项目都能调用这个 skill 时，再安装到用户级目录：

```bash
python scripts/install.py --target codex-user
python scripts/install.py --target claude-user
python scripts/install.py --target opencode-user
python scripts/install.py --target trae-user
```

## 开发者本地安装

本地 checkout 预览：

```bash
npx -y skills add . --list
```

安装当前本地目录到当前项目：

```bash
npx -y skills add . --skill karmind-skill --agent '*' -y
```

Claude Code 本地插件安装：

```text
/plugin marketplace add karmind-local /Users/lhy/Project/Prompt/karMind-skill
/plugin install karmind-skill@karmind-local
```

开发本 skill 时可以使用软链接，避免每次修改后重复复制：

```bash
python scripts/install.py --target project-agents --project . --symlink --force
```

## 初始化已有笔记

如果目标目录里已经有笔记或文档，先扫描，不要直接移动：

```bash
python scripts/init_wiki.py . --scan-existing
```

用户确认后，把候选文件导入到 `raw/imported/`：

```bash
python scripts/init_wiki.py . --import-existing move
```

如果需要保留原文件，用复制：

```bash
python scripts/init_wiki.py . --import-existing copy
```

导入后的文件会在 `wiki/cache/ingest-cache.json` 中标记为 `pending`。

## 摄取缓存

保持缓存与 `raw/` 同步：

```bash
python scripts/ingest_cache.py . ensure
python scripts/ingest_cache.py . list --status pending
```

手动整理某个 raw 文件后，标记为已处理：

```bash
python scripts/ingest_cache.py . mark raw/example.md --processor manual-agent --source-note wiki/sources/example.md
```

只有在用户明确要求强制重新提取时，才重置缓存：

```bash
python scripts/ingest_cache.py . reset
```

如果文档很多，agent 应询问用户选择：配置外部模型 API 循环整理，还是由当前 agent 按 pending 缓存逐个手动整理。

模型批处理辅助脚本：

```bash
export LLM_API_KEY="..."
export LLM_MODEL="model-name"
python scripts/model_batch_ingest.py . --limit 10
```

不调用 API，只预览待处理文件：

```bash
python scripts/model_batch_ingest.py . --dry-run
```

API key 配置见 [MODEL_KEYS.md](MODEL_KEYS.md)。推荐使用环境变量或本地 `.env.local`，不要写进 wiki。

## Agent 专用指南

- [Skills CLI](SKILLS_CLI.md)
- [模型 API Key](MODEL_KEYS.md)
- [Codex](CODEX.md)
- [Claude Code](CLAUDE_CODE.md)
- [OpenCode](OPENCODE.md)
- [Trae](TRAE.md)
- [其他 agent](OTHER_AGENTS.md)

## 验证安装

问你的 agent：

```text
What skills are available?
```

或者直接试用：

```text
使用 karmind-skill 在当前目录初始化一个 LLM Wiki。
```

也可以运行本地冒烟测试：

```bash
python scripts/smoke_test.py
```

Wiki 体检报告默认集中写入：

```text
wiki/reports/doctor-report.md
```

## 体检与修复

运行健康检查：

```text
使用 karmind-skill 做一次健康检查。
```

当你明确要求修复时，agent 会读取 `wiki/reports/doctor-report.md`，按风险分级处理：

- 低风险：直接修复明显断链、缺失索引、孤儿页挂接、缺失引用和问题页占位。
- 中风险：合并、拆分、重命名前先给出方案。
- 高风险：删除页面、覆盖 source note、重置缓存、批量重摄取、修改 schema 前必须确认。

修复完成后，agent 应更新 `wiki/index.md`、追加 `wiki/log.md`，并重新运行体检。
