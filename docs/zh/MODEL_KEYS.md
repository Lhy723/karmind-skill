# 模型 API Key 配置

`karmind-skill` 的模型批处理脚本使用 OpenAI-compatible `/chat/completions` API。你可以使用 OpenAI、兼容 OpenAI API 的网关，或自托管兼容服务。

## 推荐方式

优先使用环境变量，不要把真实 API key 写入 wiki 页面、source note、log 或报告。

```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="model-name"
export LLM_API_KEY="sk-..."
```

然后在 wiki 项目目录运行：

```bash
python scripts/model_batch_ingest.py . --dry-run
python scripts/model_batch_ingest.py . --limit 10
```

## 本地 `.env.local`

如果你不想每次都 `export`，可以在 wiki 项目根目录创建 `.env.local`：

```bash
cp .env.example .env.local
```

如果当前 wiki 项目里没有 `.env.example`，也可以直接创建 `.env.local` 并写入下面的字段。

填写：

```dotenv
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=model-name
LLM_API_KEY=sk-...
```

`.gitignore` 已排除 `.env` 和 `.env.*`，但保留 `.env.example`。不要提交 `.env.local`。

## 兼容变量名

脚本会按顺序读取：

- `LLM_API_KEY`，也兼容 `OPENAI_API_KEY`
- `LLM_MODEL`，也兼容 `OPENAI_MODEL`
- `LLM_BASE_URL`，也兼容 `OPENAI_BASE_URL`

命令行参数 `--api-key`、`--model`、`--base-url` 可以覆盖环境变量，但不推荐把 key 写进 shell history。

## 安全建议

- 为 wiki 批处理创建单独 API key。
- 给 key 设置限额和可撤销权限。
- 不要把 key 写进 `AGENTS.md`、`wiki/log.md`、`wiki/reports/` 或任何 source note。
- 如果 key 泄露，立即在服务商控制台撤销。
