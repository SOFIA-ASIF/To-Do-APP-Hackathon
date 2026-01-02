# Tasks: Todo CLI - Phase I

**Feature Branch**: `003-todo-cli` | **Date**: 2026-01-02 | **Spec**: specs/003-todo-cli/spec.md
**Input**: Feature specification (`spec.md`) and Implementation Plan (`plan.md`)

## Overview

This document outlines the granular, independently executable tasks for implementing the Todo CLI - Phase I feature. Tasks are organized into sequential phases, with user stories prioritized and broken down into smaller, actionable steps.

## Implementation Strategy

The implementation will follow an MVP (Minimum Viable Product) approach, prioritizing core user stories (P1) first to deliver foundational functionality. Subsequent stories will be implemented incrementally, ensuring each delivered increment is independently testable and stable.

## Phase 1: Setup (Project Initialization)

**Description**: This phase focuses on setting up the basic project structure and environment.

- [ ] T001 Create project directories: `src/cli/`, `src/models/`, `src/services/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [ ] T002 Initialize Python project with UV and `pyproject.toml`

## Phase 2: Foundational (Core Data Model)

**Description**: This phase establishes the core `Todo` data model, a prerequisite for all user stories.

- [ ] T003 Create `Todo` data model in `src/models/todo.py`

## Phase 3: User Story 1 - Add a new todo (P1)

**Goal**: Users want to add new tasks to their todo list.
**Independent Test**: Successfully add a todo and verify its presence in the list.

- [ ] T004 [US1] Implement `add_todo` logic in `src/services/todo_service.py`
- [ ] T005 [US1] Create CLI command for adding a todo in `src/cli/commands.py`

## Phase 4: User Story 2 - View all todos (P1)

**Goal**: Users want to see all their current tasks and their status.
**Independent Test**: Successfully view a list of todos, including newly added ones.

- [ ] T006 [US2] Implement `get_all_todos` logic in `src/services/todo_service.py`
- [ ] T007 [US2] Create CLI command for viewing todos in `src/cli/commands.py`

## Phase 5: User Story 3 - Mark a todo as completed (P2)

**Goal**: Users want to mark tasks as finished once they are done.
**Independent Test**: Mark a todo as completed and verify its status update when viewing the list.

- [ ] T008 [US3] Implement `complete_todo` logic in `src/services/todo_service.py`
- [ ] T009 [US3] Create CLI command for completing a todo in `src/cli/commands.py`

## Phase 6: User Story 4 - Update an existing todo (P2)

**Goal**: Users want to modify the title of an existing task.
**Independent Test**: Update a todo's title and verify the change when viewing the list.

- [ ] T010 [US4] Implement `update_todo_title` logic in `src/services/todo_service.py`
- [ ] T011 [US4] Create CLI command for updating a todo's title in `src/cli/commands.py`

## Phase 7: User Story 5 - Delete an existing todo (P3)

**Goal**: Users want to remove tasks they no longer need.
**Independent Test**: Delete a todo and verify its absence when viewing the list.

- [ ] T012 [US5] Implement `delete_todo` logic in `src/services/todo_service.py`
- [ ] T013 [US5] Create CLI command for deleting a todo in `src/cli/commands.py`

## Phase 8: Polish & Cross-Cutting Concerns

**Description**: This phase addresses error handling, comprehensive testing, and overall application robustness.

- [ ] T014 Implement error handling and user feedback messages across CLI and services
- [ ] T015 Integrate tests (unit, integration, contract) for all functionalities in `tests/`

## Dependencies

- Phase 1 (Setup) must complete before Phase 2 (Foundational).
- Phase 2 (Foundational) must complete before any User Story Phases.
- User Story Phases are largely independent but are ordered by priority (P1, then P2, then P3).
- Phase 8 (Polish) can begin once core functionalities are in place but will span across all implemented stories.

## Parallel Execution Opportunities

While tasks within a user story are generally sequential, some parallelization may be possible in later stages (e.g., writing different test types concurrently for a single story, or writing implementation and tests for different independent stories).

- **US1**: T004 and T005 are largely sequential for initial setup.
- **US2**: T006 and T007 are largely sequential for initial setup.
- **P2 Stories (US3, US4)**: Implementation of `todo_service.py` logic and `cli/commands.py` for each can be done in parallel with other P2 stories once P1 stories are stable.
- **P3 Story (US5)**: Implementation for `todo_service.py` logic and `cli/commands.py` for US5 can be done in parallel with other stories once P1/P2 are stable.

## MVP Scope

The Minimum Viable Product (MVP) for this feature includes completing **User Story 1 (Add a new todo)** and **User Story 2 (View all todos)**, along with their associated setup and foundational tasks. This provides basic todo management functionality.
