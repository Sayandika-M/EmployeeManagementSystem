import json
import random
import string
from dataclasses import asdict, dataclass

# ---------------- Employee Model ---------------- #
@dataclass
class Employee:
    emp_id: str
    name: str
    email: str
    password: str
    attendance: int
    salary: int

    def view_profile(self):
        return {
            "Employee ID": self.emp_id,
            "Name": self.name,
            "Email": self.email,
            "Attendance %": self.attendance,
            "Salary": self.salary
        }

    def edit_profile(self, new_name: str, new_email: str):
        self.name = new_name
        self.email = new_email

    def change_password(self, new_password: str):
        self.password = new_password


# ---------------- Storage Helpers ---------------- #
FILE_NAME = "employees.json"

def load_data() -> dict:
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # If file is empty/corrupt, start fresh
        return {}

def save_data(data: dict) -> None:
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------- Business Logic ---------------- #
def generate_emp_id(data: dict) -> str:
    # Next ID like EMP001, EMP002, ...
    next_num = len(data) + 1
    return f"EMP{next_num:03d}"

def generate_password(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=length))

def generate_attendance() -> int:
    return random.randint(60, 100)

def generate_salary() -> int:
    return random.randint(30000, 70000)

def register():
    data = load_data()
    emp_id = generate_emp_id(data)

    print("\n--- Register ---")
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    password = generate_password()
    attendance = generate_attendance()
    salary = generate_salary()

    emp = Employee(emp_id, name, email, password, attendance, salary)
    data[emp_id] = asdict(emp)
    save_data(data)

    print(f"\n✅ Registration successful!")
    print(f"   Employee ID: {emp_id}")
    print(f"   Temporary Password: {password}\n")

def login():
    data = load_data()
    print("\n--- Login ---")
    emp_id = input("Enter Employee ID: ").strip()
    password = input("Enter Password: ").strip()

    if emp_id in data and data[emp_id]["password"] == password:
        print("\n✅ Login Successful!")
        emp = Employee(**data[emp_id])
        employee_menu(emp)
        # persist any changes (e.g., profile/password)
        data[emp_id] = asdict(emp)
        save_data(data)
    else:
        print("\n❌ Invalid ID or Password!\n")

def employee_menu(emp: Employee):
    while True:
        print("\n--- Employee Menu ---")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. View Attendance")
        print("4. View Salary")
        print("5. Change Password")
        print("6. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            for k, v in emp.view_profile().items():
                print(f"{k}: {v}")
        elif choice == "2":
            name = input("Enter new name: ").strip()
            email = input("Enter new email: ").strip()
            emp.edit_profile(name, email)
            print("✅ Profile updated!")
        elif choice == "3":
            print(f"Attendance: {emp.attendance}%")
        elif choice == "4":
            print(f"Salary: ₹{emp.salary}")
        elif choice == "5":
            new_password = input("Enter new password: ").strip()
            emp.change_password(new_password)
            print("✅ Password changed!")
        elif choice == "6":
            print("🔒 Logged out.")
            break
        else:
            print("❌ Invalid choice! Please select 1-6.")


# ---------------- App Loop ---------------- #
def main():
    while True:
        print("\n===== Employee Management System =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("👋 Exiting program...")
            break
        else:
            print("❌ Invalid choice! Please select 1-3.")

if __name__ == "__main__":
    main()

