from cardmultigame.gamemanagers.create_game_manager import CreateGameManager


class UiLogicDispatcher:
    def __init__(self) -> None:
        self._game_manager = CreateGameManager().empty()

    def do_stuff(self, orders: str) -> None:
        self._game_manager.execute_orders(orders)

    def setup_game(self, orders: str) -> None:
        self._game_manager = CreateGameManager().defaults_with_orders(orders)

    def display_current_state(self) -> str:
        current_state = self._game_manager.current_state()
        return (";" + "\n").join(f"[{key}, {value}]" for key, value in current_state.items())
