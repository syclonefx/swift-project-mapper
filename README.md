# Swift Project Mapper Skill

A reusable Skill for creating and maintaining a concise navigation map for Swift and Xcode repositories.

## Installation

Requires Python 3.9 or later for the helper scripts. The scripts use only the Python standard library and inspect repositories locally; they do not send source code or project metadata over the network.

Copy or clone this repository into your coding agent's Skills directory, keeping the directory name as `swift-project-mapper`. For Codex, this is commonly `~/.codex/skills/swift-project-mapper`.

This Skill can also be used with other coding agents that support local skill instructions. Add the guidance below to the agent's repository instructions so it knows when to use the Skill.

Example:

```text
~/.codex/skills/
└── swift-project-mapper/
    ├── SKILL.md
    ├── scripts/
    ├── templates/
    └── references/
```

## Quick Start

1. Install the Skill in your agent's Skills directory.
2. In the Swift or Xcode repository you want to map, ask your agent to use `swift-project-mapper` to create an initial project map.
3. Review the generated `docs/PROJECT-MAP.md` and verify any entries marked `Needs verification:`.
4. Keep the map current when structural or architectural changes affect project navigation.

## Primary Output

The Skill creates or maintains:

```text
docs/PROJECT-MAP.md
```

## Helper Scripts

Generate a mechanical Swift inventory:

```bash
python3 scripts/scan_swift_project.py /path/to/repository \
  --output /path/to/repository/docs/generated-swift-inventory.md
```

Validate paths referenced by a project map:

```bash
python3 scripts/validate_project_map.py \
  /path/to/repository/docs/PROJECT-MAP.md \
  --root /path/to/repository
```
The scripts provide mechanical discovery and validation. The agent should still read source code to produce accurate architectural descriptions.

## Add this to your `AGENTS.md` or `CLAUDE.md`
```
## Project Map Requirements

Before planning or modifying code, check for a project map in the repository.

### Before Starting Work

1. Look for `PROJECT-MAP.md` in the project root and common documentation directories such as:

   * `docs/PROJECT-MAP.md`
   * `.codex/docs/PROJECT-MAP.md`

2. If a project map exists:

   * Read it before searching the repository broadly.
   * Use it to identify the files, targets, features, models, services, and tests relevant to the requested task.
   * Treat the map as a navigation aid, not as a substitute for inspecting the actual source files before editing them.
   * Verify that referenced paths and responsibilities are still accurate.

3. If no project map exists:

   * Run the `swift-project-mapper` Skill located at `swift-project-mapper/SKILL.md`.
   * Generate `PROJECT-MAP.md` before beginning substantial implementation work.
   * Place the generated map in `docs/PROJECT-MAP.md` unless the project already uses another documentation location.

### Keeping the Map Updated

While working, update `PROJECT-MAP.md` whenever a change:

* adds, removes, renames, or moves a file;
* adds or removes an app, framework, extension, widget, test, or package target;
* introduces a major type, model, service, manager, repository, ViewModel, or feature;
* changes the primary responsibility of a documented file or type;
* changes important data flow, dependency relationships, persistence behavior, navigation, or application architecture;
* adds, removes, or relocates tests associated with a documented feature;
* makes an existing project-map entry inaccurate or obsolete.

Do not update the map for minor implementation details that do not affect project navigation or architectural understanding.

### Before Completing Work

Before reporting a task as complete:

1. Review the files changed during the task.
2. Determine whether `PROJECT-MAP.md` needs to be updated.
3. Update any affected entries.
4. Remove or correct stale paths and descriptions discovered during the work.
5. Confirm that newly documented file paths exist.
6. Include project-map changes in the same commit or change set as the code that required them.

The project map must remain concise, accurate, and useful for locating code. Do not turn it into a line-by-line description of the codebase.
```

## License

This project is released under the [MIT License](https://opensource.org/license/mit). 