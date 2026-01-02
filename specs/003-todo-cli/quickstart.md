# Quickstart: Todo CLI - Phase I

## Overview

This document provides a quick guide to using the Todo CLI application and an overview of its internal module interactions. The application is a simple in-memory todo list manager, allowing users to add, view, update, delete, and complete tasks.

## User Guide (CLI Usage)

The Todo CLI application will expose a set of commands for managing todos.

### Add a new todo

To add a new todo, you will use a command similar to:

```bash
todo add "My new task"
```

This will create a new todo with a unique ID and mark it as incomplete. A confirmation message will be displayed.

### View all todos

To view all existing todos:

```bash
todo list
```

This will display a list of all todos, including their ID, title, and completion status. If no todos exist, an informative message will be shown.

### Mark a todo as completed

To mark an existing todo as completed, provide its ID:

```bash
todo complete 1
```

This will update the todo with ID `1` to a completed state. A confirmation message will be displayed.

### Update a todo's title

To update the title of an existing todo, provide its ID and the new title:

```bash
todo update 1 "Updated task title"
```

This will change the title of the todo with ID `1`. A confirmation message will be displayed.

### Delete a todo

To delete a todo, provide its ID:

```bash
todo delete 1
```

This will remove the todo with ID `1` from the list. A confirmation message will be displayed.

## Internal Module Interactions

The application will follow a clear separation of concerns, as outlined in the `plan.md`'s project structure.

-   **`cli/`**: This module will handle command-line parsing (e.g., using `argparse` or `click`) and dispatch user requests to the `services/` module. It will be responsible for user interaction and output formatting.
-   **`services/`**: This module will contain the core business logic for managing todos. It will interact with the `models/` module to manipulate `Todo` objects. Functions for adding, viewing, updating, deleting, and completing todos will reside here. This module will maintain the in-memory collection of `Todo` objects.
-   **`models/`**: This module will define the `Todo` data structure, including its `id`, `title`, and `completed` fields, as specified in `data-model.md`. It may also include validation logic for `Todo` objects.

The `services/` module acts as the "API" for the `cli/` module, providing the operations required to fulfill user commands. The `models/` module provides the data structures used throughout the application.
