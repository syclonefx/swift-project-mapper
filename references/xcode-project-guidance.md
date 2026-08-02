# Xcode Project Guidance

## Project Containers

Prefer `.xcworkspace` when both workspace and project files exist.

Record:

- applications;
- frameworks;
- extensions;
- widgets;
- packages;
- unit tests;
- UI tests.

## Target Membership

Do not assume a Swift file belongs to every target because it is inside the repository.

Inspect target membership when:

- code is shared across iOS and macOS;
- a file is platform-specific;
- an extension cannot see a type;
- duplicate symbol or missing symbol errors are possible;
- a change adds a new file;
- conditional compilation is used.

## Build Settings

Document only settings that affect architecture or common edits, such as:

- deployment targets;
- Swift language version;
- default actor isolation;
- strict concurrency;
- bundle identifiers;
- code signing or capabilities when relevant;
- generated Info.plist behavior;
- custom build configurations.

## Capabilities and Entitlements

Map capabilities that influence code paths:

- iCloud and CloudKit;
- push notifications;
- App Groups;
- background modes;
- Sign in with Apple;
- associated domains;
- keychain access groups;
- sandbox permissions;
- health, location, camera, or photo access.

## Packages

Record direct package dependencies and the target using each package. Avoid inventorying transitive dependencies unless they are directly relevant.

## Assets and Resources

Record important resources such as:

- asset catalogs;
- Core Data models;
- localization catalogs;
- privacy manifests;
- configuration files;
- bundled JSON or databases;
- intent definition files in older projects.
