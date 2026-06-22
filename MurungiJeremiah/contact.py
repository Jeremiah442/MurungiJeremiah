"""
Contact Management System
==========================
A simple, function/class-based contact manager.

Contacts are stored in memory as a list of tuples:
    (name, phone, email)

Phone number acts as the unique identifier for a contact (no two
contacts can share the same phone number).

Features:
    - Add / View / Update / Delete contacts (CRUD)
    - Data validation for phone numbers and emails
    - Search contacts by name, phone, OR email
    - Interactive CLI menu (see main())
"""


class ContactManager:
    def __init__(self):
        # Each contact is stored as a tuple: (name, phone, email)
        self.contacts = []

    # ------------------------------------------------------------------
    # Validation helpers (Task 1)
    # ------------------------------------------------------------------
    @staticmethod
    def is_valid_phone(phone):
        """
        A phone number is valid if it contains ONLY digits and hyphens.
        Examples of valid phone numbers: "0701234567", "+256-701" is NOT
        valid because '+' is not a digit or hyphen -- per the assignment
        spec, only digits and hyphens are allowed.
        """
        if not phone:
            return False
        return all(ch.isdigit() or ch == "-" for ch in phone)

    @staticmethod
    def is_valid_email(email):
        """
        An email (if provided) is valid if it contains both '@' and '.'.
        Empty email is considered valid since email is optional.
        """
        if email == "":
            return True
        return "@" in email and "." in email

    # ------------------------------------------------------------------
    # Internal lookup helper
    # ------------------------------------------------------------------
    def _find_index_by_phone(self, phone):
        for index, contact in enumerate(self.contacts):
            if contact[1] == phone:
                return index
        return -1

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def add_contact(self, name, phone, email=""):
        """Add a new contact after validating phone and email."""
        name = name.strip()
        phone = phone.strip()
        email = email.strip()

        if not name:
            print("Error: Name cannot be empty.")
            return False

        if not self.is_valid_phone(phone):
            print(
                "Error: Invalid phone number. "
                "Phone numbers may only contain digits and hyphens (e.g. 256-701-234567)."
            )
            return False

        if not self.is_valid_email(email):
            print("Error: Invalid email. Email must contain an '@' and a '.'.")
            return False

        if self._find_index_by_phone(phone) != -1:
            print(f"Error: A contact with phone number '{phone}' already exists.")
            return False

        self.contacts.append((name, phone, email))
        print(f"Contact '{name}' added successfully.")
        return True

    def view_contact(self, phone):
        """View a single contact by phone number."""
        index = self._find_index_by_phone(phone.strip())
        if index == -1:
            print(f"No contact found with phone number '{phone}'.")
            return None

        contact = self.contacts[index]
        self._print_contact(contact)
        return contact

    def update_contact(self, phone, new_name=None, new_phone=None, new_email=None):
        """
        Update an existing contact found by its current phone number.
        Any field left as None (or an empty string, for name/phone) is left unchanged.
        """
        index = self._find_index_by_phone(phone.strip())
        if index == -1:
            print(f"Error: No contact found with phone number '{phone}'.")
            return False

        name, current_phone, email = self.contacts[index]

        # Resolve new values, defaulting to existing ones if not provided
        updated_name = new_name.strip() if new_name else name
        updated_phone = new_phone.strip() if new_phone else current_phone
        updated_email = new_email.strip() if new_email is not None and new_email != "" else email

        # Validate phone if it's changing
        if not self.is_valid_phone(updated_phone):
            print(
                "Error: Invalid phone number. "
                "Phone numbers may only contain digits and hyphens. Update cancelled."
            )
            return False

        # If phone is changing, make sure the new one isn't already taken
        if updated_phone != current_phone and self._find_index_by_phone(updated_phone) != -1:
            print(f"Error: A contact with phone number '{updated_phone}' already exists. Update cancelled.")
            return False

        # Validate email
        if not self.is_valid_email(updated_email):
            print("Error: Invalid email. Email must contain an '@' and a '.'. Update cancelled.")
            return False

        self.contacts[index] = (updated_name, updated_phone, updated_email)
        print(f"Contact '{current_phone}' updated successfully.")
        return True

    def delete_contact(self, phone):
        """Delete a contact by phone number."""
        index = self._find_index_by_phone(phone.strip())
        if index == -1:
            print(f"Error: No contact found with phone number '{phone}'.")
            return False

        name = self.contacts[index][0]
        del self.contacts[index]
        print(f"Contact '{name}' deleted successfully.")
        return True

    def list_all_contacts(self):
        """Print every contact in a clean, readable format."""
        if not self.contacts:
            print("No contacts saved yet.")
            return
        print(f"\n--- All Contacts ({len(self.contacts)}) ---")
        for contact in self.contacts:
            self._print_contact(contact)
        print("-" * 30)

    # ------------------------------------------------------------------
    # Advanced Search (Task 2)
    # ------------------------------------------------------------------
    def search_contacts(self, query):
        """
        Search contacts by name, phone number, OR email.
        Matching is case-insensitive and based on partial (substring) matches.
        Returns the list of matching contact tuples.
        """
        query = query.strip().lower()
        if not query:
            print("Error: Search query cannot be empty.")
            return []

        results = [
            contact
            for contact in self.contacts
            if query in contact[0].lower()        # name
            or query in contact[1].lower()         # phone
            or query in contact[2].lower()         # email
        ]

        self._print_search_results(results, query)
        return results

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _print_contact(contact):
        name, phone, email = contact
        email_display = email if email else "(no email)"
        print(f"  Name: {name:<20} Phone: {phone:<15} Email: {email_display}")

    def _print_search_results(self, results, query):
        if not results:
            print(f"No contacts found matching '{query}'.")
            return

        print(f"\n--- Search Results for '{query}' ({len(results)} found) ---")
        for contact in results:
            self._print_contact(contact)
        print("-" * 30)


# ----------------------------------------------------------------------
# Interactive CLI (Task 3)
# ----------------------------------------------------------------------
def print_menu():
    print("\n=== Contact Manager Menu ===")
    print("1. Add Contact")
    print("2. View Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Search Contacts")
    print("6. List All Contacts")
    print("7. Exit")


def main():
    manager = ContactManager()

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            print("\n-- Add Contact --")
            name = input("Enter name: ")
            phone = input("Enter phone (digits and hyphens only): ")
            email = input("Enter email (optional, press Enter to skip): ")
            manager.add_contact(name, phone, email)

        elif choice == "2":
            print("\n-- View Contact --")
            phone = input("Enter phone number of contact to view: ")
            manager.view_contact(phone)

        elif choice == "3":
            print("\n-- Update Contact --")
            phone = input("Enter phone number of contact to update: ")
            if manager._find_index_by_phone(phone.strip()) == -1:
                print(f"No contact found with phone number '{phone}'.")
                continue
            print("Leave a field blank to keep its current value.")
            new_name = input("New name: ")
            new_phone = input("New phone: ")
            new_email = input("New email: ")
            manager.update_contact(phone, new_name, new_phone, new_email)

        elif choice == "4":
            print("\n-- Delete Contact --")
            phone = input("Enter phone number of contact to delete: ")
            confirm = input(f"Are you sure you want to delete '{phone}'? (y/n): ").strip().lower()
            if confirm == "y":
                manager.delete_contact(phone)
            else:
                print("Delete cancelled.")

        elif choice == "5":
            print("\n-- Search Contacts --")
            query = input("Enter a name, phone number, or email to search for: ")
            manager.search_contacts(query)

        elif choice == "6":
            manager.list_all_contacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 7.")


if __name__ == "__main__":
    main()