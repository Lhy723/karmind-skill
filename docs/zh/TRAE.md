# Trae 安装

Trae 的 skill / rules 支持会随版本变化。优先使用 `.trae/skills` 形式；如果当前版本没有原生 skill 入口，就使用项目规则文件指向本 skill。

推荐只在 LLM Wiki 项目目录启用这个 skill 或项目规则。

## 项目级 Skill 安装

```bash
python scripts/install.py --target project-trae --project .
```

等价的手动安装方式：

```bash
mkdir -p .trae/skills
cp -R /path/to/karmind-skill .trae/skills/karmind-skill
```

## 项目规则兜底方案

把 [adapters/trae_project_rules.md](../../adapters/trae_project_rules.md) 复制到：

```text
.trae/rules/project_rules.md
```

然后确保项目中可以访问本仓库，或者把 skill 安装到 `.trae/skills/karmind-skill`。

## 用法

```text
使用 karmind-skill workflow 初始化这个 LLM wiki，摄取新资料，并维护默认索引和日志。
```

```text
使用 karmind-skill 做一次健康检查。
使用 karmind-skill 修复最新体检报告中的问题。不要删除页面；需要合并、拆分或重命名时先问我。
```
