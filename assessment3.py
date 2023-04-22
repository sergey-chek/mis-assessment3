class Menu:
    def __init__(self):
        self.START_MENU_TEXT = '\n\n' \
                               'Please Enter 1 for Sign up.\n' \
                               'Please Enter 2 for Sign in.\n' \
                               'Please Enter 3 for Quit.'
        self.SIGN_IN_MENU_TEXT = '\n\n\t' \
                                 'Please Enter 2.1 to Start Ordering.\n\t' \
                                 'Please Enter 2.2 to Print Statistics.\n\t' \
                                 'Please Enter 2.3 for Logout.'
    def get_start_menu_choice(self):
        """
        The method gets the user's choice for the start menu.
        If the user enters an incorrect value (not equal to 1, 2 or 3), then a re-entry of the value is requested.
        """
        while True:
            print(self.START_MENU_TEXT)
            try:
                start_menu_choice = int(input('>>> '))
                if start_menu_choice in {1, 2, 3}:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Invalid value, please try again.')
        return start_menu_choice

    def get_sign_in_menu_choice(self):
        """
        The method gets the user's choice for the Sign In menu.
        If the user enters an incorrect value (not equal to 2.1, 2.2 or 2.3), then a re-entry of the value is requested.
        """
        while True:
            print(self.SIGN_IN_MENU_TEXT)
            try:
                sign_in_menu_choice = input('>>> ').strip()
                if sign_in_menu_choice in {'2.1', '2.2', '2.3'}:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Invalid value, please try again.')
        return sign_in_menu_choice