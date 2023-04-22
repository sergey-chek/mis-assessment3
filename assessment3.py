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
            print('start menu 1 executed')  # TODO
            return False
        elif user_choice == self.allowed_input[1]:   # 2 Sign In
            sign_in_menu = SignInMenu()
            sign_in_menu.show_menu()
            user_choice = sign_in_menu.get_user_choice()
            sign_in_menu.user_choice_processing(user_choice)
            return False
        elif user_choice == self.allowed_input[2]:   # 3 Quit
            print('\nThank you for using the Application!')
            return True


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
            ordering_menu = OrderingMenu()
            ordering_menu.show_menu()
            user_choice = ordering_menu.get_user_choice()
            ordering_menu.user_choice_processing(user_choice)
        elif user_choice == self.allowed_input[1]:  # 2.2 Print Statistics
            print('sign in menu 2.2 executed')  # TODO
        elif user_choice == self.allowed_input[2]:  # 2.3 Logout
            print('sign in menu 2.3 executed')  # TODO


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
            print('ordering menu 1 executed')  # TODO
        elif user_choice == self.allowed_input[1]:  # 2 Order Online
            print('ordering menu 2 executed')  # TODO
        elif user_choice == self.allowed_input[2]:  # 3 Login Page
            print('ordering menu 3 executed')  # TODO


# The main program begins

while True:
    start_menu = StartMenu()
    start_menu.show_menu()
    user_choice = start_menu.get_user_choice()
    if start_menu.user_choice_processing(user_choice):
        break
