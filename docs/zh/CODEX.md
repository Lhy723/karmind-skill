# Codex 安装

Codex 可以从仓库内的 `.agents/skills` 读取项目级 skill，也可以从 `~/.agents/skills` 读取用户级 skill。

推荐优先使用项目级安装，只在 LLM Wiki 所在目录启用这个 skill。

## 推荐：项目级安装

```bash
python scripts/install.py --target project-agents --project .
```

等价的手动安装方式：

```bash
mkdir -p .agents/skills
cp -R /path/to/karmind-skill .agents/skills/karmind-skill
```

## 可选：用户级安装

只有你明确希望所有项目都能调用这个 skill 时，再安装到用户级目录。

```bash
python scripts/install.py --target codex-user
```

等价的手动安装方式：

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/karmind-skill ~/.agents/skills/karmind-skill
```

如果 skill 没有出现，重启 Codex。

## 用法

```text
$karmind-skill 初始化当前目录的 LLM Wiki
```

或者：

```text
使用 karmind-skill 摄取新资料。
```

中文也可以：

```text
使用 karmind-skill 初始化当前目录，并摄取新资料。
```

健康检查和修复：

```text
使用 karmind-skill 做一次健康检查。
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```
