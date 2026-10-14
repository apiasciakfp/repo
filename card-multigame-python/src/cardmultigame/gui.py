"""Tkinter front-end: click a card to guess it. The text REPL in program.py stays as it is."""

import tkinter as tk
from importlib.resources import files

from cardmultigame.interface.gui_presenter import BACK_FILE, GuiSession, asset_file_for

GRID_SHRINK = 5
SHOWCASE_SHRINK = 3
HISTORY_SHRINK = 9
HISTORY_PAIRS_PER_ROW = 6
TABLE_COLOUR = "#2e6b3f"
FADE_TOWARDS_WHITE = 0.65


class CardImages:
    def __init__(self) -> None:
        self._assets = files("cardmultigame") / "assets"
        self._originals: dict[str, tk.PhotoImage] = {}
        self._cache: dict[tuple[str, int, bool], tk.PhotoImage] = {}

    def get(self, file_name: str, shrink: int, faded: bool = False) -> tk.PhotoImage:
        key = (file_name, shrink, faded)
        if key not in self._cache:
            image = self._original(file_name).subsample(shrink)
            self._cache[key] = _faded(image) if faded else image
        return self._cache[key]

    def _original(self, file_name: str) -> tk.PhotoImage:
        if file_name not in self._originals:
            self._originals[file_name] = tk.PhotoImage(file=str(self._assets / file_name))
        return self._originals[file_name]


def _faded(image: tk.PhotoImage) -> tk.PhotoImage:
    tcl = image.tk
    rows = [tcl.splitlist(row) for row in tcl.splitlist(tcl.call(image.name, "data"))]

    def lighten(pixel: str) -> str:
        channels = (int(pixel[i : i + 2], 16) for i in (1, 3, 5))
        return "#" + "".join(
            f"{round(c + (255 - c) * FADE_TOWARDS_WHITE):02x}" for c in channels
        )

    faded = tk.PhotoImage(width=image.width(), height=image.height())
    faded.put(" ".join("{" + " ".join(lighten(p) for p in row) + "}" for row in rows))
    return faded


