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

## 推荐：一键安装

推荐在目标 wiki 项目目录运行一键安装命令。安装器会询问目标 agent，并且只复制轻量 skill 文件。

macOS / Linux：

```bash
cd your-project
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | bash
```

Windows PowerShell：

```powershell
cd your-project
irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex
```

如果你想跳过询问，可以指定 agent：

macOS / Linux：

```bash
cd your-project
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | KARMIND_AGENT=trae bash
```

Windows PowerShell：

```powershell
cd your-project
$env:KARMIND_AGENT = "trae"; irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex; Remove-Item Env:KARMIND_AGENT
```

可选值：`codex`、`opencode`、`trae`、`claude`、`all`。

## 手动安装

如果不使用 plugin marketplace 或 `skills` CLI，按各 agent 的专用文档手动安装到项目目录。推荐只放轻量 skill 文件：`SKILL.md`、`references/`、`scripts/`；Codex 额外放 `agents/`，Trae 额外放项目规则。

手动安装可以使用文档中的 sparse checkout 命令，也可以从本地 checkout 复制同样的轻量文件到目标目录；不要复制 README、docs、tests、插件分发目录等仓库维护文件。

- Codex / 通用 agent：[CODEX.md](CODEX.md)
- OpenCode：[OPENCODE.md](OPENCODE.md)
- Trae：[TRAE.md](TRAE.md)
- 其他 agent：[OTHER_AGENTS.md](OTHER_AGENTS.md)

Claude Code 推荐使用插件安装；只有在插件不可用时才参考 [CLAUDE_CODE.md](CLAUDE_CODE.md) 的项目级备选方式。

需要用户级安装时，也按对应 agent 文档里的用户级目录手动放入轻量文件。

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

下面的辅助脚本来自本仓库。如果你的当前项目里没有 `scripts/` 目录，请使用 `/tmp/karmind-skill/scripts/...` 形式调用，或者使用已安装 skill 目录里的 `scripts/...`。

Windows PowerShell 用户请使用 `"$env:TEMP\karmind-skill\scripts\..."`。

## 初始化已有笔记

如果目标目录里已经有笔记或文档，先扫描，不要直接移动：

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --scan-existing --language zh
```

如果不是中文 wiki，把 `zh` 换成 `en`，或使用 `auto` 让脚本按已有资料自动判断。对于其他语言，不建议在仓库里维护语言包；让 agent 先复制一份临时 `init_wiki.py`，只本地化人类可读模板文字，再执行这份临时脚本。

用户确认后，把候选文件导入到 `raw/imported/`：

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --import-existing move
```

如果需要保留原文件，用复制：

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --import-existing copy
```

导入后的文件会在 `wiki/cache/ingest-cache.json` 中标记为 `pending`。

## 编译缓存（ingest cache）

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

编译 raw 文章前，把文章引用的本地图片/附件复制到 `wiki/assets/`，并下载在线图片：

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

模型批处理可以把 `--language` 换成其他语言代码；脚本会要求外部模型按该语言生成标题和正文，同时保持机器字段为英文。

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
- 高风险：删除页面、覆盖 source note、重置缓存、批量重新编译、修改 schema 前必须确认。
- 修复缺失的概念页或实体页时，即使只创建占位页，也必须报告本地搜索词、检查过的 wiki/raw 文件、是否联网搜索，以及为什么写入事实内容或只保留待找证据。
- 如果修复需要创建带事实内容的概念页或实体页，agent 应先查本地 wiki/raw；证据不足时调用可用的联网搜索/浏览能力核验权威来源并引用，不能凭常识硬写。

修复完成后，agent 应更新 `wiki/index.md`、追加 `wiki/log.md`，并重新运行体检。
