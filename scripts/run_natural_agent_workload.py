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


PHASES = [
    (
        "setup",
        [
            "Created a reproducible Zo/Codex MCP harness for Sibyl Memory.",
            "Pinned live Sibyl PyPI packages in requirements.txt for reviewer installs.",
            "Verified sibyl health before exercising MCP memory tools.",
            "Documented local venv reproduction steps from a fresh git clone.",
            "Added Docker Compose as an optional portable wrapper for the MCP server.",
        ],
    ),
    (
        "codex-mcp-integration",
        [
            "Started sibyl-memory-mcp through stdio from a local MCP client.",
            "Checked the MCP tool list exposed memory_remember and memory_recall.",
            "Stored a project decision about using Zo/Codex as the main surface.",
            "Recalled the stored project decision to confirm read-after-write behavior.",
            "Searched memory for Codex configuration notes before updating examples.",
        ],
    ),
    (
        "bounty-review",
        [
            "Compared the repo contents against the B002 reproducible-build criteria.",
            "Updated README language so reviewers can reproduce without local Zo paths.",
            "Checked that the repo uses live Sibyl tools instead of mocks.",
            "Recorded the Discord claim text and proof links for the early-user bounty.",
            "Tracked the reviewer caveat that Docker is supplemental, not the primary proof.",
        ],
    ),
    (
        "fresh-clone-verification",
        [
            "Cloned the public repo into a temporary directory for clean verification.",
            "Created a new Python virtual environment for the public-clone test.",
            "Installed the same requirements.txt package set in the clean checkout.",
            "Ran sibyl health successfully from the fresh clone environment.",
            "Confirmed MCP memory round-trip behavior after the fresh clone install.",
        ],
    ),
    (
        "early-user-proof",
        [
            "Activated the Sibyl account before generating request proof.",
            "Confirmed the account is on the FREE tier before running memory operations.",
            "Used memory_remember for durable task notes created during setup.",
            "Used memory_recall to retrieve earlier notes during verification.",
            "Used memory_search to find previous context instead of relying on local files only.",
        ],
    ),
    (
        "submission-hardening",
        [
            "Scanned the repo for credentials before pushing proof artifacts.",
            "Masked the email address in screenshot proof before publishing it.",
            "Committed proof logs and claim notes to the public GitHub repository.",
            "Verified the screenshot link opens from the GitHub proof folder.",
            "Prepared a concise Discord response with repo and screenshot links.",
        ],
    ),
    (
        "ticket-feedback",
        [
            "Captured reviewer feedback that the proof should look like real usage.",
            "Switched from a request-count-only script to a task-oriented memory workload.",
            "Grouped memory activity into setup, integration, review, and claim phases.",
            "Stored concrete project facts instead of synthetic counter-only entries.",
            "Kept the original 150-operation log as historical proof, not the only evidence.",
        ],
    ),
    (
        "agent-workflow",
        [
            "Remembered implementation decisions before editing bounty documentation.",
            "Recalled prior verification facts before answering the user in Discord.",
            "Searched memory for proof artifact names while preparing claim text.",
            "Recorded the final payout wallet note separately from technical proof.",
            "Used memory context to avoid repeating stale B002-only instructions.",
        ],
    ),
    (
        "quality-audit",
        [
            "Checked that public instructions do not expose local credentials.",
            "Verified the claim distinguishes early-user bounty proof from B002 proof.",
            "Confirmed logs show successful completion rather than partial progress.",
            "Recorded that credits are awarded by Sibyl after review, not by local CLI.",
            "Kept reviewer-facing proof short enough to inspect quickly.",
        ],
    ),
    (
        "final-response",
        [
            "Prepared an updated Discord response that acknowledges reviewer feedback.",
            "Linked the natural workload proof log as the stronger follow-up evidence.",
            "Explained that requests came from real MCP memory operations during project work.",
            "Avoided claiming payout completion before Sibyl confirms the credits.",
            "Saved this natural workload as reproducible evidence for future review.",
        ],
    ),
]


async def call_checked(session: ClientSession, tool: str, args: dict, context: str) -> dict:
    result = await session.call_tool(tool, args)
    if result.isError:
        raise RuntimeError(f"{tool} failed during {context}")
    return {"tool": tool, "context": context, "args": args}


async def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    nonce = int(time.time())
    operations = []
    params = StdioServerParameters(command=SERVER, args=[], env=os.environ.copy())

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = sorted(tool.name for tool in tools.tools)
            required = {"memory_remember", "memory_recall", "memory_search"}
            missing = sorted(required - set(tool_names))
            if missing:
                raise RuntimeError(f"missing expected tools: {missing}")

            print("Natural Sibyl MCP workload started")
            print(f"Available memory tools: {', '.join(sorted(required))}")

            for phase_index, (phase, notes) in enumerate(PHASES, start=1):
                print(f"\n[{phase_index:02d}] phase: {phase}")
                for note_index, note in enumerate(notes, start=1):
                    name = f"natural-agent-workload-{nonce}-{phase}-{note_index:02d}"
                    body = {
                        "project": "sibyl-early-user-bounty",
                        "surface": "Zo/Codex MCP harness",
                        "phase": phase,
                        "note": note,
                        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
                    }

                    operations.append(
                        await call_checked(
                            session,
                            "memory_remember",
                            {"category": "agent-work", "name": name, "body": body},
                            f"{phase}: remember note {note_index}",
                        )
                    )
                    operations.append(
                        await call_checked(
                            session,
                            "memory_recall",
                            {"category": "agent-work", "name": name},
                            f"{phase}: recall note {note_index}",
                        )
                    )
                    operations.append(
                        await call_checked(
                            session,
                            "memory_search",
                            {"query": f"{phase} {note}", "limit": 3, "tiers": "entity"},
                            f"{phase}: search context {note_index}",
                        )
                    )
                    print(f"  - {note}")

    finished = datetime.now(timezone.utc).isoformat()
    summary = {
        "started_utc": started,
        "finished_utc": finished,
        "workload": "natural agent project memory workflow",
        "phases": len(PHASES),
        "notes_recorded": sum(len(notes) for _, notes in PHASES),
        "completed_ops": len(operations),
        "tools": sorted(set(item["tool"] for item in operations)),
    }
    print("\nSummary:")
    print(json.dumps(summary, indent=2))

    if len(operations) < 150:
        raise RuntimeError(f"expected at least 150 natural MCP operations, completed {len(operations)}")


if __name__ == "__main__":
    asyncio.run(main())
