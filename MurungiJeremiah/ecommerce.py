SYSTEM_NAME = "TechHub Sales Management System"
ROLES = ("customer", "cashier", "admin")
SESSION_FILE = "session.bin"
ENCODING = "utf-32"

USERS = [
    {
        "fullname": "Admin User",
        "username": "admin",
        "password": "admin123",
        "role": "admin",
        "location": "kampala",
    },
    {
        "fullname": "Cashier User",
        "username": "cashier",
        "password": "cashier123",
        "role": "cashier",
        "location": "wakiso",
    },
    {
        "fullname": "Customer User",
        "username": "customer",
        "password": "customer123",
        "role": "customer",
        "location": "mbarara",
    },
]

PRODUCTS = [
    {"id": "P001", "name": "iPad", "price": 1800000},
    {"id": "P002", "name": "Samsung Galaxy S24", "price": 1200000},
    {"id": "P003", "name": "AirPods Pro", "price": 350000},
]

COUPONS = {
    "VIP20": 20,
    "SAVE10": 10,
    "TECH15": 15,
    "EARLY5": 5,
}

TAX_RATES = {
    "kampala": 20,
    "wakiso": 16,
    "mbarara": 12,
    "gulu": 8,
}

ACCESS_LEVELS = {
    "create_product": ("admin", "cashier"),
    "remove_product": ("admin",),
    "view_product": ("admin", "cashier", "customer"),
    "buy_product": ("admin", "cashier", "customer"),
    "calculate_price": ("admin", "cashier", "customer"),
    "create_user": ("admin",),
    "view_users": ("admin",),
}


def print_line():
    print("-" * 60)


def print_title(title):
    print_line()
    print(title.upper().center(60))
    print_line()


def format_money(amount):
    return f"UGX {amount:,.2f}"


def find_user(username):
    username = username.strip().lower()
    for user in USERS:
        if user["username"].lower() == username:
            return user
    return None


def set_session(user):
    with open(SESSION_FILE, "wb") as file:
        session_text = ",".join(
            [user["username"], user["role"], user["location"]]
        )
        file.write(session_text.encode(ENCODING))


def read_session():
    try:
        with open(SESSION_FILE, "rb") as file:
            session_text = file.read().decode(ENCODING).strip()
    except FileNotFoundError:
        return None

    if session_text == "":
        return None

    session_parts = session_text.split(",")
    if len(session_parts) != 3:
        unset_session()
        return None

    username = session_parts[0]
    role = session_parts[1]
    location = session_parts[2]
    return {"username": username, "role": role, "location": location}


def unset_session():
    with open(SESSION_FILE, "wb") as file:
        file.write(b"")


def get_current_user():
    session = read_session()
    if session is None:
        return None

    user = find_user(session["username"])
    if user is None:
        unset_session()
        return None

    if user["role"] != session["role"]:
        unset_session()
        return None

    return user


def has_access(user, action):
    if user is None:
        return False
    return user["role"] in ACCESS_LEVELS[action]


def check_access(user, action):
    if has_access(user, action):
        return True

    print("Access denied. Your role cannot perform this action.")
    return False


def register_user(fullname, username, password, location, role):
    fullname = fullname.strip()
    username = username.strip()
    password = password.strip()
    location = location.strip().lower()
    role = role.strip().lower()

    if fullname == "" or username == "" or password == "" or location == "":
        return False, "All fields are required."

    if role not in ROLES:
        return False, "Invalid role."

    if find_user(username) is not None:
        return False, "Username already exists."

    user = {
        "fullname": fullname,
        "username": username,
        "password": password,
        "role": role,
        "location": location,
    }
    USERS.append(user)
    return True, "User registered successfully."


def get_confirmed_password():
    password = ""
    confirm_password = "_"

    while password != confirm_password:
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            print("Passwords do not match. Try again.")

    return password


def register_customer_flow():
    print_title("Customer Registration")
    fullname = input("Enter full name: ")
    username = input("Enter username: ")
    password = get_confirmed_password()
    location = input("Enter location: ")

    success, message = register_user(
        fullname, username, password, location, "customer"
    )
    print(message)

    if success:
        user = find_user(username)
        set_session(user)
        print(f"Logged in as {user['fullname']} ({user['role']}).")


