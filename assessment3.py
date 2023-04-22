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


class Account:
    def __init__(self):
        self.signed_in_user = None

    def is_signed_in(self):
        if self.signed_in_user:
            return True
        else:
            return False

    def set_account(self, user):
        self.signed_in_user = user

    def exit_account(self):
        self.signed_in_user = None


class Menu:
    def __init__(self):
        self.menu_text = ''
        self.allowed_input = []

    def show_menu(self):
        """The method prints menu"""
        print(self.menu_text)

    def get_user_choice(self):
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

    def user_choice_processing(self, user_choice):
        """The method must contain the business logic of menu in the inherited classes"""
        raise NotImplementedError


class StartMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\n' \
                         'Please Enter 1 for Sign up.\n' \
                         'Please Enter 2 for Sign in.\n' \
                         'Please Enter 3 for Quit.'
        self.allowed_input = ['1', '2', '3']

    def user_choice_processing(self, user_choice):
        if user_choice == self.allowed_input[0]:     # 1 Sign Up
            self._sign_up()
        elif user_choice == self.allowed_input[1]:   # 2 Sign In
            if self._sign_in():
                sign_in_menu = SignInMenu()
                sign_in_menu.show_menu()
                user_choice = sign_in_menu.get_user_choice()
                sign_in_menu.user_choice_processing(user_choice)
        elif user_choice == self.allowed_input[2]:   # 3 Quit
            print('\nThank you for using the Application!')
            return 'quit'

    def _sign_up(self):
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
                if (user.mobile_number == mobile_number):
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

    def _sign_in(self):
        mobile_number = input('\nPlease enter your Username (Mobile Number): ')
        password = input('Please enter your password: ')
        current_user = None
        for user in users:
            if (user.mobile_number == mobile_number):
                current_user = user
                break
        if not current_user:
            print('You have not Signed up with this contact number, please Sign up first.')
        else:
            if (current_user.password == password):
                account.set_account(current_user)   # Set info that current user Signed in
                print('\nYou have successfully Signed in')
                print(f'Welcome {current_user.name}')
                return True
            else:
                print('\nYou have entered the wrong Password. You will be directed to the main menu.')
                return False


class SignInMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\t' \
                         'Please Enter 2.1 to Start Ordering.\n\t' \
                         'Please Enter 2.2 to Print Statistics.\n\t' \
                         'Please Enter 2.3 for Logout.'
        self.allowed_input = ['2.1', '2.2', '2.3']

    def user_choice_processing(self, user_choice):
        if user_choice == self.allowed_input[0]:    # 2.1 Start Ordering
            self._start_ordering()
            ordering_menu = OrderingMenu()
            ordering_menu.show_menu()
            user_choice = ordering_menu.get_user_choice()
            ordering_menu.user_choice_processing(user_choice)
        elif user_choice == self.allowed_input[1]:  # 2.2 Print Statistics
            self._print_statistics()
        elif user_choice == self.allowed_input[2]:  # 2.3 Logout
            self._logout()

    def _start_ordering(self):
        pass  # TODO

    def _print_statistics(self):
        pass  # TODO

    def _logout(self):
        pass  # TODO
        account.exit_account()


class OrderingMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\t2.1\n\t\t' \
                         'Please Enter 1 for Dine in.\n\t\t' \
                         'Please Enter 2 for Order Online.\n\t\t' \
                         'Please Enter 3 to go to Login Page.'
        self.allowed_input = ['1', '2', '3']

    def user_choice_processing(self, user_choice):
        if user_choice == self.allowed_input[0]:    # 1 Dine In
            self._dine_in()
        elif user_choice == self.allowed_input[1]:  # 2 Order Online
            self._order_online()
        elif user_choice == self.allowed_input[2]:  # 3 Login Page
            self._login_page()

    def _dine_in(self):
        pass  # TODO

    def _order_online(self):
        pass  # TODO

    def _login_page(self):
        pass  # TODO

# The main program begins
users = []
account = Account()

while True:
    start_menu = StartMenu()
    start_menu.show_menu()
    user_choice = start_menu.get_user_choice()
    if start_menu.user_choice_processing(user_choice) == 'quit':
        break
