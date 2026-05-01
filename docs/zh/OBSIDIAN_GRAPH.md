# Obsidian 关系图谱颜色组推荐

这套颜色组按 LLM Wiki 的知识层级分组，而不是按文件扩展名分组。目标是在 Obsidian Graph View 中快速看出资料从 `raw/` 进入 source note，再流向概念、实体、问题和综合页面的路径。

## 使用方式

在 Obsidian 中打开：

```text
Graph View -> Filters -> Groups -> New group
```

逐条添加下面的 query 和颜色。建议按表格顺序添加；更具体的组放在更前面，避免被宽泛路径覆盖。

## 推荐颜色组

| 顺序 | 名称 | Query | 颜色 | 用途 |
| --- | --- | --- | --- | --- |
| 1 | Source Drafts | `path:wiki/sources/_drafts` | `#A855F7` | 外部模型或未复核 source note 草稿 |
| 2 | Reviewed Sources | `path:wiki/sources -path:wiki/sources/_drafts` | `#2563EB` | 已复核 source notes，是证据到知识页的桥 |
| 3 | Concepts | `path:wiki/concepts` | `#16A34A` | 概念、机制、定义、方法 |
| 4 | Entities | `path:wiki/entities` | `#0891B2` | 人、组织、产品、项目、地点等实体 |
| 5 | Questions | `path:wiki/questions` | `#E11D48` | 开放问题、待验证假设、研究任务 |
| 6 | Synthesis | `path:wiki/synthesis` | `#D97706` | 跨资料综合、比较、模型、结论 |
| 7 | Core Navigation | `path:wiki/index.md OR path:wiki/overview.md OR path:wiki/log.md` | `#6366F1` | 索引、总览、日志 |
| 8 | Assets | `path:wiki/assets OR path:raw/assets` | `#0D9488` | 镜像图片、附件、原始附件 |
| 9 | Raw Evidence | `path:raw -path:raw/assets` | `#71717A` | 原始资料层，不应直接改写 |
| 10 | Reports and Cache | `path:wiki/reports OR path:wiki/cache` | `#64748B` | 体检报告、批处理报告、缓存文件 |

如果你的 Obsidian 版本不支持 `OR` 或负向查询，可以把这些组拆成多条，或者先只配置 `path:wiki/sources/_drafts`、`path:wiki/sources`、`path:wiki/concepts`、`path:wiki/entities`、`path:wiki/questions`、`path:wiki/synthesis`、`path:raw`。

## 设计原则

- 蓝色表示已复核证据层：`wiki/sources/`。
- 绿色表示可复用概念层：`wiki/concepts/`。
- 青色表示实体节点：`wiki/entities/`。
- 红色表示不确定性和待处理问题：`wiki/questions/`。
- 琥珀色表示综合产物：`wiki/synthesis/`。
- 紫色表示草稿，提醒它还不能当作正式知识。
- 灰色表示原始资料、报告和缓存，降低视觉权重。

## 推荐 Graph View 设置

建议先打开：

```text
Show attachments: on
Show existing files only: on
Show orphans: on
```

如果图谱太杂：

```text
Show attachments: off
Show orphans: off
```

如果要检查维护质量：

```text
Show orphans: on
```

孤立的 `concepts/`、`entities/` 或 `synthesis/` 页面通常说明缺少索引、source note 链接或反向链接。

## 可选：标签增强

路径分组已经足够稳定。只有当一个页面跨多个目录职责时，再考虑加标签：

```yaml
tags:
  - llm-wiki/concept
  - llm-wiki/needs-review
```

对应的图谱组可以是：

```text
tag:#llm-wiki/needs-review
```

但不要过早依赖大量标签；目录结构和链接关系应先保持清楚。
