# Trae 安装

推荐在 wiki 项目目录内使用“项目规则 + 轻量 skill”组合安装。

- `project_rules.md` 负责告诉 Trae：这个项目是 LLM Wiki，普通问答默认从 wiki 出发。
- `.trae/skills/karmind-skill/` 只放 Trae 需要读取的 skill 内容：`SKILL.md`、`references/` 和 `scripts/`。
- 安装使用 Git sparse checkout，不会把仓库里的 README、docs、adapters、测试文件等无关文件下载到项目里。

这样 Trae 不需要全局启用这个能力，也不会影响普通代码项目。

## 推荐：一键安装

在目标 wiki 项目目录运行：

macOS / Linux：

```bash
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | KARMIND_AGENT=trae bash
```

Windows PowerShell：

```powershell
$env:KARMIND_AGENT = "trae"; irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex; Remove-Item Env:KARMIND_AGENT
```

## 备选：项目级手动组合安装

macOS / Linux：

```bash
mkdir -p .trae/rules .trae/skills
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
git -C .trae/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force ".trae\rules", ".trae\skills"
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae\rules\project_rules.md"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".trae\skills\karmind-skill"
git -C ".trae\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
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
        └── scripts/
```

其中：

- `.trae/rules/project_rules.md` 是 Trae 项目规则入口。
- `.trae/skills/karmind-skill/SKILL.md` 是 skill 工作流入口。
- 仓库里的 `adapters/AGENTS.md` 是给通用 agent 使用的适配文件，Trae 不需要它。推荐安装方式不会把 `adapters/` 放进 `.trae/skills/karmind-skill/`，因此不会和 `.trae/rules/project_rules.md` 混淆。

如果你之前按旧文档完整 clone 过仓库，建议删除旧目录后重新安装：

```bash
rm -rf .trae/skills/karmind-skill
```

PowerShell：

```powershell
Remove-Item -Recurse -Force ".trae\skills\karmind-skill"
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
New-Item -ItemType Directory -Force ".trae\rules"
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae\rules\project_rules.md"
```

这种方式可用，但功能依赖项目规则里的简短说明；推荐组合安装，因为 Trae 可以在需要时读取完整 `SKILL.md`。

## 常用提示

```text
使用 karmind-skill 在当前目录初始化一个 LLM Wiki。先扫描已有笔记或文档，列出候选项，并询问我是移动、复制还是跳过。
```

```text
使用 karmind-skill 编译新资料。按默认目录寻找待处理资料，创建 source note，更新相关页面，并维护索引、日志和缓存。
```

如果有多个 pending raw 文件，skill 应先询问使用外部模型批处理、当前 agent 手动循环处理、只处理下一篇，还是暂缓。

```text
使用 karmind-skill 做一次健康检查。
```

```text
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```

## 更新

如果使用推荐的组合安装，更新轻量 skill：

```bash
git -C .trae/skills/karmind-skill pull --ff-only
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
  -OutFile ".trae\rules\project_rules.md"
```
