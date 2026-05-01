# Trae 安装

推荐使用“项目规则 + 完整 skill”组合安装。

- `project_rules.md` 负责告诉 Trae：这个项目是 LLM Wiki，普通问答默认从 wiki 出发。
- `.trae/skills/karmind-skill/` 负责提供完整的 `SKILL.md`、参考文档和脚本。

这样 Trae 不需要全局启用这个能力，也不会影响普通代码项目。

## 推荐：组合安装

macOS / Linux：

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
python /tmp/karmind-skill/scripts/install.py --target project-trae --project .
```

Windows PowerShell：

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-trae --project .
```

安装后，项目里会出现：

```text
.trae/
├── rules/
│   └── project_rules.md
└── skills/
    └── karmind-skill/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── adapters/
```

其中：

- `.trae/rules/project_rules.md` 是 Trae 项目规则入口。
- `.trae/skills/karmind-skill/SKILL.md` 是完整 skill 入口。

## 不使用 Python 的手动安装

如果你不想运行安装脚本，可以手动执行。

macOS / Linux：

```bash
mkdir -p .trae/rules .trae/skills
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
git clone https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force .trae/rules, .trae/skills
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae/rules/project_rules.md"
git clone https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
```

## 只安装项目规则

如果你只想要最小安装，也可以只放项目规则。

macOS / Linux：

```bash
mkdir -p .trae/rules
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force .trae/rules
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae/rules/project_rules.md"
```

这种方式可用，但功能依赖项目规则里的简短说明；推荐组合安装，因为 Trae 可以在需要时读取完整 `SKILL.md`。

## 常用提示

```text
使用 karmind-skill 在当前目录初始化一个 LLM Wiki。先扫描已有笔记或文档，列出候选项，并询问我是移动、复制还是跳过。
```

```text
使用 karmind-skill 摄取新资料。按默认目录寻找待处理资料，创建 source note，更新相关页面，并维护索引、日志和缓存。
```

```text
使用 karmind-skill 做一次健康检查。
```

```text
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```

## 更新

如果使用组合安装，更新完整 skill：

```bash
git -C .trae/skills/karmind-skill pull
```

更新项目规则：

macOS / Linux：

```bash
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```

Windows PowerShell：

```powershell
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae/rules/project_rules.md"
```
