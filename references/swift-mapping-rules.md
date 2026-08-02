# Swift Mapping Rules

## Declaration Types to Detect

Prioritize declarations for:

- `@main`
- `struct`, `class`, `actor`, `enum`, and `protocol`
- `extension`
- SwiftUI `View`
- SwiftData `@Model`
- `@Observable`
- `ObservableObject`
- `AppIntent`
- `Widget` and `WidgetBundle`
- `XCTestCase`
- Swift Testing suites and `@Test`

## Responsibility Inference

Use source evidence in this order:

1. protocol conformances;
2. property wrappers and annotations;
3. initializer dependencies;
4. method names and public API;
5. call sites;
6. filename and directory name.

Do not rely on filename alone when describing responsibility.

## Relationship Mapping

Record relationships that affect navigation or safe editing:

- ownership;
- parent-child model relationships;
- dependency injection;
- protocol implementation;
- service consumers;
- View-to-ViewModel relationships;
- ViewModel-to-store relationships;
- model-to-persistence relationships;
- widget or App Intent dependencies;
- test-to-subject relationships.

Avoid recording every incidental call.

## SwiftUI Notes

For SwiftUI views, record:

- whether the view is a root, screen, container, component, sheet, or row;
- state ownership;
- environment dependencies;
- navigation role;
- associated ViewModel or store;
- platform-specific behavior.

## Concurrency Notes

Record actor isolation when architecturally important:

- `@MainActor` ViewModels or services;
- custom actors;
- `Sendable` boundaries;
- background tasks;
- synchronization primitives.

Do not list actor isolation for every trivial type.

## Persistence Notes

For SwiftData or Core Data models, record:

- required and optional relationships;
- cascade, nullify, or deny deletion behavior when visible;
- uniqueness constraints;
- external storage;
- migration-sensitive fields;
- CloudKit compatibility concerns;
- store or repository responsible for access.

## Tests

Map tests to behavior, not only filenames. Note whether a test covers:

- domain logic;
- persistence;
- networking;
- ViewModel state;
- UI flow;
- integration behavior;
- migration behavior.
