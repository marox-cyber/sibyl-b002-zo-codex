# Sibyl B002 - Zo/Codex MCP Harness

Working notes for Sibyl Labs bounty `B002`: ship the Sibyl Memory plugin into a reproducible harness outside the default install path.

## Current proof

This folder verifies the Sibyl MCP server over stdio in a Zo/Codex-style local harness and a Docker Compose harness:

- installs `sibyl-memory-cli` and `sibyl-memory-mcp` in a local Python venv
- runs `sibyl health`
- starts `sibyl-memory-mcp` over stdio
- uses an MCP client to call:
  - `tools/list`
  - `memory_remember`
  - `memory_recall`
- includes Docker/Compose files for a portable MCP server wrapper
- includes Codex MCP config examples for local and Docker execution

## Reproduce locally

```bash
cd /home/workspace/Bounties/sibyl-b002-zo-codex
python3.12 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/sibyl health
.venv/bin/python scripts/verify_mcp_stdio.py
```

## Reproduce with Docker Compose

```bash
cd /home/workspace/Bounties/sibyl-b002-zo-codex
docker compose build
docker compose run --rm verify
```

To run the MCP server as a stdio command from an MCP client:

```bash
docker compose run --rm sibyl-memory-mcp
```

For Codex, copy the relevant block from:

- `examples/codex-config.local.toml`
- `examples/codex-config.docker.toml`

## Verified locally

Package install succeeded with:

- `sibyl-memory-cli==0.3.17`
- `sibyl-memory-mcp==0.1.11`
- `sibyl-memory-client==0.4.15`
- `sibyl-memory-hermes==0.3.11`

`sibyl health` returned all green using the local free-tier database.

`scripts/verify_mcp_stdio.py` successfully called the MCP server and wrote/loaded a test entity from `proof-memory.db`.

Docker is not available in the current Zo container, so the Docker files are scaffolded and statically checked here. The local stdio proof is verified end-to-end.

## Next work

- Add a clean public repo or gist.
- Run the Docker Compose verification in an environment with Docker.
- Claim `B002` in the Sibyl Discord after the proof package is polished.
