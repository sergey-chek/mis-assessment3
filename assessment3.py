import re
import datetime
import copy


class User:
    def __init__(self, name, address, mobile_number, password, date_of_birth):
        self.name = name
        self.address = address
        self.mobile_number = mobile_number
        self.password = password
        self.date_of_birth = date_of_birth
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
        self.time = None
        self.number_of_persons = None
        self.name_of_person_picking_up = None
        self.distance = 0
        self.ordering_mode = None
        self.items = []

    def save(self):
        self.id = self._generate_id(orders)
        orders.append(copy.deepcopy(self))
        account.get_signed_in_user().orders.append(copy.deepcopy(self))

    def _generate_id(self, orders):
        if not orders:
            return 'S001'
        else:
            max_id = int(orders[0].id[1:4])
            for order in orders:
                if int(order.id[1:4]) > max_id:
                    max_id = int(order.id[1:4])
            new_id = 'S{:03}'.format(max_id + 1)
            return new_id

    def set_ordering_mode(self, ordering_mode):
        self.ordering_mode = ordering_mode

    def reset(self):
        self.id = None
        self.date = None
        self.time = None
        self.number_of_persons = None
        self.name_of_person_picking_up = None
        self.distance = 0
        self.ordering_mode = None
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item.price
        return round(total_price, 2)

    def get_total_price_with_charges(self):
        return round(self.get_total_price() + self.get_service_charges(), 2)

    def get_service_charges(self):
        if self.ordering_mode == 'SELF_PICKUP':
            return 0
        elif self.ordering_mode == 'DINE_IN':
            return self.get_total_price() * 0.15
        elif self.ordering_mode == 'HOME_DELIVERY':
            if 0 < self.distance <= 5:
                return 5
            elif 5 < self.distance <= 10:
                return 10
            elif 10 < self.distance <= 15:
                return 15
            else:
                return 0


class Account:
    def __init__(self):
        self.signed_in_user = None
        self.action = None

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

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action

    def reset_action(self):
        self.action = None


class Utils:
    def __init__(self):
        pass

    def get_user_choice(self, allowed_input):
        while True:
            try:
                user_choice = input('>>> ').upper()
                if user_choice in allowed_input:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Invalid value, please try again.')
        return user_choice


class Menu:
    def __init__(self):
        self.menu_text = ''
        self.allowed_input = []
        self.action = ''

    def execute(self):
        ''' TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
        ''' TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
        print('--------------------------------------TESTING-------------------------------------')
        for user in users:
            print(f'SAVED USER:\n\tname={user.name}, address={user.address}, mobile={user.mobile_number}, '
                  f'\n\tpass={user.password}, dob={user.date_of_birth}, orders={user.orders}')
        print(f'CURRENT_ORDER:\n\tid={current_order.id}, date={current_order.date}, time={current_order.time}, num_of_persons={current_order.number_of_persons}, '
              f'\n\tname={current_order.name_of_person_picking_up}, distance={current_order.distance}, mode={current_order.ordering_mode}, '
              f'\n\titems={current_order.items}, total_price={current_order.get_total_price()}, charges={current_order.get_service_charges()}')
        for order in orders:
            print(f'SAVED ORDER:\n\tid={order.id}, date={order.date}, time={order.time}, num_of_persons={order.number_of_persons}, '
                  f'\n\tname={order.name_of_person_picking_up}, distance={order.distance}, mode={order.ordering_mode}, '
                  f'\n\titems={order.items}, total_price={order.get_total_price()}, charges={order.get_service_charges()}')
        print('--------------------------------------TESTING-------------------------------------')
        ''' TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
        ''' TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
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
        return Utils().get_user_choice(self.allowed_input)

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
        if user_choice == self.allowed_input[0]:     # 1 Sign Up
            account.sign_up()
        elif user_choice == self.allowed_input[1]:   # 2 Sign In
            if account.is_signed_in():
                SignInMenu().execute()
            elif account.sign_in():
                SignInMenu().execute()
        elif user_choice == self.allowed_input[2]:   # 3 Quit
            print('\nThank you for using the Application!')
            account.set_action('QUIT')


