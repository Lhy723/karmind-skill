# OpenCode 安装

OpenCode 支持原生 `.opencode/skills`，也支持全局 `~/.config/opencode/skills`，并兼容 Claude / Agent 风格的 skill 目录。

推荐只在 LLM Wiki 项目目录使用项目级安装。

## 推荐：项目级安装

如果使用安装脚本，先获取本仓库。

macOS / Linux：

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
```

Windows PowerShell：

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
```

然后在目标 LLM Wiki 项目目录中运行。

macOS / Linux：

```bash
python /tmp/karmind-skill/scripts/install.py --target project-opencode --project .
```

Windows PowerShell：

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-opencode --project .
```

## 可选：用户级安装

只有你明确希望所有 OpenCode 项目都能调用这个 skill 时，再使用：

macOS / Linux：

```bash
python /tmp/karmind-skill/scripts/install.py --target opencode-user
```

Windows PowerShell：

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target opencode-user
```

等价的手动安装方式。

macOS / Linux：

```bash
mkdir -p ~/.config/opencode/skills
cp -R /path/to/karmind-skill ~/.config/opencode/skills/karmind-skill
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode\skills"
Copy-Item -Recurse -Force "C:\path\to\karmind-skill" "$HOME\.config\opencode\skills\karmind-skill"
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

## 用法

```text
加载 karmind-skill，并对当前 LLM wiki 做一次健康检查。
```

或者：

```text
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```
