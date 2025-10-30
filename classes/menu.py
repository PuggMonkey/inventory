from classes.account import Account
from classes.auth import Authenticator
from enums.accountPermission import AccountPermission
from enums.page import Page
from classes.item import Item
from enums.category import Category
from database.databaseService import db

class Menu:
    """Menu class handles the display and navigation of the menu system."""
    def __init__(self):
        self.account: Account | None = None
        self.current_page: Page = Page.LOGIN
        self.auth: Authenticator = Authenticator()
        self.all_items: list[Item] = []
        self.selected_item: Item | None = None
        
    def run(self) -> None:
        """Runs the menu system"""
        while True:
            self.display()
    
    def display(self) -> None:
        """Displays the menu"""
        print("\033[2J\033[1;1H") # clear console
        
        # Update current page
        if self.current_page == Page.LOGIN and self.account:
            self.current_page = Page.MAIN
        
        # Title
        print("\n\n=== Inventory Management System ===\n")
        
        # Print login page
        if not self.account and self.current_page == Page.LOGIN:
            print("1. Login")
            print("2. Exit")
            
        # Print main menu
        elif self.account and self.current_page == Page.MAIN:
            print(f"Welcome, {self.account.username}!\n")
            print("1. Inventory Management")
            print("2. Manage Account")
            print("3. Logout")
            
        # Print inventory menu
        elif self.account and self.current_page == Page.INVENTORY:
            print("Inventory Page\n")
            print("1. View Inventory")
            if self.account.permission in [AccountPermission.ADMIN, AccountPermission.WRITE]:
                 print("2. Edit Inventory")
            print("3. Back to Main Menu")
            
        # Print account management menu
        elif self.account and self.current_page == Page.ACCOUNT_MANAGEMENT:
            print("Account Management Page\n")
            if self.account.permission == AccountPermission.ADMIN:
                print ("1. Create Account")
            else:
                print("1. Delete Account")
            print("2. Back to Main Menu")
            
        # Print create user menu
        elif self.account and self.current_page == Page.CREATE_USER:
            print("Create User Account Page\n")
            print("1. Create New Account")
            print("2. Back to Account Management Menu")
            
        # Print view inventory menu
        elif self.account and self.current_page == Page.VIEW_INVENTORY:
            print("View Inventory Page\n")
            print("1. Back to Inventory Menu\n")
            self.print_items(2)
            
        # Print edit inventory menu
        elif self.account and self.current_page == Page.EDIT_INVENTORY:
            print("Edit Inventory Page\n")
            print("1. Back to Inventory Menu")
            print("2. Create Item")
            self.print_items(3)
            
        # Print create item menu
        elif self.account and self.current_page == Page.CREATE_ITEM:
            print("Create Item Page\n")
            print("1. Create New Item")
            print("2. Back to Edit Inventory Menu")
            
        # Print edit item menu
        elif self.account and self.current_page == Page.EDIT_ITEM:
            print(f"Edit Item Page - {self.selected_item.name if self.selected_item else 'No Item Selected'}\n")
            print("1. Increase Quantity")
            print("2. Decrease Quantity")
            print("3. Mark as Defective")
            print("4. Repair Defective Items")
            print("5. Delete Item")
            print("6. Back to Edit Inventory Menu")
            
        # Invalid action, sign user out
        else:
            print("Invalid state detected.")
            self.current_page = Page.LOGIN
            self.account = None
         
        # Get users option choice   
        choice = input("\nEnter your choice: ")
        if choice.isdigit():
            self.navigate(int(choice))
        else:
            input("Invalid input. Please enter a number.")
            
    def navigate(self, choice: int) -> None:
        # Login Page
        if not self.account and self.current_page == Page.LOGIN:
            self.login_page(choice)
        
        # Main Page
        elif self.account and self.current_page == Page.MAIN:
            self.main_page(choice)
            
        # Inventory Page
        elif self.account and self.current_page == Page.INVENTORY:
            self.inventory_page(choice)
            
        # Account Management Page
        elif self.account and self.current_page == Page.ACCOUNT_MANAGEMENT:
            self.manage_account_page(choice)
            
        # Create Account Page
        elif self.account and self.current_page == Page.CREATE_USER:
            self.create_account_page(choice)
                        
        # View Inventory Page
        elif self.account and self.current_page == Page.VIEW_INVENTORY:
            self.view_inventory_page(choice)
        
        # Edit Inventory Page
        elif self.account and self.current_page == Page.EDIT_INVENTORY:
            self.edit_inventory_page(choice)
            
        # Create Item Page
        elif self.account and self.current_page == Page.CREATE_ITEM:
            self.create_item(choice)
        
        # Edit Item Page
        elif self.account and self.current_page == Page.EDIT_ITEM:
            self.edit_item_page(choice)
            
    
    def login_page(self, choice: int) -> None:
        # Handle login
        if choice == 1:
            again = True
            while again:
                again = False
                # Get username and password
                username = input("\nUsername: ")
                password = input("Password: ")
                account = self.auth.find_account(username, password)
                
                # Check if account exists
                if account:
                    self.account = account
                    self.current_page = Page.MAIN
                else:
                    retry = input("Invalid credentials. Would you like to try again? (y/n) ").lower()
                    if retry != 'y':
                        again = False
            # Exit
        elif choice == 2:
            print("Exiting the system. Goodbye!")
            exit()
            
    def main_page(self, choice: int) -> None:
        # Navigate to Inventory
        if choice == 1:
            self.current_page = Page.INVENTORY
            
        # Navigate to Account Management
        elif choice == 2:
            self.current_page = Page.ACCOUNT_MANAGEMENT
            
        # Sign out
        elif choice == 3:
            self.account = None 
            self.current_page = Page.LOGIN
            
    def inventory_page(self, choice: int) -> None:
        # If no account, sign out
        if not self.account:
            self.current_page = Page.LOGIN
            return
        
        # View Inventory
        if choice == 1:
            self.current_page = Page.VIEW_INVENTORY
        
        # Edit Inventory
        elif choice == 2 and self.account.permission in [AccountPermission.ADMIN, AccountPermission.WRITE]:
            self.current_page = Page.EDIT_INVENTORY
            
        # Back to main menu
        elif choice == 3:
            self.current_page = Page.MAIN
            
    def view_inventory_page(self, choice: int) -> None:
        # View Inventory
        if choice == 1:
            self.current_page = Page.INVENTORY
        else:
            input("Invalid choice. Please try again.")
    
    def edit_inventory_page(self, choice: int) -> None:
        # Back to main Inventory page
        if choice == 1:
            self.current_page = Page.INVENTORY
            
        # Create new item
        elif choice == 2:
            self.current_page = Page.CREATE_ITEM
            
        # Edit existing item
        elif choice > 2 and choice - 3 < len(self.all_items):
            self.selected_item = self.all_items[choice - 3]
            self.current_page = Page.EDIT_ITEM
        else:
            input("Invalid choice. Please try again.")
            return
            
    def create_item(self, choice: int) -> None:
        # Create new item
        if choice == 1:
            self.fetch_items(False)
            # Get item name, check if it already exists
            name = input("Enter item name: ")
            for i in range(len(self.all_items)):
                if self.all_items[i].name.lower() == name.lower():
                    input("Item with this name already exists.")
                    return
                
            # Get categories and display options
            categories = [name for name in dir(Category) if not name.startswith('__') and name in Category.__dict__]
            categories.reverse()
            for i in range(len(categories)):
                print(f"{i + 1}. {categories[i]}")
            
            # Get category and quantity
            cat_choice = input("Select category: ")
            if cat_choice.isdigit() and int(cat_choice) >= 1 and int(cat_choice) <= len(categories):
                category = categories[int(cat_choice) - 1]
                quantity = input("Enter quantity: ")
                # If all is good, create item
                if quantity.isdigit() and int(quantity) >= 0:
                    db.items.add_item(name, getattr(Category, category), int(quantity))
                    input("\nItem created successfully.")
                    self.current_page = Page.EDIT_INVENTORY
                else:
                    input("Invalid quantity.")
                    return
            else:
                input("Invalid category choice.")
                return
        elif choice == 2:
            self.current_page = Page.EDIT_INVENTORY
        else:
            input("Invalid choice. Please try again.")
            
            
    def edit_item_page(self, choice: int) -> None:
        # If no item selected, return
        if not self.selected_item:
            input("\nNo item selected.")
            self.current_page = Page.EDIT_INVENTORY
            return
        
        # Increase quantity
        if choice == 1:
            increase = input("Enter quantity to increase: ")
            if increase.isdigit() and int(increase) >= 0:
                self.selected_item.increase_quantity(int(increase))
                input("\nQuantity increased successfully.")
                self.current_page = Page.EDIT_INVENTORY
                self.selected_item = None
            else:
                input("\nInvalid quantity.")
                
        # Decrease quantity
        elif choice == 2:
            decrease = input("Enter quantity to decrease: ")
            if decrease.isdigit() and int(decrease) >= 0:
                self.selected_item.decrease_quantity(int(decrease))
                input("\nQuantity decreased successfully.")
                self.current_page = Page.EDIT_INVENTORY
                self.selected_item = None
            else:
                input("\nInvalid quantity.")
                
        # Mark as defective
        elif choice == 3:
            defective = input("Enter defective quantity to mark: ")
            if defective.isdigit() and int(defective) >= 0 and int(defective) <= self.selected_item.quantity:
                self.selected_item.mark_defective(int(defective))
                input("\nItems marked as defective successfully.")
                self.current_page = Page.EDIT_INVENTORY
                self.selected_item = None
            else:
                input("\nInvalid quantity.")
                
        # Repair defective
        elif choice == 4:
            repair = input("Enter defective quantity to repair: ")
            if repair.isdigit() and int(repair) >= 0 and int(repair) <= self.selected_item.defective_quantity:
                self.selected_item.repair_defective(int(repair))
                input("\nDefective items repaired successfully.")
                self.current_page = Page.EDIT_INVENTORY
                self.selected_item = None
            else:
                input("\nInvalid quantity.")
                
        # Delete item
        elif choice == 5:
            confirmation = input("Are you sure you want to delete this item? (y/n): ").lower()
            if confirmation == 'y':
                db.items.delete_item(self.selected_item.id)
                input("\nItem deleted successfully.")
                self.current_page = Page.EDIT_INVENTORY
                self.selected_item = None
            else:
                input("\nItem deletion cancelled.")
        elif choice == 6:
            self.current_page = Page.EDIT_INVENTORY
            self.selected_item = None
            
    def manage_account_page(self, choice: int) -> None:
        # If no account, return
        if not self.account:
            input("No account found...")
            self.current_page = Page.LOGIN
            return
        
        # If admin, display account creation
        if self.account.permission == AccountPermission.ADMIN:
            if choice == 1:
                self.current_page = Page.CREATE_USER
            elif choice == 2:
                self.current_page = Page.MAIN
        
        # Else, display account deletion
        else:
            if choice == 1:
                db.accounts.delete_account(self.account.id)
                self.account = None
                self.current_page = Page.LOGIN
            elif choice == 2:
                self.current_page = Page.MAIN
    
    def create_account_page(self, choice: int) -> None:
        if choice == 1:
            # Get username, password, and permission
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            perm_input = input("Enter permission (1 for ADMIN, 2 for WRITE, 3 for READ): ")
            if perm_input.isdigit() and int(perm_input) in [1, 2, 3]:
                # Create account
                permission = AccountPermission(int(perm_input))
                db.accounts.create_account(username, self.auth.hash_password(password), permission)
                input("\nAccount created successfully.")
                self.current_page = Page.ACCOUNT_MANAGEMENT
            else:
                input("\nInvalid permission choice.")
        # Return to account management menu
        elif choice == 2:
            self.current_page = Page.ACCOUNT_MANAGEMENT
        else:
            input("\nInvalid choice. Please try again.")
        
    def print_items(self, offset: int) -> None:
        # Fetch items   
        self.fetch_items()
        categories = [name for name in dir(Category) if not name.startswith('__') and name in Category.__dict__]
        categories.reverse()
        # Print items
        for i in range(len(self.all_items)):
            item = self.all_items[i]
            print(f"{i + offset}. {item.name}\n      Category: {categories[item.category-1]}\n      Total: {item.quantity + item.defective_quantity}\n      Working Quantity: {item.quantity}\n      Defective Quantity: {item.defective_quantity}\n")
    
    def fetch_items(self, log: bool = True) -> None:
        # Fetch items
        items = db.items.get_all_items()
        if not items:
            if log:
                print("No items found in inventory.\n")
            return
        # Store items
        self.all_items = items