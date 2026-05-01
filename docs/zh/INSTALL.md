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

如果不使用 plugin marketplace 或 `skills` CLI，推荐按各 agent 的专用文档做不依赖 Python 的项目级轻量安装。它们都只检出运行时需要的 `SKILL.md`、`references/`、`scripts/`，不会把整仓库复制到 wiki 项目里。

- Codex / 通用 agent：[CODEX.md](CODEX.md)
- OpenCode：[OPENCODE.md](OPENCODE.md)
- Trae：[TRAE.md](TRAE.md)
- 其他 agent：[OTHER_AGENTS.md](OTHER_AGENTS.md)

Claude Code 推荐使用插件安装；只有在插件不可用时才参考 [CLAUDE_CODE.md](CLAUDE_CODE.md) 的项目级备选方式。

如果你已经有 Python，也可以使用内置安装脚本作为备选。先获取仓库：

```bash
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
```

然后在目标 LLM Wiki 项目目录中运行对应目标，例如：

```bash
python /tmp/karmind-skill/scripts/install.py --target project-agents --project .
python /tmp/karmind-skill/scripts/install.py --target project-opencode --project .
python /tmp/karmind-skill/scripts/install.py --target project-trae --project .
```

Windows PowerShell 用户把 `/tmp/karmind-skill/scripts/install.py` 替换为 `"$env:TEMP\karmind-skill\scripts\install.py"`。

查看所有支持的安装目标：

```bash
python /tmp/karmind-skill/scripts/install.py --list-targets
```

## 可选：用户级安装

只有你明确希望所有项目都能调用这个 skill 时，再安装到用户级目录：

```bash
python /tmp/karmind-skill/scripts/install.py --target codex-user
python /tmp/karmind-skill/scripts/install.py --target claude-user
python /tmp/karmind-skill/scripts/install.py --target opencode-user
python /tmp/karmind-skill/scripts/install.py --target trae-user
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
/plugin marketplace add karmind-local <local-repo-path>
/plugin install karmind-skill@karmind-local
```

开发本 skill 时可以使用软链接，避免每次修改后重复复制：

```bash
python scripts/install.py --target project-agents --project . --symlink --force
```

下面的辅助脚本同样来自本仓库。如果你的当前项目里没有 `scripts/` 目录，请使用 `/tmp/karmind-skill/scripts/...` 形式调用。

Windows PowerShell 用户请使用 `"$env:TEMP\karmind-skill\scripts\..."`。

## 初始化已有笔记

如果目标目录里已经有笔记或文档，先扫描，不要直接移动：

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --scan-existing --language zh
```

如果不是中文 wiki，把 `zh` 换成 `en`，或使用 `auto` 让脚本按已有资料自动判断。

用户确认后，把候选文件导入到 `raw/imported/`：

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --import-existing move
```

如果需要保留原文件，用复制：

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --import-existing copy
```

导入后的文件会在 `wiki/cache/ingest-cache.json` 中标记为 `pending`。

## 摄取缓存

保持缓存与 `raw/` 同步：

```bash
python /tmp/karmind-skill/scripts/ingest_cache.py . ensure
python /tmp/karmind-skill/scripts/ingest_cache.py . list --status pending
```

手动整理某个 raw 文件后，标记为已处理：

```bash
python /tmp/karmind-skill/scripts/ingest_cache.py . mark raw/example.md --processor manual-agent --source-note wiki/sources/example.md
```

只有在用户明确要求强制重新提取时，才重置缓存：

```bash
python /tmp/karmind-skill/scripts/ingest_cache.py . reset
```

## 图片和附件镜像

摄取 raw 文章前，把文章引用的本地图片/附件复制到 `wiki/assets/`，并下载在线图片：

macOS / Linux：

```bash
python /tmp/karmind-skill/scripts/mirror_assets.py . raw/example.md
```

Windows PowerShell：

```powershell
python "$env:TEMP\karmind-skill\scripts\mirror_assets.py" . raw/example.md
```

镜像结果记录在 `wiki/cache/assets-cache.json`。如果只想预览，不复制也不下载：

```bash
python /tmp/karmind-skill/scripts/mirror_assets.py . raw/example.md --dry-run
```

如果文档很多，agent 应询问用户选择：配置外部模型 API 循环整理，还是由当前 agent 按 pending 缓存逐个手动整理。

模型批处理辅助脚本：

macOS / Linux：

```bash
export LLM_API_KEY="..."
export LLM_MODEL="model-name"
python /tmp/karmind-skill/scripts/model_batch_ingest.py . --limit 10 --language zh
```

Windows PowerShell：

```powershell
$env:LLM_API_KEY = "..."
$env:LLM_MODEL = "model-name"
python "$env:TEMP\karmind-skill\scripts\model_batch_ingest.py" . --limit 10 --language zh
```

不调用 API，只预览待处理文件：

macOS / Linux：

```bash
python /tmp/karmind-skill/scripts/model_batch_ingest.py . --dry-run --language zh
```

Windows PowerShell：

```powershell
python "$env:TEMP\karmind-skill\scripts\model_batch_ingest.py" . --dry-run --language zh
```

API key 配置见 [MODEL_KEYS.md](MODEL_KEYS.md)。推荐使用环境变量或本地 `.env.local`，不要写进 wiki。

默认情况下，模型批处理只生成待复核草稿到 `wiki/sources/_drafts/`，并把缓存标记为 `drafted`。当前 agent 复核原文和草稿、整理正式 source note、更新相关页面后，才应标记为 `processed`。只有明确接受低质量批量输出时，才使用 `--publish-final-source-notes` 直接写入 `wiki/sources/`。

## Agent 专用指南

- [Skills CLI](SKILLS_CLI.md)
- [模型 API Key](MODEL_KEYS.md)
- [Obsidian 关系图谱](OBSIDIAN_GRAPH.md)
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
python /tmp/karmind-skill/scripts/smoke_test.py
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
- 如果修复需要创建带事实内容的概念页或实体页，agent 应先查本地 wiki/raw；证据不足时调用可用的联网搜索/浏览能力核验权威来源并引用，不能凭常识硬写。

修复完成后，agent 应更新 `wiki/index.md`、追加 `wiki/log.md`，并重新运行体检。
