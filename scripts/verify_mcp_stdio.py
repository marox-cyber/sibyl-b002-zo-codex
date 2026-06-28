import asyncio
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
SERVER = os.environ.get("SIBYL_MCP_COMMAND", str(ROOT / ".venv" / "bin" / "sibyl-memory-mcp"))
DB = os.environ.get("SIBYL_MEMORY_DB", str(ROOT / "proof-memory.db"))


async def main() -> None:
    child_env = os.environ.copy()
    child_env["SIBYL_MEMORY_DB"] = DB

    params = StdioServerParameters(
        command=SERVER,
        args=[],
        env=child_env,
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            expected = {"memory_remember", "memory_recall", "memory_search", "memory_list"}
            missing = sorted(expected - set(tool_names))
            if missing:
                raise RuntimeError(f"missing expected tools: {missing}")
            print("TOOLS", tool_names)

            remember = await session.call_tool(
                "memory_remember",
                {
                    "category": "bounty",
                    "name": "B002-zo-codex-proof",
                    "body": {
                        "status": "mcp stdio call succeeded",
                        "surface": "Zo/Codex harness",
                    },
                },
            )
            print("REMEMBER", remember.content[0].text if remember.content else remember)
            if remember.isError:
                raise RuntimeError("memory_remember returned an MCP error")

            recall = await session.call_tool(
                "memory_recall",
                {
                    "category": "bounty",
                    "name": "B002-zo-codex-proof",
                },
            )
            print("RECALL", recall.content[0].text if recall.content else recall)
            if recall.isError:
                raise RuntimeError("memory_recall returned an MCP error")


if __name__ == "__main__":
    asyncio.run(main())
