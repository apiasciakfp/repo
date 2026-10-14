class GameState(dict):
    """EncapsulatedContext pattern — a dictionary of string -> object.

    This is for readability ONLY. Do not do this in real-world systems unless you REALLY
    know what you are doing. The missing-key handling exists only to make this easier to
    work with for people less accustomed to dictionaries; in normal real-world stuff, do
    not do this.
    """

    def __missing__(self, key):
        return None
