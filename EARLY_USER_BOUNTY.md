# Early-User Bounty Claim Draft

Screenshot requirement:

1. Install the Sibyl Memory Plugin
2. Reach 150 requests
3. Get $30 USDC in inference credits

## Verification performed

- Activated Sibyl Memory Plugin via email binding.
- Confirmed `sibyl status`, `sibyl whoami`, and `sibyl health`.
- Ran `scripts/run_early_user_requests.py`.
- Completed 150 MCP memory operations:
  - `memory_remember`
  - `memory_recall`
  - `memory_search`
- Verified the generated memories are searchable with `sibyl memory search`.

## Follow-up natural workload proof

After reviewer feedback that the proof should reflect real plugin usage instead of only targeting the request count, an additional task-oriented workload was run:

- Script: `scripts/run_natural_agent_workload.py`
- Log: `proof/natural-agent-workload-2026-07-06T132810Z.log`
- Workload: 10 project phases, 50 agent work notes, 150 live MCP memory operations
- Tools used:
  - `memory_remember`
  - `memory_recall`
  - `memory_search`

This workload stores and retrieves actual project context from the Sibyl plugin during setup, integration, bounty review, fresh-clone verification, submission hardening, and ticket follow-up.

## Claim text

```text
Claiming the Early-User Bounty.

I installed and activated the Sibyl Memory Plugin, then completed 150 valid MCP memory requests through a Zo/Codex MCP harness.

Proof:
- Account is activated on Sibyl FREE tier
- `sibyl health` returns all green
- 150 MCP memory operations completed successfully
- Operations used live Sibyl Memory Plugin tools, not mocks:
  - memory_remember
  - memory_recall
  - memory_search

Proof repo:
https://github.com/marox-cyber/sibyl-b002-zo-codex

Proof log:
proof/early-user-150-requests-2026-07-06T071414Z.log

Follow-up natural workload proof:
proof/natural-agent-workload-2026-07-06T132810Z.log
```
