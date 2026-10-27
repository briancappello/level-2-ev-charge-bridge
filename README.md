# 9.6 kW Level 2 EV charger on the Pionix ChargeBridge eval board

Design files for a 240 V / 40 A, J1772 tethered, plug-in (NEMA 14-50) EVSE bench unit. A Pionix CB-EVAL v1.2 board with a ChargeBridge EVSE module handles the pilot and safety state machine, and EVerest runs on an external PC.

Open **`cb-l2-evse.html`** in a browser. It contains:

- Two schematic sheets: the power path, and control wiring with board connector pin numbers
- A BOM with vendor links and prices (read 26–27 Oct 2026, US shipping)
- Build notes, plus a 10-step assembly guide with to-scale layout and wiring drawings

> This is a bench test device for private use by someone qualified to work on 240 V equipment. It is not a listed product.

## Get it

Install [Git LFS](https://git-lfs.com) first (`git lfs install`), then clone with the submodule:

```sh
git clone --recurse-submodules <this-repo-url> cb-l2-evse
cd cb-l2-evse
```

If you already cloned without it:

```sh
git submodule update --init
git lfs pull
```

## Contents

| Path | What |
|---|---|
| `cb-l2-evse.html` | The design document |
| `cb-eval-board/` | Pionix CB-EVAL KiCad project (submodule, tag 1.2). Open with KiCad 9.0.3+ |
| `datasheets/` | Manufacturer datasheets for every major part (Git LFS); see `datasheets/README.md` |
| `scripts/` | BOM and assembly generators, KiCad netlister, web lookup tool; see `scripts/README.md` |
| `session/` | The OpenCode session the design was developed in |
| `AGENTS.md` | Project instructions that OpenCode loads automatically |

## Regenerate the document

The build scripts need only Python 3.10+:

```sh
python3 scripts/build_bom.py        # BOM table
python3 scripts/build_assembly.py   # assembly steps and drawings
```

For web lookups (price and datasheet research), set up the Camoufox tool once (about 600 MB):

```sh
scripts/setup.sh
scripts/cfx search "Mean Well HDR-60-24"
```

## Continue the design session in OpenCode

The full design conversation, including every tool call and the reasoning behind each decision, is in `session/cb-l2-evse.opencode-session.json`. To import it with this clone as its working directory:

```sh
opencode session import session/cb-l2-evse.opencode-session.json --directory "$(pwd)"
opencode session list          # find the imported session's ID
opencode -s <session-id>       # open it and keep going
```

The transcript refers to the original machine's paths: `/home/brian/gl` is the repository root, and `~/.local/bin/cfx` is `scripts/cfx`. `AGENTS.md` tells the agent this. Some tools used in the session (an MCP-driven Firefox sandbox, the original subagents) aren't part of this repo. The agent doesn't need them to pick up the work.

## Licensing

The `cb-eval-board` submodule is Pionix's, under CERN-OHL-P-2.0. Each datasheet belongs to its manufacturer and is included for reference.