def choose_role_for_new_user():
    while True:
        print("1. Customer")
        print("2. Cashier")
        print("3. Admin")
        choice = input("Choose role: ")

        if choice == "1":
            return "customer"
        elif choice == "2":
            return "cashier"
        elif choice == "3":
            return "admin"
        else:
            print("Invalid role choice.")


def admin_create_user_flow(current_user):
    if not check_access(current_user, "create_user"):
        return

    print_title("Admin Create User")
    fullname = input("Enter full name: ")
    username = input("Enter username: ")
    password = get_confirmed_password()
    location = input("Enter location: ")
    role = choose_role_for_new_user()

    success, message = register_user(fullname, username, password, location, role)
    print(message)


def login(username, password):
    user = find_user(username)

    if user is None:
        return False, "Invalid username or password."

    if user["password"] != password:
        return False, "Invalid username or password."

    set_session(user)
    return True, f"Logged in as {user['fullname']} ({user['role']})."


def login_flow():
    print_title("Login")
    username = input("Enter username: ")
    password = input("Enter password: ")

    success, message = login(username, password)
    print(message)


def logout():
    unset_session()
    print("Logged out successfully.")


def view_users(current_user):
    if not check_access(current_user, "view_users"):
        return

    print_title("Users")
    print(f"{'Username':<15}{'Full name':<22}{'Role':<12}{'Location':<12}")
    print_line()

    for user in USERS:
        print(
            f"{user['username']:<15}"
            f"{user['fullname']:<22}"
            f"{user['role']:<12}"
            f"{user['location']:<12}"
        )


def next_product_id():
    number = len(PRODUCTS) + 1
    return f"P{number:03d}"


def find_product(product_id):
    product_id = product_id.strip().upper()
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def view_products(current_user):
    if not check_access(current_user, "view_product"):
        return

    print_title("Products")
    print(f"{'ID':<8}{'Name':<25}{'Price':>20}")
    print_line()

    for product in PRODUCTS:
        print(
            f"{product['id']:<8}"
            f"{product['name']:<25}"
            f"{format_money(product['price']):>20}"
        )


def add_product(current_user):
    if not check_access(current_user, "create_product"):
        return

    print_title("Add Product")
    name = input("Enter product name: ").strip()
    price = get_positive_number("Enter product price: ")

    product = {"id": next_product_id(), "name": name, "price": price}
    PRODUCTS.append(product)
    print("Product added successfully.")


def remove_product(current_user):
    if not check_access(current_user, "remove_product"):
        return

    view_products(current_user)
    product_id = input("Enter product ID to remove: ")
    product = find_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        PRODUCTS.remove(product)
        print("Product removed successfully.")


def get_positive_number(prompt):
    while True:
        value = input(prompt)

        try:
            number = float(value)
        except ValueError:
            print("Enter a valid number.")
            continue

        if number > 0:
            return number
        else:
            print("Enter a number greater than zero.")


def get_tax_rate(location):
    location = location.strip().lower()

    if location in TAX_RATES:
        return TAX_RATES[location], f"{location.capitalize()} tax rate"
    else:
        default_rate = TAX_RATES.get("kampala", 20)
        return default_rate, "Unknown location, default tax rate used"


def get_subtotal_discount(subtotal):
    if subtotal >= 2000000:
        return 12, "Premium subtotal discount"
    else:
        if subtotal >= 1000000:
            return 8, "High subtotal discount"
        else:
            if subtotal >= 500000:
                return 5, "Medium subtotal discount"
            else:
                return 0, "No subtotal discount"


def get_coupon_discount(coupon_code):
    coupon_code = coupon_code.strip().upper()

    if coupon_code != "":
        if coupon_code in COUPONS:
            return COUPONS[coupon_code], f"Valid coupon: {coupon_code}"
        else:
            return 0, f"Invalid coupon ignored: {coupon_code}"
    else:
        return 0, "No coupon entered"


def calculate_final_price(subtotal, coupon_code, location):
    if subtotal <= 0:
        return None

    coupon_discount, coupon_message = get_coupon_discount(coupon_code)
    subtotal_discount, subtotal_message = get_subtotal_discount(subtotal)
    tax_rate, tax_message = get_tax_rate(location)

    total_discount_rate = coupon_discount + subtotal_discount

    if total_discount_rate > 25:
        total_discount_rate = 25

    discount_amount = subtotal * total_discount_rate / 100
    amount_after_discount = subtotal - discount_amount
    tax_amount = amount_after_discount * tax_rate / 100
    final_price = amount_after_discount + tax_amount

    return {
        "subtotal": subtotal,
        "coupon_message": coupon_message,
        "subtotal_message": subtotal_message,
        "coupon_discount": coupon_discount,
        "subtotal_discount": subtotal_discount,
        "total_discount_rate": total_discount_rate,
        "discount_amount": discount_amount,
        "tax_message": tax_message,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "final_price": final_price,
    }


