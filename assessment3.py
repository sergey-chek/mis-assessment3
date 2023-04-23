import re
import datetime


class User:
    def __init__(self, name, address, mobile_number, password, date_of_birth):
        self.name = name
        self.address = address
        self.mobile_number = mobile_number
        self.password = password
        self.date_of_birth = date_of_birth
        self.previous_passwords = []
        self.orders = []

class MenuItem:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def item_text(self):
        return f'Enter {self.id} for {self.name}\t\t\tPrice AUD {self.price}'

class Order:
    def __init__(self):
        self.id = None
        self.date = None
        self.ordering_mode = None
        self.items = []

    def set_ordering_mode(self, ordering_mode):
        self.ordering_mode = ordering_mode

    def reset(self):
        self.ordering_mode = None
        self.items = []
        self.total_price = 0

    def add_item(self, item):
        self.items.append(item)

    def get_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item.price
        return total_price


class Account:
    def __init__(self):
        self.signed_in_user = None

    def sign_in(self):
        mobile_number = input('\nPlease enter your Username (Mobile Number): ')
        password = input('Please enter your password: ')
        current_user = None
        for user in users:
            if user.mobile_number == mobile_number:
                current_user = user
                break
        if not current_user:
            print('You have not Signed up with this contact number, please Sign up first.')
        else:
            if current_user.password == password:
                self.signed_in_user = current_user   # Set info that current user Signed in
                print('\nYou have successfully Signed in')
                print(f'Welcome {current_user.name}!')
                return True
            else:
                print('\nYou have entered the wrong Password. You will be directed to the main menu.')
                return False

    def sign_up(self):
        while True:
            name = input('\tPlease enter your name: ')
            address = input('\tPlease enter your address or press enter to Skip: ')
            mobile_number = input('\tPlease enter your mobile number: ')
            password = input('\tPlease enter your password: ')
            password_confirmation = input('\tPlease re-enter your password for confirmation: ')
            date_of_birth = input('\tPlease enter your Date of Birth # DD/MM/YYYY (No Space): ')
            print('')

            # Input data checks
            error_flag = False
            if not re.match(r'^0\d{9}$', mobile_number):
                print("Invalid mobile number. Please enter a 10 digit mobile number starting with 0.")
                error_flag = True
            for user in users:
                if user.mobile_number == mobile_number:
                    print('Mobile Number exist')
                    error_flag = True
            if not re.match(r'^[a-zA-Z]+[@&]\d+$', password):
                print(
                    'Invalid password. Password must initiate with alphabets followed by either one of @, & and ending with numeric.')
                error_flag = True
            if password != password_confirmation:
                print("Password confirmation does not match. Please enter same password for confirmation.")
                error_flag = True

            try:
                dob_date = datetime.datetime.strptime(date_of_birth, '%d/%m/%Y').date()
                today = datetime.date.today()
                age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                if age < 21:
                    print("You must be at least 21 years old.")
                    error_flag = True
            except ValueError:
                print("Invalid date format. Please enter date in DD/MM/YYYY format.")
                error_flag = True

            if error_flag:
                print('\nPlease start again: ')
                continue
            else:
                print('\nYou have successfully signed up.')
                user = User(name, address, mobile_number, password, date_of_birth)
                users.append(user)
                break

    def is_signed_in(self):
        if self.signed_in_user:
            return True
        else:
            return False

    def get_signed_in_user(self):
        return self.signed_in_user

    def log_out(self):
        self.signed_in_user = None


class Menu:
    def __init__(self):
        self.menu_text = ''
        self.allowed_input = []
        self.action = ''

    def execute(self):
        self._show_menu()
        user_choice = self._get_user_choice()
        self._user_choice_processing(user_choice)

    def _show_menu(self):
        """The method prints menu"""
        print(self.menu_text)

    def _get_user_choice(self):
        """
        The method gets the user's choice for the menu.
        If the user enters an incorrect value, then a re-entry of the value is requested.
        """
        while True:
            try:
                user_choice = input('>>> ').strip()
                if user_choice in self.allowed_input:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Invalid value, please try again.')
        return user_choice

    def _user_choice_processing(self, user_choice):
        """The method must contain the business logic of menu in the inherited classes"""
        raise NotImplementedError


class StartMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\nMAIN MENU:\n' \
                         'Please Enter 1 for Sign up.\n' \
                         'Please Enter 2 for Sign in.\n' \
                         'Please Enter 3 for Quit.\n'
        self.allowed_input = ['1', '2', '3']

    def _user_choice_processing(self, user_choice):
        current_order.reset()
        account.log_out()
        if user_choice == self.allowed_input[0]:     # 1 Sign Up
            account.sign_up()
        elif user_choice == self.allowed_input[1]:   # 2 Sign In
            if account.sign_in():
                SignInMenu().execute()
        elif user_choice == self.allowed_input[2]:   # 3 Quit
            print('\nThank you for using the Application!')
            self.action = 'QUIT'


class SignInMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\n\tMAIN MENU --> SIGNED IN MENU:\n\t' \
                         'Please Enter 2.1 to Start Ordering.\n\t' \
                         'Please Enter 2.2 to Print Statistics.\n\t' \
                         'Please Enter 2.3 for Logout.\n'
        self.allowed_input = ['2.1', '2.2', '2.3']

    def _user_choice_processing(self, user_choice):
        if user_choice == self.allowed_input[0]:    # 2.1 Start Ordering
            self._start_ordering()
        elif user_choice == self.allowed_input[1]:  # 2.2 Print Statistics
            self._print_statistics()
        elif user_choice == self.allowed_input[2]:  # 2.3 Logout
            account.log_out()
            current_order.reset()
            print('You have successfully Logged out!')

    def _start_ordering(self):
        ordering_menu = OrderingMenu()
        ordering_menu.execute()
        if ordering_menu.action == 'TO_ORDERING_MENU':
            self._start_ordering()

    def _print_statistics(self):
        pass  # TODO


class OrderingMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\n\t\tMAIN MENU -> SIGNED IN MENU -> ORDERING MENU:\n\t\t' \
                         'Please Enter 1 for Dine in.\n\t\t' \
                         'Please Enter 2 for Order Online.\n\t\t' \
                         'Please Enter 3 to go to Login Page.\n'
        self.allowed_input = ['1', '2', '3']

    def _user_choice_processing(self, user_choice):
        if user_choice == self.allowed_input[0]:    # 1 Dine In
            FoodMenu(show_drinks=True).execute()
        elif user_choice == self.allowed_input[1]:  # 2 Order Online
            self._order_online()
            FoodMenu(show_drinks=False).execute()
        elif user_choice == self.allowed_input[2]:  # 3 Login Page
            account.log_out()
            current_order.reset()

    def _order_online(self):
        ordering_online_menu = OrderingOnlineMenu()
        ordering_online_menu.execute()
        if ordering_online_menu.action == 'TO_ORDERING_MENU':
            self.action = ordering_online_menu.action


class OrderingOnlineMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\n\t\t\tMAIN MENU -> SIGN IN MENU -> ORDERING MENU -> ORDER ONLINE:\n\t\t\t' \
                         'Enter 1 for Self Pickup.\n\t\t\t' \
                         'Enter 2 for Home Delivery.\n\t\t\t' \
                         'Enter 3 to go to Previous Menu.\n'
        self.allowed_input = ['1', '2', '3']

    def _user_choice_processing(self, user_choice):
        if user_choice == self.allowed_input[0]:  # 1 Self Pickup
            current_order.set_ordering_mode('SELF_PICKUP')
        elif user_choice == self.allowed_input[1]:  # 2 Home Delivery
            current_order.set_ordering_mode('HOME_DELIVERY')
        elif user_choice == self.allowed_input[2]:  # 3 Previous Menu
            self.action = 'TO_ORDERING_MENU'


class FoodMenu(Menu):
    def __init__(self, show_drinks):
        super().__init__()
        self.show_drinks = show_drinks
        self.items = [
            MenuItem(1, 'Noodles', 2),
            MenuItem(2, 'Sandwich', 4),
            MenuItem(3, 'Dumpling', 6),
            MenuItem(4, 'Muffins', 8),
            MenuItem(5, 'Pasta', 10),
            MenuItem(6, 'Pizza', 20)
        ]
        if show_drinks:
            self.menu_text = 'Enter 1 for Noodles   Price AUD 2\n' \
                             'Enter 2 for Sandwich  Price AUD 4\n' \
                             'Enter 3 for Dumpling  Price AUD 6\n' \
                             'Enter 4 for Muffins   Price AUD 8\n' \
                             'Enter 5 for Pasta     Price AUD 10\n' \
                             'Enter 6 for Pizza     Price AUD 20\n' \
                             'Enter 7 for drinks menu'
        else:
            self.menu_text = 'Enter 1 for Noodles   Price AUD 2\n' \
                             'Enter 2 for Sandwich  Price AUD 4\n' \
                             'Enter 3 for Dumpling  Price AUD 6\n' \
                             'Enter 4 for Muffins   Price AUD 8\n' \
                             'Enter 5 for Pasta     Price AUD 10\n' \
                             'Enter 6 for Pizza     Price AUD 20\n' \
                             'Enter 7 for Checkout'
        self.allowed_input = ['1', '2', '3', '4', '5', '6', '7']

    def _user_choice_processing(self, user_choice):
        if user_choice == '7' and self.show_drinks:
            DrinksMenu().execute()
        elif user_choice == '7' and not self.show_drinks:
            pass  # todo to checkout
        else:
            for item in self.items:
                if item.id == int(user_choice):
                    current_order.add_item(item)
                    print(f'\n{item.name} added to your order. Total price = {current_order.get_total_price()} AUD\n')
                    break
            FoodMenu(show_drinks=self.show_drinks).execute()


class DrinksMenu(Menu):
    def __init__(self):
        super().__init__()
        self.items = [
            MenuItem(1, 'Coffee', 2),
            MenuItem(2, 'Colddrink', 4),
            MenuItem(3, 'Shake', 6),
        ]
        self.menu_text = 'Enter 1 for Coffee        Price AUD 2\n' \
                         'Enter 2 for Colddrink     Price AUD 4\n' \
                         'Enter 3 for Shake         Price AUD 6\n' \
                         'Enter 4 for Checkout'
        self.allowed_input = ['1', '2', '3', '4']

    def _user_choice_processing(self, user_choice):
        if user_choice == '4':
            self.action = 'TO_CHECKOUT'
            pass # todo
        else:
            for item in self.items:
                if item.id == int(user_choice):
                    current_order.add_item(item)
                    print(f'\n{item.name} added to your order. Total price = {current_order.get_total_price()} AUD\n')
                    break
            DrinksMenu().execute()

# The main program begins
users = []

user = User('Sergey', 'Brisbane', '0987654321', 'S@2', '01/11/1987')
users.append(user)

account = Account()
current_order = Order()

while True:
    start_menu = StartMenu()
    start_menu.execute()
    if start_menu.action == 'QUIT':
        break
