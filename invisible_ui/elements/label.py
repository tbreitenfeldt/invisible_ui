"""Label class."""

import logging

from invisible_ui.elements.element import Element


class Label(Element):
    """This element does nothing, and just acts as a header in menus ETC."""

    def __init__(self, parent, title):
        """Set the title, and alter the help message."""
        super().__init__(parent, title, "Label", logger=logging.getLogger("Label"))
        self.type = "Label"
        self.help = "This object has no controls."

    def get_title(self):
        """Get the title."""
        return "{}".format(self.title)
