import csv
import json
import logging
import os
import re
from datetime import datetime
from typing import Any


STUDENT_CSV  = "students.csv"
DETAILS_JSON = "students.json"
ACTIVITY_LOG  = "student_system.log"

# Field definitions for storage
FIELD_NAMES = ["reg_number", "first_name", "last_name", "dob", "email", "gpa"]

# Configure activity tracking
logging.basicConfig(
    filename=ACTIVITY_LOG,
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Exception Classes
class RecordNotFoundError(Exception):
    """Raised when no record matches the provided identifier."""
    pass


class RegistrationAlreadyExistsError(Exception):
    """Raised when attempting to create a record with an existing identifier."""
    pass


class DataValidationError(Exception):
    """Raised when input data does not meet requirements."""
    pass


# Input validation functions
def validate_reg_number(reg: str) -> str:
    """
    Verify registration number format (2[0-5]-U-xxx for recent, 1[0-9]-U-xxx for older).
    """
    reg = reg.strip().upper()
    if not re.match(r"^([2][0-5]|[1][0-9])-U-[\d]{4,5}$", reg):
        raise DataValidationError(
            "Registration number must match pattern 2x-U-xxxx "
            "(e.g., 24-U-00001)."
        )
    return reg


def validate_email(email: str) -> str:
    """Check email format validity; raise error if invalid."""
    email = email.strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise DataValidationError(f"'{email}' is not a valid email format.")
    return email


def validate_gpa(gpa_str: str) -> float:
    """
    Verify GPA is numeric and within acceptable range (0.0-5.0).
    """
    try:
        gpa = float(gpa_str)
    except ValueError:
        raise DataValidationError("GPA must be a number (e.g., 3.5).")
    if not (0.0 <= gpa <= 5.0):
        raise DataValidationError("GPA must be between 0.0 and 5.0.")
    return round(gpa, 2)


def validate_date(date_str: str) -> str:
    """Ensure date follows YYYY-MM-DD format."""
    date_str = date_str.strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise DataValidationError("Date format must be YYYY-MM-DD (e.g., 2002-05-14).")
    return date_str

# File initialization routines
def _init_csv() -> None:
    """Initialize CSV storage with headers if absent."""
    if not os.path.exists(STUDENT_CSV):
        with open(STUDENT_CSV, "w") as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
            writer.writeheader()
        logger.info("CSV storage created: %s", STUDENT_CSV)


def load_csv() -> list[dict]:
    """Retrieve all records from CSV storage."""
    _init_csv()
    records: list[dict[str, Any]] = []
    try:
        with open(STUDENT_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except OSError as e:
        logger.error("CSV read failed: %s", e)
        raise
    return records


def save_csv(records: list[dict[str, Any]]) -> None:
    """Write records to CSV storage."""
    try:
        with open(STUDENT_CSV, "w") as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(records)
    except OSError as e:
        logger.error("CSV write failed: %s", e)
        raise


# JSON-based detail storage
def _init_json() -> None:
    """Set up JSON storage if needed."""
    if not os.path.exists(DETAILS_JSON):
        with open(DETAILS_JSON, "w") as f:
            json.dump({}, f, indent=4)
        logger.info("JSON storage created: %s", DETAILS_JSON)


def load_json() -> dict[str, dict[str, Any]]:
    """Retrieve extended details from JSON storage."""
    _init_json()
    try:
        with open(DETAILS_JSON, "r") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logger.error("JSON read failed: %s", e)
        raise
    return data


def save_json(data: dict[str, Any]) -> None:
    """Save extended details to JSON storage."""
    try:
        with open(DETAILS_JSON, "w") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        logger.error("JSON write failed: %s", e)
        raise


# CRUD Operations
def add_student() -> None:
    """
    Insert new record; raise RegistrationAlreadyExistsError if duplicate ID.
    """
    print("\n--- Insert New Record ---")
    logger.info("Operation: Add New Entry")

    try:
        # Gather user information
        reg_number = validate_reg_number(input("ID Number (e.g., 24-U-xxxxx): "))
        first_name = input("Given Name: ").strip()
        last_name  = input("Family Name: ").strip()

        if not first_name or not last_name:
            raise DataValidationError("Both names are required.")

        dob   = validate_date(input("Birth Date (YYYY-MM-DD): "))
        email = validate_email(input("Email: "))
        gpa   = validate_gpa(input("Academic Score (0.0-5.0): "))

        # Gather additional information
        address = input("Residence: ").strip()
        contact = input("Phone: ").strip()
        program = input("Field of Study (e.g., BSc Computer Science): ").strip()

        # Verify uniqueness of ID
        records = load_csv()
        if any(r["reg_number"] == reg_number for r in records):
            raise RegistrationAlreadyExistsError(
                f"An entry with ID '{reg_number}' is already registered."
            )

        # Store core information
        records.append({
            "reg_number": reg_number,
            "first_name": first_name,
            "last_name":  last_name,
            "dob":        dob,
            "email":      email,
            "gpa":        gpa,
        })
        save_csv(records)

        # Store supplementary information
        details = load_json()
        details[reg_number] = {
            "address": address,
            "contact": contact,
            "program": program,
            "enrolled": datetime.today().strftime("%Y-%m-%d"),
        }
        save_json(details)

        print(f"\nRecord for '{first_name} {last_name}' successfully created.")
        logger.info("Entry added: %s (%s %s)", reg_number, first_name, last_name)

    except (RegistrationAlreadyExistsError, DataValidationError) as e:
        print(f"\nError: {e}")
        logger.warning("Add operation failed: %s", e)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        logger.error("Unexpected error in add_student: %s", e)
    finally:
        logger.debug("add_student() completed.")


def view_all_students() -> None:
    """Show all stored records in tabular format."""
    print("\n--- All Records ---")
    logger.info("Operation: View All Entries")

    try:
        records = load_csv()

        if not records:
            print("No records available.")
            logger.info("View all: database empty.")
            return

        # Display table
        print(f"\n{'ID':<14} {'First':<14} {'Last':<14} "
              f"{'Birth':<12} {'Email':<28} {'Score'}")
        print("-" * 90)
        for r in records:
            print(f"{r['reg_number']:<14} {r['first_name']:<14} {r['last_name']:<14} "
                  f"{r['dob']:<12} {r['email']:<28} {r['gpa']}")
        print(f"\nTotal entries: {len(records)}")
        logger.info("View all: retrieved %d records.", len(records))

    except Exception as e:
        print(f"\n  Unable to fetch records: {e}")
        logger.error("Error in view_all_students: %s", e)
    finally:
        logger.debug("view_all_students() completed.")


def search_student() -> None:
    """
    Look up record by ID and display core + extended information.
    Raises RecordNotFoundError if ID not found.
    """
    print("\n--- Lookup Record ---")
    logger.info("Operation: Search Entry")

    try:
        reg_number = validate_reg_number(input("Enter ID to search for: "))

        records = load_csv()
        match   = next((r for r in records if r["reg_number"] == reg_number), None)

        if match is None:
            raise RecordNotFoundError(
                f"No entry with ID '{reg_number}' exists."
            )

        # Show primary information
        print(f"\n{'─'*45}")
        print(f"  ID          : {match['reg_number']}")
        print(f"  Person      : {match['first_name']} {match['last_name']}")
        print(f"  Birth Date  : {match['dob']}")
        print(f"  Email       : {match['email']}")
        print(f"  Score       : {match['gpa']}")

        # Show supplementary information
        details = load_json()
        if reg_number in details:
            d = details[reg_number]
            print(f"  Major       : {d.get('program', 'N/A')}")
            print(f"  Location    : {d.get('address', 'N/A')}")
            print(f"  Mobile      : {d.get('contact', 'N/A')}")
            print(f"  Joined      : {d.get('enrolled', 'N/A')}")
        print(f"{'─'*45}")

        logger.info("Search: located %s.", reg_number)

    except (RecordNotFoundError, DataValidationError) as e:
        print(f"\n  {e}")
        logger.warning("Search failed: %s", e)
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        logger.error("Unexpected error in search_student: %s", e)
    finally:
        logger.debug("search_student() completed.")


def update_student() -> None:
    """
    Find record by ID and modify fields. Leave blank to preserve existing values.
    """
    print("\n--- Modify Entry ---")
    logger.info("Operation: Update Entry")

    try:
        reg_number = validate_reg_number(input("Enter ID to modify: "))

        records = load_csv()
        idx     = next((i for i, r in enumerate(records) if r["reg_number"] == reg_number), None)

        if idx is None:
            raise RecordNotFoundError(
                f"No entry with ID '{reg_number}' found."
            )

        student = records[idx]
        print(f"\nModifying: {student['first_name']} {student['last_name']}")
        print("(Hit Enter to skip field)\n")

        # Modify primary fields
        new_first = input(f"Given Name [{student['first_name']}]: ").strip()
        new_last  = input(f"Family Name [{student['last_name']}]: ").strip()
        new_dob   = input(f"Birth Date [{student['dob']}]: ").strip()
        new_email = input(f"Email [{student['email']}]: ").strip()
        new_gpa   = input(f"Score [{student['gpa']}]: ").strip()

        if new_first: student["first_name"] = new_first
        if new_last:  student["last_name"]  = new_last
        if new_dob:   student["dob"]        = validate_date(new_dob)
        if new_email: student["email"]      = validate_email(new_email)
        if new_gpa:   student["gpa"]        = validate_gpa(new_gpa)

        records[idx] = student
        save_csv(records)

        # Modify supplementary fields
        details = load_json()
        old_details = details.get(reg_number, {})

        new_address = input(f"Residence [{old_details.get('address', '')}]: ").strip()
        new_contact = input(f"Phone [{old_details.get('contact', '')}]: ").strip()
        new_program = input(f"Major [{old_details.get('program', '')}]: ").strip()

        if new_address: old_details["address"] = new_address
        if new_contact: old_details["contact"] = new_contact
        if new_program: old_details["program"] = new_program

        details[reg_number] = old_details
        save_json(details)

        print(f"\n  Entry '{reg_number}' has been updated.")
        logger.info("Entry modified: %s", reg_number)

    except (RecordNotFoundError, DataValidationError) as e:
        print(f"\n  {e}")
        logger.warning("Update failed: %s", e)
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        logger.error("Unexpected error in update_student: %s", e)
    finally:
        logger.debug("update_student() completed.")


def delete_student() -> None:
    """
    Erase record from both storage systems after user confirms.
    Raises RecordNotFoundError if ID doesn't exist.
    """
    print("\n--- Remove Entry ---")
    logger.info("Operation: Delete Entry")

    try:
        reg_number = validate_reg_number(input("Enter ID to remove: "))

        records = load_csv()
        match   = next((r for r in records if r["reg_number"] == reg_number), None)

        if match is None:
            raise RecordNotFoundError(
                f"No entry with ID '{reg_number}' exists."
            )

        print(f"\nEntry to remove: {match['first_name']} {match['last_name']} "
              f"({reg_number})")
        confirm = input("Confirm deletion? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Operation cancelled.")
            logger.info("Deletion aborted for %s.", reg_number)
            return

        # Remove from CSV storage
        updated_records = [r for r in records if r["reg_number"] != reg_number]
        save_csv(updated_records)

        # Remove from JSON storage
        details = load_json()
        if reg_number in details:
            del details[reg_number]
            save_json(details)

        print(f"\n  Entry '{reg_number}' removed successfully.")
        logger.info("Entry deleted: %s", reg_number)

    except (RecordNotFoundError, DataValidationError) as e:
        print(f"\n  {e}")
        logger.warning("Delete failed: %s", e)
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        logger.error("Unexpected error in delete_student: %s", e)
    finally:
        logger.debug("delete_student() completed.")


# User Interface
def display_menu() -> None:
    """Display menu options to user."""
    print("\n" + "=" * 45)
    print("   ACADEMIC RECORD SYSTEM")
    print("=" * 45)
    print("  1. Add New Entry")
    print("  2. View All Entries")
    print("  3. Search by ID")
    print("  4. Modify Entry")
    print("  5. Remove Entry")
    print("  6. Quit")
    print("=" * 45)


def main() -> None:
    """
    Main program loop. Initialize storage and present menu until exit.
    """
    logger.info("=== System initialized ===")
    _init_csv()
    _init_json()

    menu_actions = {
        "1": add_student,
        "2": view_all_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
    }

    while True:
        display_menu()
        choice = input("Select option (1-6): ").strip()
        logger.debug("User selected: %s", choice)

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice == "6":
            print("\nExiting. Changes saved.")
            logger.info("=== System terminated by user ===")
            break
        else:
            print("\n  Invalid choice. Select 1-6.")
            logger.warning("Invalid selection: '%s'", choice)


if __name__ == "__main__":
    main()