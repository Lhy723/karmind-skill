# 其他 Agent

如果某个 agent 没有原生 Agent Skills 支持，可以使用项目指令文件模式。

推荐只把这些规则放进 LLM Wiki 项目目录，不要放进全局指令，避免普通代码项目也触发 wiki 管理行为。

## AGENTS.md

把 [adapters/AGENTS.md](../../adapters/AGENTS.md) 复制到 wiki 项目根目录，并确保 agent 能访问本 skill 仓库。

## CLAUDE.md

如果 agent 会读取 `CLAUDE.md`，可以把 [adapters/CLAUDE.md](../../adapters/CLAUDE.md) 复制到项目根目录。

## 通用提示词

```text
请读取 karmind-skill 仓库中的 SKILL.md。以后只要我要求你维护当前目录的 LLM wiki，就按照它的工作流执行：把 raw/ 视为不可变资料层，维护 wiki/index.md，向 wiki/log.md 追加记录，给结论保留引用，并记录矛盾和开放问题。普通问答默认从 wiki 出发；修复体检问题时读取 wiki/reports/doctor-report.md，低风险问题直接修，中高风险变更先问我。需要创建事实性概念页或实体页时，先查本地 wiki/raw；证据不足且可联网时，用搜索/浏览核验权威来源并引用，不要凭常识编写。
```

## 推荐项目结构

```text
project/
├── AGENTS.md
├── raw/
└── wiki/
```