class SignInMenu(Menu):
    def __init__(self):
        super().__init__()
        self.menu_text = '\n\tMAIN MENU --> SIGNED IN MENU:\n\t' \
                         'Please Enter 2.1 to Start Ordering.\n\t' \
                         'Please Enter 2.2 to Print Statistics.\n\t' \
                         'Please Enter 2.3 for Logout.\n'
        self.allowed_input = ['2.1', '2.2', '2.3']

    def execute(self):
        self._show_menu()
        user_choice = self._get_user_choice()
        self._user_choice_processing(user_choice)
        if account.get_action() == 'CANCEL_ORDER':
            self.execute()

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
        if account.get_action() == 'TO_ORDERING_MENU':
            account.reset_action()
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
            current_order.set_ordering_mode('DINE_IN')
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
            account.set_action('TO_ORDERING_MENU')


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
            self._checkout()
        else:
            for item in self.items:
                if item.id == int(user_choice):
                    current_order.add_item(item)
                    print(f'\n{item.name} added to your order. Total price = {current_order.get_total_price()} AUD\n')
                    break
            FoodMenu(show_drinks=self.show_drinks).execute()

    def _checkout(self):
        print(f'The total amount to be paid: {current_order.get_total_price()} AUD')
        print('\nPlease Enter Y to proceed to Checkout or Enter N to cancel the order:')
        user_choice = Utils().get_user_choice(['Y','N'])
        if user_choice == 'N':
            current_order.reset()
            account.set_action('CANCEL_ORDER')
        elif user_choice == 'Y':
            if not account.get_signed_in_user().address:
                print('\nYou have not mentioned your address, while signing up.\n'
                      'Please Enter Y if would like to enter your address.\n'
                      'Enter N if you would like to select other mode of order.')
                user_choice = Utils().get_user_choice(['Y', 'N'])
                if user_choice == 'Y':
                    account.get_signed_in_user().address = input('\nEnter address: ')
                elif user_choice == 'N':
                    current_order.reset()
                    account.set_action('TO_ORDERING_MENU')
            if account.get_action() != 'TO_ORDERING_MENU':
                if current_order.ordering_mode == 'DINE_IN':
                    service_charges = current_order.get_service_charges()
                    total_amount = current_order.get_total_price_with_charges()
                    print(f'\nYour total payable amount is: AUD {total_amount} including AUD {service_charges} for Service Charges')
                elif current_order.ordering_mode == 'SELF_PICKUP':
                    total_amount = current_order.get_total_price_with_charges()
                    print(f'\nYour total payable amount is: AUD {total_amount}')
                elif current_order.ordering_mode == 'HOME_DELIVERY':
                    total_amount = current_order.get_total_price_with_charges()
                    print(f'\nYour total payable amount is: AUD {total_amount} and there will be  an additional charges for Delivery')
                print('\nDo you want to proceed? [Y, N]: ')
                user_choice = Utils().get_user_choice(['Y', 'N'])
                if user_choice == 'N':
                    current_order.reset()
                    account.set_action('CANCEL_ORDER')
                elif user_choice == 'Y':
                    if current_order.ordering_mode == 'DINE_IN':
                        current_order.date = input('Please enter the Date of Booking for Dine in [DD/MM/YYYY]: ')
                        current_order.time = input('Please enter the Time of Booking for Dine in [HH:MM]: ')
                        current_order.number_of_persons = input('Please enter the Number of Persons: ')
                        current_order.save()
                        print('Thank you for entering the details, Your Booking is Confirmed.')
                    elif current_order.ordering_mode == 'SELF_PICKUP':
                        current_order.date = input('Please enter the Date of Pick up [DD/MM/YYYY]: ')
                        current_order.time = input('Please enter the Time of Pick up [HH:MM]: ')
                        current_order.name_of_person_picking_up = input('Please enter the Name of person picking up: ')
                        current_order.save()
                        print('Thank you for entering the details, Your Booking is Confirmed.')
                    elif current_order.ordering_mode == 'HOME_DELIVERY':
                        current_order.date = input('Please enter the Date of Delivery [DD/MM/YYYY]: ')
                        current_order.time = input('Please enter the Time of Delivery [HH:MM]: ')
                        while True:
                            try:
                                current_order.distance = int(input('Please enter the Distance from the restaurant: '))
                                break
                            except ValueError:
                                print('Enter an integer number.')
                        if not (0 < current_order.distance <= 15):
                            print('The distance more than the applicable limits. Do you want to pick up the Order?'
                                  '\n\tY - Yes, I want to pick it up.'
                                  '\n\tN - No, I want to cancel the Order.')
                            user_choice = Utils().get_user_choice(['Y', 'N'])
                            if user_choice == 'Y':
                                current_order.distance = 0
                                current_order.ordering_mode = 'SELF_PICKUP'
                            elif user_choice == 'N':
                                account.set_action('CANCEL_ORDER')
                        if account.get_action() != 'CANCEL_ORDER':
                            current_order.save()
                            print('Thank you for your Order, Your Order has been Confirmed.')
                    current_order.reset()

class DrinksMenu(FoodMenu):
    def __init__(self):
        super().__init__(show_drinks=True)
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
            self._checkout()
        else:
            for item in self.items:
                if item.id == int(user_choice):
                    current_order.add_item(item)
                    print(f'\n{item.name} added to your order. Total price = {current_order.get_total_price()} AUD\n')
                    break
            DrinksMenu().execute()

# The main program begins
users = []
orders = []

''' TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
user1 = User('Sergey1', 'Brisbane1', '0987654321', 'S@2', '01/11/1111')
user2 = User('Sergey2', 'Brisbane2', '0987654322', 'S@2', '02/11/1111')
users.append(user1)
users.append(user2)
''' TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''

account = Account()
current_order = Order()

while True:
    start_menu = StartMenu()
    start_menu.execute()
    if account.get_action() == 'QUIT':
        break
