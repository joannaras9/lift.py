#!/usr/bin/env python3.4

import time
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from random import randint

__name____ = "Joanna Rasztar"
__author__ = "D15124542"


class InvalidValueException(Exception):
    """ Custom Exception Class """
    def __init__(self, message):
        self.message = message


class Building:
    _queue = None
    _floors = None
    _elevator = None

    def __init__(self, floors, elevator, queue):
        self.floors = floors
        self.elevator = elevator
        self.queue = queue

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, queue):
        """
        Sets and validate the queue. Makes sure that the queue it's a list

        :param queue
        :raise AttributeError
        """
        if type(queue) is not list:
            t = str(type(queue))
            raise AttributeError("\nError: 'queue' must be and instance of object list " + t + " given.")
        else:
            self._queue = queue

    @property
    def floors(self):
        return self._floors

    @floors.setter
    def floors(self, floors):
        """
        Sets and validate the number of floors

        :param floors
        :raise InvalidValueException
        """
        if floors <= 0:
            raise InvalidValueException("\nError: The number of floors has to be greater than 0.")
        else:
            self._floors = floors

    @property
    def elevator(self):
        return self._elevator

    @elevator.setter
    def elevator(self, elevator):
        """
        Sets and validate the Elevator
        Makes sure that is an instance of the class Elevator

        :raise AttributeError
        """
        if not isinstance(elevator, Elevator):
            t = str(type(elevator))
            raise AttributeError("\nError: 'elevator' must be and instance of class Elevator " + t + " given.")
        self._elevator = elevator

    def move_elevator(self, floor=None, direction=None):
        """
        Moves the elevator and return the current floor
        Makes sure that the elevator moves inside the building only :)

        :param direction:
        :param floor:
        :returns int
        """
        if direction:
            self._elevator.direction = direction
        if floor:
            if floor - 1 in range(self._floors):
                self._elevator.floor = floor
                if not direction:
                    self._elevator.direction = 'going_up'
                return self._elevator.floor
            else:
                raise AttributeError("\nError: 'floor' must be between 1 and " + str(self._floors))
        if not self._elevator.direction:
            self._elevator.direction = 'going_up'
            self._elevator.floor = 1
        else:
            if self._elevator.direction == 'going_up':
                if self._elevator.floor >= self._floors:
                    self._elevator.direction = 'going_down'
                    self._elevator.floor -= 1
                else:
                    self._elevator.floor += 1
            elif self._elevator.direction == 'going_down':
                if self._elevator.floor <= 1:
                    self._elevator.direction = 'going_up'
                    self._elevator.floor += 1
                else:
                    self._elevator.floor -= 1
        return self._elevator.floor

    def __str__(self):
        return "\n####\nYour building has {} floors and equipped with one elevator and you have {} customers\n####". \
            format(self._floors, len(self.queue))


class Elevator:
    _floor = None
    _payload = []
    _direction = None

    def __init__(self, floor=0):
        self.floor = floor

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @property
    def floor(self):
        return self._floor

    @floor.setter
    def floor(self, floor):
        self._floor = floor

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload


class Customer:
    def __init__(self, moves_in, moves_out):
        self.moves_in = moves_in
        self.moves_out = moves_out


