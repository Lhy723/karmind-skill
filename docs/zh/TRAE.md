# Trae 安装

Trae 的项目规则比 skill 目录更稳定，所以推荐先使用项目规则文件。这样 Trae 只会在当前 LLM Wiki 项目里遵守 `karmind-skill` 工作流，不会影响其他项目。

## 推荐：项目规则安装

在你的 LLM Wiki 项目根目录运行：

```bash
mkdir -p .trae/rules
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```

安装后，项目里应该有：

```text
.trae/rules/project_rules.md
```

然后在 Trae 中打开这个项目，直接说：

```text
使用 karmind-skill 在当前目录初始化一个 LLM Wiki。
```

或者：

```text
使用 karmind-skill 摄取新资料。
```

## 可选：安装完整 skill 文件

如果你的 Trae 版本支持读取 `.trae/skills/`，可以把完整仓库放到项目内：

```bash
mkdir -p .trae/skills
git clone https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
```

安装后，项目里应该有：

```text
.trae/skills/karmind-skill/SKILL.md
```

如果 Trae 没有自动读取这个目录，仍然保留上面的项目规则文件即可。项目规则会要求 Trae 在需要维护 wiki 时读取 `karmind-skill` 的 `SKILL.md`。

## 目录建议

推荐最终结构：

```text
your-wiki-project/
├── .trae/
│   ├── rules/
│   │   └── project_rules.md
│   └── skills/
│       └── karmind-skill/
│           └── SKILL.md
├── raw/
└── wiki/
```

只使用项目规则时，`.trae/skills/` 可以不存在。

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

如果使用了 `.trae/skills/karmind-skill`，更新方式：

```bash
git -C .trae/skills/karmind-skill pull
```

如果只使用项目规则，重新下载规则文件即可：

```bash
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```
