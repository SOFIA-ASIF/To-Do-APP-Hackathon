---
id: 1
title: Todo CLI - Phase I Specification
stage: spec
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-cli
branch: 003-todo-cli
user: unknown
command: /sp.specify
labels: [spec, todo-cli, feature-generation]
links:
  spec: specs/003-todo-cli/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-todo-cli/spec.md
  - specs/003-todo-cli/checklists/requirements.md
tests: null
---

## Prompt

FEATURE: Todo CLI — Phase I

ACTOR
- User

GOAL
- Manage a list of todos from the command line during a single runtime session.

SCOPE
- Add todo
- View todos
- Update todo
- Delete todo
- Mark todo as completed
- In-memory storage only

DATA MODEL
- Todo:
  - id: integer (auto-increment, unique)
  - title: string (required)
  - completed: boolean (default: false)

BEHAVIOR

1. Add Todo
- User provides a non-empty title.
- System assigns a unique ID.
- Todo is stored in memory.
- Confirmation message is shown.

2. View Todos
- System displays all todos.
- Each todo shows ID, title, and completion status.
- Todos are listed in creation order.
- If no todos exist, display an informative message.

3. Update Todo
- User provides a valid todo ID and a new non-empty title.
- System updates the title.
- ID and completion status remain unchanged.
- Confirmation message is shown.

4. Delete Todo
- User provides a valid todo ID.
- Todo is removed from memory.
- Confirmation message is shown.

5. Complete Todo
- User

## Response snapshot

The specification for "Todo CLI - Phase I" has been successfully created. All checklist items have passed, and the specification is ready for the planning phase (`/sp.plan`).

## Outcome

- ✅ Impact: Successfully generated the feature specification for Todo CLI - Phase I.
- 🧪 Tests: No tests were executed as this was a specification generation task.
- 📁 Files: Two files were created: `specs/003-todo-cli/spec.md` and `specs/003-todo-cli/checklists/requirements.md`.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The spec was successfully generated based on the user's input. All checklist items passed. The next step is planning the implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: N/A
