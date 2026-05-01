# OpenCode 安装

OpenCode 支持原生 `.opencode/skills`，也支持全局 `~/.config/opencode/skills`，并兼容 Claude / Agent 风格的 skill 目录。

推荐在 LLM Wiki 项目目录内使用项目级轻量安装。不要默认全局安装，也不要把整仓库复制到 wiki 项目里。

## 推荐：项目级手动安装

这个方式只把运行 skill 需要的文件检出到当前项目：

- `SKILL.md`
- `references/`
- `scripts/`

macOS / Linux：

```bash
mkdir -p .opencode/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .opencode/skills/karmind-skill
git -C .opencode/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force ".opencode\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".opencode\skills\karmind-skill"
git -C ".opencode\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

安装后，项目里会出现：

```text
.opencode/
└── skills/
    └── karmind-skill/
        ├── SKILL.md
        ├── references/
        └── scripts/
```

如果你之前完整复制过仓库，建议删除旧目录后按上面的命令重装。

macOS / Linux：

```bash
rm -rf .opencode/skills/karmind-skill
```

Windows PowerShell：

```powershell
Remove-Item -Recurse -Force ".opencode\skills\karmind-skill"
```

## 可选：用户级安装

只有你明确希望所有 OpenCode 项目都能调用这个 skill 时，再使用：

macOS / Linux：

```bash
mkdir -p ~/.config/opencode/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ~/.config/opencode/skills/karmind-skill
git -C ~/.config/opencode/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git "$HOME\.config\opencode\skills\karmind-skill"
git -C "$HOME\.config\opencode\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

## 权限配置

如果你的 OpenCode 配置限制了 skill 使用，需要允许 `karmind-skill`：

```json
{
  "permission": {
    "skill": {
      "karmind-skill": "allow"
    }
  }
}
```

## 更新

项目级安装：

```bash
git -C .opencode/skills/karmind-skill pull --ff-only
```

用户级安装：

```bash
git -C ~/.config/opencode/skills/karmind-skill pull --ff-only
```

## 用法

```text
加载 karmind-skill，并对当前 LLM wiki 做一次健康检查。
```

摄取新资料时，如果缓存中有多个 pending raw 文件，skill 会先询问处理方式，而不是默认只整理第一篇。

```text
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```
