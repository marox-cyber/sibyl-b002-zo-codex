import asyncio
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
SERVER = os.environ.get("SIBYL_MCP_COMMAND", str(ROOT / ".venv" / "bin" / "sibyl-memory-mcp"))
TARGET_OPS = int(os.environ.get("SIBYL_EARLY_USER_TARGET_OPS", "150"))


async def main() -> None:
    if TARGET_OPS % 3 != 0:
        raise SystemExit("SIBYL_EARLY_USER_TARGET_OPS must be divisible by 3")

    started = datetime.now(timezone.utc).isoformat()
    params = StdioServerParameters(command=SERVER, args=[], env=os.environ.copy())
    completed = []

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = sorted(tool.name for tool in tools.tools)
            required = {"memory_remember", "memory_recall", "memory_search"}
            missing = sorted(required - set(tool_names))
            if missing:
                raise RuntimeError(f"missing expected tools: {missing}")

            cycles = TARGET_OPS // 3
            nonce = int(time.time())
            for i in range(1, cycles + 1):
                name = f"early-user-bounty-{nonce}-{i:03d}"
                body = {
                    "bounty": "early-user",
                    "target": "150 requests",
                    "cycle": i,
                    "surface": "Zo/Codex MCP",
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                }

                remember = await session.call_tool(
                    "memory_remember",
                    {"category": "sibyl-bounty", "name": name, "body": body},
                )
                if remember.isError:
                    raise RuntimeError(f"memory_remember failed at cycle {i}")
                completed.append({"op": len(completed) + 1, "tool": "memory_remember", "name": name})

                recall = await session.call_tool(
                    "memory_recall",
                    {"category": "sibyl-bounty", "name": name},
                )
                if recall.isError:
                    raise RuntimeError(f"memory_recall failed at cycle {i}")
                completed.append({"op": len(completed) + 1, "tool": "memory_recall", "name": name})

                search = await session.call_tool(
                    "memory_search",
                    {"query": name, "limit": 1, "tiers": "entity"},
                )
                if search.isError:
                    raise RuntimeError(f"memory_search failed at cycle {i}")
                completed.append({"op": len(completed) + 1, "tool": "memory_search", "name": name})

                if i % 10 == 0:
                    print(f"completed {len(completed)}/{TARGET_OPS} MCP memory operations", flush=True)

    finished = datetime.now(timezone.utc).isoformat()
    summary = {
        "started_utc": started,
        "finished_utc": finished,
        "target_ops": TARGET_OPS,
        "completed_ops": len(completed),
        "tools": sorted(set(item["tool"] for item in completed)),
        "first_op": completed[0] if completed else None,
        "last_op": completed[-1] if completed else None,
    }
    print(json.dumps(summary, indent=2))

    if len(completed) != TARGET_OPS:
        raise RuntimeError(f"expected {TARGET_OPS} ops, completed {len(completed)}")


if __name__ == "__main__":
    asyncio.run(main())