class CardGameApp:
    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._session = GuiSession()
        self._images = CardImages()
        self._screen: tk.Frame | None = None

        root.title("Card Multigame — Guess a Card!")
        root.configure(bg=TABLE_COLOUR)
        self._show_setup()

    def _replace_screen(self) -> tk.Frame:
        if self._screen is not None:
            self._screen.destroy()
        self._screen = tk.Frame(self._root, bg=TABLE_COLOUR, padx=16, pady=16)
        self._screen.pack(fill="both", expand=True)
        return self._screen

    def _show_setup(self) -> None:
        screen = self._replace_screen()
        label_style = {"bg": TABLE_COLOUR, "fg": "white"}

        tk.Label(screen, text="Guess a Card!", font=("Helvetica", 20, "bold"), **label_style).pack(pady=(0, 12))
        tk.Label(screen, image=self._images.get(BACK_FILE, SHOWCASE_SHRINK), bg=TABLE_COLOUR).pack()

        turns_row = tk.Frame(screen, bg=TABLE_COLOUR)
        turns_row.pack(pady=(12, 4))
        tk.Label(turns_row, text="Max turns:", **label_style).pack(side="left")
        max_turns = tk.IntVar(value=5)
        # The default deck has 24 cards and every guess draws one, so more turns than that would empty it.
        tk.Spinbox(turns_row, from_=1, to=24, width=4, textvariable=max_turns, state="readonly").pack(side="left", padx=6)

        red_black = tk.BooleanVar(value=False)
        tk.Checkbutton(
            screen,
            text="Red/Black variant (only the colour has to match)",
            variable=red_black,
            selectcolor=TABLE_COLOUR,
            activebackground=TABLE_COLOUR,
            activeforeground="white",
            **label_style,
        ).pack(pady=4)

        tk.Button(screen, text="Play", width=12, command=lambda: self._start(max_turns.get(), red_black.get())).pack(pady=(12, 0))

    def _start(self, max_turns: int, red_black_variant: bool) -> None:
        self._session.start(max_turns, red_black_variant)
        self._show_table()

    def _show_table(self) -> None:
        screen = self._replace_screen()

        self._status = tk.Label(screen, bg=TABLE_COLOUR, fg="white", font=("Helvetica", 12), anchor="w")
        self._status.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 12))

        self._grid = tk.Frame(screen, bg=TABLE_COLOUR)
        self._grid.grid(row=1, column=0, sticky="n")
        self._card_buttons: dict[str, tk.Label] = {}
        self._build_card_grid()

        showcase = tk.Frame(screen, bg=TABLE_COLOUR, padx=24)
        showcase.grid(row=1, column=1, sticky="n")
        self._your_guess = self._showcase_slot(showcase, "Your guess", 0)
        self._magician_draw = self._showcase_slot(showcase, "Magician's draw", 1)

        self._banner = tk.Label(showcase, bg=TABLE_COLOUR, font=("Helvetica", 22, "bold"))
        self._banner.grid(row=2, column=0, columnspan=2, pady=(16, 4))
        self._new_game = tk.Button(showcase, text="New game", command=self._show_setup)

        self._history = tk.Frame(screen, bg=TABLE_COLOUR)
        self._history.grid(row=2, column=0, columnspan=2, sticky="w", pady=(16, 0))

        self._refresh()

    def _build_card_grid(self) -> None:
        cards = self._session.all_cards
        suits = list(dict.fromkeys(code[-1] for code in cards))
        ranks = list(dict.fromkeys(code[:-1] for code in cards))

        for code in cards:
            button = tk.Label(self._grid, bg=TABLE_COLOUR, cursor="hand2", borderwidth=0)
            button.grid(row=suits.index(code[-1]), column=ranks.index(code[:-1]), padx=3, pady=3)
            button.bind("<Button-1>", lambda _event, c=code: self._guess(c))
            self._card_buttons[code] = button

    def _showcase_slot(self, parent: tk.Frame, caption: str, column: int) -> tk.Label:
        tk.Label(parent, text=caption, bg=TABLE_COLOUR, fg="white").grid(row=0, column=column, padx=6)
        slot = tk.Label(parent, bg=TABLE_COLOUR)
        slot.grid(row=1, column=column, padx=6)
        return slot

    def _guess(self, card_code: str) -> None:
        if self._session.guess(card_code) is not None:
            self._refresh()

    def _refresh(self) -> None:
        drawn = self._session.drawn_cards()
        finished = self._session.is_finished()

        for code, button in self._card_buttons.items():
            # Drawn cards are faded but stay clickable: noticing they can't come up again is the player's job.
            button.configure(
                image=self._images.get(asset_file_for(code), GRID_SHRINK, faded=code in drawn),
                cursor="arrow" if finished else "hand2",
            )

        last = self._session.history[-1] if self._session.history else None
        self._your_guess.configure(image=self._showcase_image(last.guessed if last else None))
        self._magician_draw.configure(image=self._showcase_image(last.drawn if last else None))
        self._status.configure(text=self._session.status_text())

        self._render_history()

        outcome = self._session.outcome()
        if outcome == "Victory":
            self._banner.configure(text="Victory!", fg="#ffd34d")
        elif outcome == "Defeat":
            self._banner.configure(text="Defeat", fg="#ff8a80")
        if finished:
            self._new_game.grid(row=3, column=0, columnspan=2)

    def _showcase_image(self, card_code: str | None) -> tk.PhotoImage:
        return self._images.get(asset_file_for(card_code) if card_code else BACK_FILE, SHOWCASE_SHRINK)

    def _render_history(self) -> None:
        for child in self._history.winfo_children():
            child.destroy()

        for index, guess_round in enumerate(self._session.history):
            pair = tk.Frame(self._history, bg="#ffd34d" if guess_round.hit else TABLE_COLOUR, padx=2, pady=2)
            pair.grid(row=index // HISTORY_PAIRS_PER_ROW, column=index % HISTORY_PAIRS_PER_ROW, padx=6, pady=4)
            for side, code in enumerate((guess_round.guessed, guess_round.drawn)):
                image = self._images.get(asset_file_for(code) if code else BACK_FILE, HISTORY_SHRINK)
                tk.Label(pair, image=image, borderwidth=0).grid(row=0, column=side, padx=1)


def main() -> None:
    root = tk.Tk()
    CardGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
