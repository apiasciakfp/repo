from cardmultigame.usecases.gameactions.add10c_or_draw_a_card import Add10COrDrawACard
from cardmultigame.usecases.gameactions.add_queen_of_hearts_to_deck import AddQueenOfHeartsToDeck
from cardmultigame.usecases.gameactions.draw_single_card_action import DrawSingleCardAction
from cardmultigame.usecases.gameactions.i_game_action import IGameAction


class CreateGameActions:
    def having_orders(self, actions_to_perform: str) -> list[IGameAction]:
        tokens = actions_to_perform.split()

        actions: list[IGameAction] = []
        for token in tokens:
            sanitized = token.strip(",")

            if sanitized == "drawSingleCard":
                actions.append(DrawSingleCardAction())
            if sanitized == "addQH":
                actions.append(AddQueenOfHeartsToDeck())
            if sanitized == "add10cOrDraw":
                actions.append(Add10COrDrawACard())

        return actions
