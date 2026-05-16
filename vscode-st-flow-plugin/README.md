# ST Flow Runner (VSCode Extension)

This extension runs `full_process.py` in your workspace and visualizes:

- Live process logs
- Stage status (`build -> clarify -> retrieve -> generate -> fix -> evaluate`)
- Intermediate artifacts in `output/<runId>/<project>/...`

## Commands

- `ST Flow: Open Monitor Panel`
- `ST Flow: Run Full Process`

## Prerequisites

- Open this repository root in VSCode.
- Python environment can run `full_process.py`.
- Environment variables (`ZHIZENGZENG_API_KEY`, etc.) are already configured in your shell/environment.
- Node.js + npm installed (for building this extension).

## Development

```bash
cd vscode-st-flow-plugin
npm install
npm run compile
```

Then press `F5` in VSCode to launch Extension Development Host.

## Usage

1. Run command: `ST Flow: Run Full Process`
2. Select project under `dataset/query`
3. Optionally set case filter and skip flags
4. Watch logs and intermediate files in `ST Flow Monitor`

Click an artifact item to:
- preview in panel
- open source file in editor

## Notes

- This extension currently invokes:
  - `python full_process.py --result_dir <runId> --project <project> ...`
- The panel refreshes artifacts every 2 seconds while process is running.
