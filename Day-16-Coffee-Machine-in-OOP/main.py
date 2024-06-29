# import necessary modules
from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

# instantiate the classes
menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

# boolean to check if the coffee machine is on
is_on = True


while is_on:
    options = menu.get_items()
    
    choice = input(f'What would you like? ({options}): ').lower()

    if choice == 'off':
        is_on = False

    elif choice == 'report':
        money_machine.report()
        coffee_maker.report()

    else:
        drink = menu.find_drink(choice)

        if (coffee_maker.is_resource_sufficient(drink)
                and money_machine.make_payment(drink.cost)):
            coffee_maker.make_coffee(drink)