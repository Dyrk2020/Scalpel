# Scalpel

Gateway-style [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for IDA Pro. Instead of exposing a single IDA instance to an AI agent, Scalpel puts a stateless gateway between your MCP client (Gemini CLI, Claude Code, Codex, ...) and any number of concurrent IDA Pro backends — GUI or headless — plus a relational SQL query engine, an assembly patching service, and a web-based security dashboard.

Forked from [`mrexodia/ida-pro-mcp`](https://github.com/mrexodia/ida-pro-mcp); now an independent architecture.

## Why a gateway

Single-server MCP setups break down quickly in real RE work: several binaries at once, headless IDA in the background, multiple agents. Scalpel solves this with three ideas:

1. **Dead-drop discovery** — every IDA instance registers by writing JSON metadata (PID, port, auth token) into a shared registry (`~/.ida_mcp_registry` by default).
2. **Watching router** — the gateway monitors the registry with `watchdog`, verifies each backend is alive, and maintains a routing table.
3. **Explicit session IDs** — every tool call carries a `database_id` = `SHA256(absolute_idb_path)[:8]`. Two snapshots of the same binary (`analysis_v1.i64`, `analysis_final.i64`) are distinct addressable sessions; agents hot-swap databases without reconnecting.

## Architecture

```
MCP Client ──► Gateway (stateless) ──► IDA GUI #1
                    │  ▲                IDA headless #2
                    │  └── registry ──► IDA headless #N
                    ▼
     SQL query engine · asm patcher · security dashboard
```

## Layout

| Path | Role |
|---|---|
| `gateway/` | reverse proxy: forwarding, patching, SQL query bridge |
| `ida_mcp/` | IDA-side plugin: backend registry, RPC registry, thread/async marshalling, tools (`analysis`, `debug`, `edit`, `memory`, `query`, `types`, `export`, ...) |
| `frontend/` | security dashboard (web UI) |
| `generators/` | proxy code generator |

## Build & run

```bash
make build     # build the gateway + plugin
make install   # install into IDA plugins dir
make test
```

See [`docs/DESIGN.md`](docs/DESIGN.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

## Acknowledgments

Originally a fork of [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) — credit for the original code belongs to its author and contributors.
