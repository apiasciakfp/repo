import sys

from cardmultigame.interface.ui_logic_dispatcher import UiLogicDispatcher


def main() -> None:
    dispatcher = UiLogicDispatcher()
    builder = ""

    while True:
        print("Please, input the command with proper separators\n")

        orders = input()
        builder = builder + orders.strip()

        if "SETUP" in orders:
            actual_orders = builder
            builder = ""
            dispatcher.setup_game(actual_orders)
        elif "EXIT" in orders:
            break
        else:
            dispatcher.do_stuff(orders)

        sys.stdout.write(dispatcher.display_current_state() + "\n" + "\n")


if __name__ == "__main__":
    main()