class Window(Frame):
    def __init__(self, master=Tk()):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('ELEVATOR SIMULATOR APP')
        self.master.maxsize(1000, 600)
        self.master.minsize(500, 150)
        self.master.eval('tk::PlaceWindow %s center' % self.master.winfo_pathname(self.master.winfo_id()))
        self.display_box = scrolledtext.ScrolledText(self.master)
        self.init_window()

    def init_window(self):

        label_title = Label(self.master, text='Elevator Simulator', font=("Helvetica", 12))
        label_title.grid(row=0, column=1, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

        label_floors = Label(self.master, text='Num. floors:')
        label_floors.grid(row=1, column=0, sticky=E, padx=5, pady=5)
        input_floors = Entry(self.master)
        input_floors.insert(INSERT, 5)
        input_floors.grid(row=1, column=1, padx=5, pady=5)

        label_customers = Label(self.master, text='Num. customers:')
        label_customers.grid(row=2, column=0, sticky=E, padx=5, pady=5)
        input_customers = Entry(self.master)
        input_customers.insert(INSERT, 10)
        input_customers.grid(row=2, column=1, padx=5, pady=5)

        ttk.Separator(self.master).grid(row=3, columnspan=4, sticky=E + W, padx=5, pady=10)

        quit_button = Button(self.master, text='Quit', fg='white', bg='red', command=self.close_window)
        quit_button.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        run_other_button = Button(
            self.master,
            text='Run Other',
            fg='white',
            bg='green',
            command=lambda: self.other_strategy(input_floors.get(), input_customers.get())
        )
        run_other_button.grid(row=4, column=3, padx=5, pady=5, sticky=E)

        run_default_button = Button(
            self.master,
            text='Run Default',
            fg='white', bg='green',
            command=lambda: self.default_strategy(input_floors.get(), input_customers.get())
        )
        run_default_button.grid(row=4, column=2, padx=5, pady=5, sticky=E)

        self.display_box.grid(row=5, column=0, columnspan=4, rowspan=5, sticky=W + E + N + S, padx=5, pady=5)

    def default_strategy(self, floors, customers):
        """
        Pick up every customer regardless if he/she wants to go up or down

        :param floors: Number of floors the building will have
        :param customers: Number of customers
        :returns void
        """

        self.display_box.delete('1.0', END)

        floors = self.validate_input(floors)
        if isinstance(floors, str):
            self.display_box.insert(INSERT, floors + '\n')
            return False

        customers = self.validate_input(customers)
        if isinstance(customers, str):
            self.display_box.insert(INSERT, customers + '\n')
            return False

        queue = []
        for i in range(customers):
            moves_in = randint(1, floors)
            moves_out = randint(1, floors)
            c = Customer(moves_in, moves_out)
            queue.append(c)

        build = Building(floors=floors, elevator=Elevator(), queue=queue)

        count_moves = 0

        while build.queue or build.elevator.payload:
            build.move_elevator()
            if build.elevator.payload:
                for p, c in enumerate(build.elevator.payload):
                    # Check if any customer wants out.
                    if c.moves_out == build.elevator.floor:
                        build.elevator.payload.pop(p)  # Remove customer from payload
            if build.queue:
                for i, customer in enumerate(build.queue):
                    if customer.moves_in == customer.moves_out:
                        # Check if the customer is stupid and kick his ass out from the queue
                        build.queue.pop(i)
                    elif customer.moves_in == build.elevator.floor:
                        # Check if any customer wants in.
                        build.elevator.payload.append(customer)
                        build.queue.pop(i)  # Remove customer from queue
            count_moves += 1
            self.display_box.insert(INSERT, '\n#######\n' + 'Elevator on floor: ' + str(build.elevator.floor) + '\n')
            self.display_box.insert(INSERT, 'Num. customers in queue: ' + str(len(build.queue)) + '\n')
            self.display_box.insert(INSERT, 'Num. customers in elevator: ' + str(len(build.elevator.payload)) + '\n')
        self.display_box.insert(INSERT, '\nCounter elevator moves for DEFAULT strategy: ' + str(count_moves) + '\n')

    def other_strategy(self, floors, customers):
        """
        Pick up customer depending of the elevator direction
        If the elevator goes up will pick up only customers who wants to go up and vice versa

        :param floors: Number of floors the building will have
        :param customers: Number of customers
        :returns void
        """

        self.display_box.delete('1.0', END)

        floors = self.validate_input(floors)
        if isinstance(floors, str):
            self.display_box.insert(INSERT, floors + '\n')
            return False

        customers = self.validate_input(customers)
        if isinstance(customers, str):
            self.display_box.insert(INSERT, customers + '\n')
            return False

        queue = []
        for i in range(customers):
            moves_in = randint(1, floors)
            moves_out = randint(1, floors)
            c = Customer(moves_in, moves_out)
            queue.append(c)

        build = Building(floors=floors, elevator=Elevator(), queue=queue)

        count_moves = 0

        while build.queue or build.elevator.payload:
            build.move_elevator()
            if build.elevator.payload:
                for p, c in enumerate(build.elevator.payload):
                    # Check if any customer wants out.
                    if c.moves_out == build.elevator.floor:
                        build.elevator.payload.pop(p)  # Remove customer from payload
            if build.queue:
                for i, customer in enumerate(build.queue):
                    if customer.moves_in == customer.moves_out:
                        # Check if the customer is stupid and kick his ass out from the queue
                        build.queue.pop(i)
                    elif customer.moves_in == build.elevator.floor:
                        if customer.moves_in > customer.moves_out and build.elevator.direction == 'going_up':
                            build.elevator.payload.append(customer)
                            build.queue.pop(i)  # Remove customer from queue
                        if customer.moves_in < customer.moves_out and build.elevator.direction == 'going_down':
                            build.elevator.payload.append(customer)
                            build.queue.pop(i)  # Remove customer from queue
            count_moves += 1
            self.display_box.insert(INSERT, '\n#######\n' + 'Elevator on floor: ' + str(build.elevator.floor) + '\n')
            self.display_box.insert(INSERT, 'Num. customers in queue: ' + str(len(build.queue)) + '\n')
            self.display_box.insert(INSERT, 'Num. customers in elevator: ' + str(len(build.elevator.payload)) + '\n')
        self.display_box.insert(INSERT, '\nCounter elevator moves for DEFAULT strategy: ' + str(count_moves) + '\n')

    @classmethod
    def validate_input(cls, user_input):
        """
        Validate the user input. If the input is valid returns integer representation of the user input.
        In case of an invalid input prints out an error message.

        :param user_input:
        :returns integer | string
        """

        if not user_input:
            return 'Error: You must insert a value.'
        elif not user_input.isnumeric():
            return 'Error: Your value is not numeric.'
        elif int(user_input) <= 0:
            return "Error: Your value must be greater than '0'."
        else:
            return int(user_input)

    @classmethod
    def close_window(cls):
        exit()


def is_valid_input(user_input):
    """
    Validate the user input. If the input is valid returns integer representation of the user input.
    In case of an invalid input prints out an error message.

    :param user_input:
    :returns integer | string
    """
    if user_input is '':
        print("Error: You must insert a value.")
    elif not user_input.isdigit():
        print("Error: Your value is not numeric.")
    elif int(user_input) <= 0:
        print("Error: Your value must be greater than '0'.")
    else:
        return int(user_input)
    return False


def run_default_strategy(floors, customers):
    """
    Pick up every customer regardless if he/she wants to go up or down

    :param floors: Number of floors the building will have
    :param customers: Number of customers
    :exception InvalidValueException
    :exception AttributeError
    :exception ValueError
    :returns void
    """

    queue = []
    for i in range(customers):
        moves_in = randint(1, floors)
        moves_out = randint(1, floors)
        c = Customer(moves_in, moves_out)
        queue.append(c)

    build = Building(floors=floors, elevator=Elevator(), queue=queue)

    count_moves = 0

    while build.queue or build.elevator.payload:
        build.move_elevator()
        if build.elevator.payload:
            for p, c in enumerate(build.elevator.payload):
                # Check if any customer wants out.
                if c.moves_out == build.elevator.floor:
                    build.elevator.payload.pop(p)  # Remove customer from payload
        if build.queue:
            for i, customer in enumerate(build.queue):
                if customer.moves_in == customer.moves_out:
                    # Check if the customer is stupid and kick his ass out from the queue
                    build.queue.pop(i)
                elif customer.moves_in == build.elevator.floor:
                    # Check if any customer wants in.
                    build.elevator.payload.append(customer)
                    build.queue.pop(i)  # Remove customer from queue
        count_moves += 1
        time.sleep(2)
        print('\n#######\n' + 'Elevator on floor: ' + str(build.elevator.floor))
        print('Num. customers in queue: ' + str(len(build.queue)))
        print('Num. customers in elevator: ' + str(len(build.elevator.payload)))

    print('Counter elevator moves for DEFAULT strategy: ', count_moves)


def run_other_strategy(floors, customers):
    """
    Pick up customer depending of the elevator direction
    If the elevator goes up will pick up only customers who wants to go up and vice versa

    :param floors: Number of floors the building will have
    :param customers: Number of customers
    :exception InvalidValueException
    :exception AttributeError
    :exception ValueError
    :returns void
    """

    queue = []
    for i in range(customers):
        moves_in = randint(1, floors)
        moves_out = randint(1, floors)
        c = Customer(moves_in, moves_out)
        queue.append(c)

    build = Building(floors=floors, elevator=Elevator(), queue=queue)

    count_moves = 0

    while build.queue or build.elevator.payload:
        build.move_elevator()
        if build.elevator.payload:
            for p, c in enumerate(build.elevator.payload):
                # Check if any customer wants out.
                if c.moves_out == build.elevator.floor:
                    build.elevator.payload.pop(p)  # Remove customer from payload
        if build.queue:
            for i, customer in enumerate(build.queue):
                if customer.moves_in == customer.moves_out:
                    # Check if the customer is stupid and kick his ass out from the queue
                    build.queue.pop(i)
                elif customer.moves_in == build.elevator.floor:
                    if customer.moves_in > customer.moves_out and build.elevator.direction == 'going_up':
                        build.elevator.payload.append(customer)
                        build.queue.pop(i)  # Remove customer from queue
                    if customer.moves_in < customer.moves_out and build.elevator.direction == 'going_down':
                        build.elevator.payload.append(customer)
                        build.queue.pop(i)  # Remove customer from queue
        count_moves += 1
        time.sleep(2)
        print('\n#######\n' + 'Elevator on floor: ' + str(build.elevator.floor))
        print('Num. customers in queue: ' + str(len(build.queue)))
        print('Num. customers in elevator: ' + str(len(build.elevator.payload)))

    print('Counter elevator moves for OTHER strategy: ', count_moves)


def main():

    interface = input("\nPlease insert 1 for GUI or 2 for CLI. [1]: ")
    if interface != '2':
        interface = '1'  # Default 1 GUI

    if interface == '1':
        app = Window()
        app.mainloop()

    if interface == '2':
        floors = ''
        while not floors:
            floors_input = input("\nPlease enter the number of floors for your building: ")
            floors = is_valid_input(floors_input)
            if not floors_input:
                continue
        customers = ''
        while not customers:
            customers_input = input("\nPlease enter the number of customers for your building: ")
            customers = is_valid_input(customers_input)
            if not customers_input:
                continue

        # For testing skip user inputs
        # floors = 5  # Comment this line in production
        # customers = 10  # Comment this line in production

        print('\n##### START DEFAULT STRATEGY SIMULATION #####\n')
        run_default_strategy(floors, customers)
        print('\n##### END DEFAULT STRATEGY SIMULATION #####\n')

        print('\n##### START OTHER STRATEGY SIMULATION #####\n')
        run_other_strategy(floors, customers)
        print('\n##### END OTHER STRATEGY SIMULATION #####\n')


if __name__ == "__main__":
    try:
        main()
    except InvalidValueException as e:
        #  Custom error Exception
        print(e)
        exit(1)
    except AttributeError as e:
        print(e)
        exit(1)
    except ValueError as e:
        #  Python error Exception
        print(e)
        exit(1)
