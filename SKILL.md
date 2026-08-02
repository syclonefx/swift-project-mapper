---
name: swift-project-mapper
description: Maps and documents Swift and Xcode projects so coding agents can quickly locate relevant files, understand the project architecture, and navigate the codebase without repeatedly scanning the entire repository.
metadata:
  author: Chuck Perdue
  version: 1.0
---

# Swift Project Mapper

## Purpose

Create and maintain a concise, accurate map of a Swift or Xcode repository so an agent can navigate the project without repeatedly scanning the entire codebase.

The project map is a routing index. It does not replace reading the source files involved in a requested change.

## When to Use

Use this Skill when:

- onboarding to an existing Swift or Xcode project;
- creating an initial `PROJECT-MAP.md`;
- locating files relevant to a requested change;
- documenting a multi-target Apple-platform application;
- updating documentation after structural or architectural changes;
- validating whether an existing project map is stale;
- reducing broad repository scans during future coding tasks.

## Supported Project Types

This Skill is designed for repositories containing one or more of the following:

- SwiftUI applications;
- UIKit or AppKit applications;
- Swift packages;
- iOS, iPadOS, macOS, watchOS, tvOS, or visionOS targets;
- widgets;
- App Intents;
- app extensions;
- test targets;
- SwiftData, Core Data, GRDB, SQLite, CloudKit, or file-based persistence.

## Default Outputs

Create the following file unless the repository defines another location:

- `docs/PROJECT-MAP.md`

Create supporting files only when the project is large enough to justify them:

- `docs/ARCHITECTURE.md`
- `docs/DEPENDENCY-MAP.md`
- `docs/features/<FEATURE>.md`

Do not create multiple documents that duplicate the same information.

## Operating Modes

### 1. Initial Mapping

Use when no reliable project map exists.

### 2. Map-Assisted Navigation

Use when handling a coding task in a repository that already has a project map.

### 3. Map Refresh

Use after significant structural changes or when the existing map appears stale.

### 4. Validation

Use to verify that documented files, types, targets, and relationships still exist.

## Initial Mapping Workflow

1. Read repository instructions first:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.github/copilot-instructions.md`
   - `README.md`
   - relevant files under `docs/`
2. Inspect the top-level repository structure.
3. Identify project containers:
   - `.xcodeproj`
   - `.xcworkspace`
   - `Package.swift`
4. Identify products and targets.
5. Identify application and extension entry points.
6. Group source files by feature and architectural responsibility.
7. Identify important models, services, stores, ViewModels, views, coordinators, managers, and shared utilities.
8. Identify test targets and connect tests to the code they cover.
9. Identify cross-cutting systems:
   - persistence;
   - networking;
   - dependency injection;
   - navigation;
   - notifications;
   - logging;
   - synchronization;
   - background work;
   - App Intents;
   - widgets;
   - extensions.
10. Write or update `docs/PROJECT-MAP.md` using the supplied template.
11. Verify every documented path and type against the repository.
12. Record uncertainty instead of guessing.

## Map-Assisted Navigation Workflow

Before changing code:

1. Read the repository instructions.
2. Read only the relevant section of `docs/PROJECT-MAP.md` when possible.
3. Identify the likely feature, target, source files, tests, and dependencies.
4. Inspect the actual source files before editing them.
5. Inspect direct callers, direct dependencies, protocols, extensions, and associated tests when relevant.
6. Expand beyond the mapped area only when:
   - the map is incomplete;
   - a referenced type cannot be found;
   - shared behavior may be affected;
   - build configuration or target membership is involved;
   - tests reveal additional dependencies;
   - the requested change crosses feature boundaries.
7. After editing, determine whether the map needs to be updated.

Never make a code change solely from the project map without reading the relevant implementation.

## Swift-Specific Discovery Rules

### Application Entry Points

Look for:

- types conforming to `App`;
- `@main` declarations;
- `UIApplicationDelegate` or `NSApplicationDelegate` implementations;
- scene delegates;
- extension entry points;
- widget bundles;
- App Intents entry points.

### SwiftUI

Identify:

- `View` conformances;
- root views;
- feature views;
- navigation containers;
- sheets, popovers, inspectors, and commands;
- environment dependencies;
- observable state objects;
- reusable view components.

Do not list every small private view unless it is shared, architecturally important, or commonly edited.

### State and ViewModels

Identify types using or conforming to:

- `@Observable`;
- `ObservableObject`;
- `@MainActor`;
- custom state containers;
- reducers or stores;
- dependency containers.

Document ownership and responsibility, not every stored property.

### Persistence

Identify:

- SwiftData `@Model` types;
- Core Data model files and managed object subclasses;
- GRDB records, migrations, database pools, and repositories;
- CloudKit containers and synchronization services;
- file-based stores;
- keychain wrappers;
- UserDefaults-backed settings.

Document important relationships, deletion behavior, migrations, and the primary persistence access layer.

### Networking

Identify:

- API clients;
- endpoint definitions;
- request and response models;
- authentication services;
- caching layers;
- mock clients;
- transport protocols.

### App Extensions and Platform Features

Identify and map:

- widgets and WidgetKit configuration;
- App Intents and entities;
- Share extensions;
- notification service or content extensions;
- Safari extensions;
- menu bar extras;
- background tasks;
- Live Activities;
- watch complications;
- Spotlight integration;
- URL schemes and universal links.

### Tests

Identify:

- Swift Testing suites and `@Test` declarations;
- XCTest cases;
- UI tests;
- test fixtures;
- mocks, fakes, and spies;
- test support utilities.

Connect test files to the feature or service they validate.

### Xcode Project Configuration

When target configuration matters, inspect:

- `.pbxproj` target and file membership;
- build configurations;
- entitlements;
- capabilities;
- Info.plist settings;
- asset catalogs;
- package dependencies;
- build phases;
- schemes when relevant.

Do not manually summarize the entire `.pbxproj`. Extract only information useful for project navigation and safe edits.

## Classification Rules

Classify files by their primary responsibility:

- App entry and composition;
- Feature UI;
- ViewModels or state;
- Models and domain types;
- Persistence;
- Networking;
- Services;
- Navigation;
- Shared UI;
- Utilities and extensions;
- Platform integrations;
- Resources;
- Tests;
- Build and configuration.

When a file has multiple responsibilities, document the dominant responsibility and note important secondary roles.

## Detail Level

Include:

- path;
- major types;
- one- or two-sentence responsibility summary;
- target or platform when not obvious;
- important direct dependencies;
- associated tests;
- important ownership or data-flow relationships.

Exclude by default:

- every function;
- every property;
- private implementation details;
- generated code;
- build artifacts;
- dependency source code;
- long directory dumps;
- obvious boilerplate.

## Common Change Paths

Add a `Common Change Paths` section for frequently modified systems. Examples:

- add or edit a task;
- change persistence behavior;
- add a model property;
- change notification scheduling;
- add an App Intent;
- change widget data;
- add a settings option;
- modify app navigation;
- add a new target.

Each path should list the smallest reasonable set of files to inspect first.

## Generated and Curated Content

When using automation, keep generated inventory separate from human- or agent-curated architectural notes.

Use markers such as:

```markdown
<!-- BEGIN GENERATED INVENTORY -->
<!-- END GENERATED INVENTORY -->

