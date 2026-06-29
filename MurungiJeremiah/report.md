# Academic Record System Report

## Overview

The Academic Record System is a console-based CRUD application implemented in `student_management.py`. It stores primary student entries in `students.csv` and keeps supplementary profile details in `students.json`. The application runs from a menu loop that lets the user add, view, search, modify, or remove records.

The design keeps the core CSV storage compact while using JSON for flexible extra information. Logging is written to `student_system.log` for diagnostics and workflow tracing.

## Program Structure

The application is organized into three main groups:

1. Validation functions
   - `validate_reg_number()` enforces the student ID format.
   - `validate_email()` checks email syntax.
   - `validate_gpa()` confirms a numeric GPA within 0.0-5.0.
   - `validate_date()` validates `YYYY-MM-DD` date strings.

2. Storage helpers
   - `_init_csv()`, `load_csv()`, and `save_csv()` are responsible for CSV data management.
   - `_init_json()`, `load_json()`, and `save_json()` handle JSON persistence.

3. CRUD operations
   - `add_student()` creates a new record in both storage systems.
   - `view_all_students()` prints all CSV entries.
   - `search_student()` looks up a record by ID and displays core and extended details.
   - `update_student()` updates existing entries, preserving unchanged fields.
   - `delete_student()` removes an entry from both CSV and JSON after confirmation.

The `main()` function initializes storage, shows the menu, and dispatches the selected action until the user quits.

## Key Functions

### `add_student()`

This function prompts the user for student details, validates the input, checks that the ID is unique, and appends the core fields to `students.csv`. It also writes address, phone, major, and enrollment date into `students.json`.

The function uses `RecordNotFoundError`, `RegistrationAlreadyExistsError`, and `DataValidationError` to manage expected validation and business-rule failures while logging unexpected exceptions.

### `view_all_students()`

This function loads CSV records and displays them in a table with the columns: ID, First, Last, Birth, Email, and Score. It reports when no records are present and logs the number of entries displayed.

### `search_student()`

This function retrieves a record by ID from the CSV storage and enriches the output with supplementary JSON fields. When details exist, it shows Major, Location, Mobile, and Joined.

### `update_student()`

This function finds an existing entry by ID and prompts the user for updated values. Blank responses preserve current values. It updates both the core CSV fields and the supplementary JSON details.

### `delete_student()`

This function confirms that the requested ID exists before prompting the user to delete the entry. If the user does not type `yes`, the removal is cancelled. Otherwise, the entry is removed from both the CSV and JSON stores.

## Exception Handling

The program defines custom exception types for clear separation of user-facing validation errors and system failures:

- `RecordNotFoundError` is raised when the requested ID is not found.
- `RegistrationAlreadyExistsError` is raised when a duplicate ID is entered during creation.
- `DataValidationError` is raised when any input fails validation rules.

CRUD functions catch these exceptions and print friendly messages instead of crashing. File I/O errors in storage helpers are logged and re-raised to make failures easier to diagnose.

## User Interface

The menu labels and prompts have been updated to reflect the current implementation:

- `1. Add New Entry`
- `2. View All Entries`
- `3. Search by ID`
- `4. Modify Entry`
- `5. Remove Entry`
- `6. Quit`

Input prompts and confirmation messages are also adapted to the refactored text, while the underlying logic remains unchanged.

## Storage Details

- `students.csv` stores the core entry fields: `reg_number`, `first_name`, `last_name`, `dob`, `email`, and `gpa`.
- `students.json` stores supplemental details keyed by `reg_number`: `address`, `contact`, `program`, and `enrolled`.

This separation keeps the main academic data tabular and the extended profile information flexible.

## Validation Rules

- Registration IDs must follow the pattern `2x-U-xxxx` or `1x-U-xxxx`.
- Email values must match a standard email structure.
- GPA values must be numeric and between 0.0 and 5.0.
- Dates must use the `YYYY-MM-DD` format.
