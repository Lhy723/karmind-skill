# Codex 安装

Codex 可以从仓库内的 `.agents/skills` 读取项目级 skill，也可以从 `~/.agents/skills` 读取用户级 skill。

推荐在 LLM Wiki 项目目录内使用项目级轻量安装。不要默认全局安装，也不要把整仓库复制到 wiki 项目里。

## 推荐：不使用 Python 的项目级安装

这个方式只把运行 skill 需要的文件检出到当前项目：

- `SKILL.md`
- `references/`
- `scripts/`
- `agents/`，用于 Codex 的 skill 元数据

macOS / Linux：

```bash
mkdir -p .agents/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .agents/skills/karmind-skill
git -C .agents/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force ".agents\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".agents\skills\karmind-skill"
git -C ".agents\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

安装后，项目里会出现：

```text
.agents/
└── skills/
    └── karmind-skill/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

如果你之前完整复制过仓库，建议删除旧目录后按上面的命令重装。

macOS / Linux：

```bash
rm -rf .agents/skills/karmind-skill
```

Windows PowerShell：

```powershell
Remove-Item -Recurse -Force ".agents\skills\karmind-skill"
```

## 备选：Python 脚本安装

如果你已经有 Python，并希望让安装器处理目录创建，可以先获取本仓库，再运行脚本。这个方式现在也只会复制运行时需要的轻量 skill 文件。

macOS / Linux：

```bash
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
python /tmp/karmind-skill/scripts/install.py --target project-agents --project .
```

Windows PowerShell：

```powershell
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-agents --project .
```

## 可选：用户级安装

只有你明确希望所有项目都能调用这个 skill 时，再安装到用户级目录。

macOS / Linux：

```bash
mkdir -p ~/.agents/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ~/.agents/skills/karmind-skill
git -C ~/.agents/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git "$HOME\.agents\skills\karmind-skill"
git -C "$HOME\.agents\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

如果 skill 没有出现，重启 Codex。

## 更新

项目级安装：

```bash
git -C .agents/skills/karmind-skill pull --ff-only
```

用户级安装：

```bash
git -C ~/.agents/skills/karmind-skill pull --ff-only
```

## 用法

```text
$karmind-skill 初始化当前目录的 LLM Wiki
```

或者：

```text
使用 karmind-skill 摄取新资料。
```

如果缓存中有多个 pending raw 文件，skill 会先询问处理方式，而不是默认只整理第一篇。

健康检查和修复：

```text
使用 karmind-skill 做一次健康检查。
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```
