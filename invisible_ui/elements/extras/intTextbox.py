"""Int textbox class."""

from invisible_ui.elements import Textbox


class IntTextbox(Textbox):
    """A text box that only allows integers."""

    def __init__(self, parent, title, value="", hidden = False):
        allowedChars = "1234567890"
        super().__init__(parent, title, value=value, hidden=hidden, allowedChars=allowedChars)
