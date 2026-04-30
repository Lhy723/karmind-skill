# 安全说明

本 skill 设计为 local-first，内置辅助脚本只使用 Python 标准库。

启用任何第三方 skill 之前，建议先审查：

- `SKILL.md`
- `scripts/` 下的脚本
- 安装脚本
- agent 专用规则文件

如果 wiki 涉及敏感资料：

- 不要把私有 raw sources 提交到公开仓库。
- 摄取前移除密钥、token、个人隐私和商业敏感信息。
- 模型 API key 使用环境变量或本地 `.env.local`，不要写入 wiki 页面、日志或报告。
- 不要把机密原文粘贴进未获批准的托管 agent。
- 对敏感研究优先使用本地 agent 或受控工作区。
- 把 agent 生成的 wiki 结论视为草稿，重要内容需要人工复核。

更多说明见 [MODEL_KEYS.md](MODEL_KEYS.md)。