def show_price_breakdown(subtotal, coupon_code, location):
    result = calculate_final_price(subtotal, coupon_code, location)

    if result is None:
        print("Subtotal must be greater than zero.")
        return

    print_title("Receipt Summary")
    print(f"Subtotal:             {format_money(result['subtotal'])}")
    print(f"Coupon:               {result['coupon_message']}")
    print(f"Subtotal discount:    {result['subtotal_message']}")
    print(f"Coupon discount:      {result['coupon_discount']}%")
    print(f"Subtotal discount:    {result['subtotal_discount']}%")
    print(f"Total discount:       {result['total_discount_rate']}%")
    print(f"Discount amount:      {format_money(result['discount_amount'])}")
    print(f"Tax:                  {result['tax_message']} ({result['tax_rate']}%)")
    print(f"Tax amount:           {format_money(result['tax_amount'])}")
    print_line()
    print(f"Final price:          {format_money(result['final_price'])}")


def buy_product(current_user):
    if not check_access(current_user, "buy_product"):
        return

    view_products(current_user)
    product_id = input("Enter product ID: ")
    product = find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    quantity = get_positive_number("Enter quantity: ")
    subtotal = product["price"] * quantity
    coupon_code = input("Enter coupon code or press Enter to skip: ")
    location = input(f"Enter location [{current_user['location']}]: ").strip()

    if location == "":
        location = current_user["location"]

    show_price_breakdown(subtotal, coupon_code, location)


def manual_calculation(current_user):
    if not check_access(current_user, "calculate_price"):
        return

    print_title("Manual Final Price Calculator")
    subtotal = get_positive_number("Enter subtotal: ")
    coupon_code = input("Enter coupon code or press Enter to skip: ")
    location = input(f"Enter location [{current_user['location']}]: ").strip()

    if location == "":
        location = current_user["location"]

    show_price_breakdown(subtotal, coupon_code, location)


def guest_menu():
    print_title(SYSTEM_NAME)
    print("1. Register as customer")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        register_customer_flow()
    elif choice == "2":
        login_flow()
    elif choice == "3":
        print("Thank you for shopping with us.")
        return False
    else:
        print("Invalid choice.")

    return True


def user_menu(current_user):
    print_title(f"{current_user['role']} dashboard")
    print(f"Logged in as: {current_user['fullname']}")
    print(f"Location: {current_user['location']}")
    print_line()

    print("1. View products")
    print("2. Buy product")
    print("3. Calculate final price manually")

    if current_user["role"] == "customer":
        print("4. Logout")
        print("5. Exit")
    elif current_user["role"] == "cashier":
        print("4. Add product")
        print("5. Logout")
        print("6. Exit")
    elif current_user["role"] == "admin":
        print("4. Add product")
        print("5. Remove product")
        print("6. Add user")
        print("7. View users")
        print("8. Logout")
        print("9. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        view_products(current_user)
    elif choice == "2":
        buy_product(current_user)
    elif choice == "3":
        manual_calculation(current_user)
    elif choice == "4":
        if current_user["role"] == "customer":
            logout()
        else:
            add_product(current_user)
    elif choice == "5":
        if current_user["role"] == "customer":
            print("Thank you for shopping with us.")
            return False
        elif current_user["role"] == "cashier":
            logout()
        else:
            remove_product(current_user)
    elif choice == "6":
        if current_user["role"] == "cashier":
            print("Thank you for shopping with us.")
            return False
        elif current_user["role"] == "admin":
            admin_create_user_flow(current_user)
    elif choice == "7" and current_user["role"] == "admin":
        view_users(current_user)
    elif choice == "8" and current_user["role"] == "admin":
        logout()
    elif choice == "9" and current_user["role"] == "admin":
        print("Thank you for shopping with us.")
        return False
    else:
        print("Invalid choice.")

    return True


def main():
    keep_running = True

    while keep_running:
        current_user = get_current_user()

        if current_user is None:
            keep_running = guest_menu()
        else:
            keep_running = user_menu(current_user)


main()