<!-- BEGIN CURATED NOTES -->
<!-- END CURATED NOTES -->
```

Scripts may replace generated sections but must not overwrite curated notes.

## Map Update Rules

Update the map when a change:

- adds, removes, renames, or moves a source file;
- introduces or removes a target;
- introduces a major type, service, store, or feature;
- changes the primary responsibility of a type;
- changes ownership or data flow;
- changes persistence architecture or model relationships;
- changes major navigation structure;
- changes platform or extension integration;
- adds or removes an important dependency;
- moves tests or changes the test strategy.

Do not update the map for minor implementation-only changes that do not affect navigation or architecture.

## Accuracy Rules

- Never invent paths, types, targets, capabilities, or relationships.
- Verify every path before documenting it.
- Prefer source code over filenames as evidence of responsibility.
- Prefer project configuration over assumptions about target membership.
- Mark uncertain findings with `Needs verification:`.
- Remove stale entries when confirmed obsolete.
- Keep descriptions concise.
- Do not copy entire source files into documentation.

## Staleness Checks

Treat the map as potentially stale when:

- documented files are missing;
- important new directories are absent;
- referenced types have been renamed;
- target structure differs from the map;
- the requested change cannot be reconciled with the documented architecture;
- recent commits contain broad moves or refactors.

When stale, inspect the affected area and refresh only the relevant sections unless a full remap is necessary.

## Completion Checklist

Before completing a mapping task:

- all documented paths exist;
- all listed major types exist;
- application and extension entry points are represented;
- targets and platforms are accurately described;
- persistence and major services are represented;
- important tests are linked to their subjects;
- common change paths are useful and concise;
- uncertainty is explicitly marked;
- generated output did not overwrite curated notes.

Before completing a coding task:

- the relevant project-map section was consulted;
- the actual implementation files were read;
- direct dependencies and tests were inspected as needed;
- the map was updated only if navigation or architecture changed.

## Included Resources

- `templates/PROJECT-MAP.template.md`
- `templates/FEATURE-MAP.template.md`
- `templates/ARCHITECTURE.template.md`
- `references/swift-mapping-rules.md`
- `references/xcode-project-guidance.md`
- `scripts/scan_swift_project.py`
- `scripts/validate_project_map.py`
