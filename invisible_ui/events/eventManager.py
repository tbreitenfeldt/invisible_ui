"""manage events for pygame related elements."""

from abc import ABC, abstractmethod
from logging import Logger

import pygame

from invisible_ui.events.handler import Handler


class EventManager(ABC):
    """
    This abstract base class is used to manage events for any child class that needs event handling

    Public methods:
    handle_event - an abstract method that is used to handle a given event by the child class

    add_handler - Adds an event handler to this session.

    remove_handler - Remove an event handler from this session.

    add_keydown - Adds a keydown event to be trapped by the session.

    add_keyup - Adds a keyup event to be handled by the session.
    """

    def __init__(self, logger=None):
        self._events = {}
        self._logger = logger

    @abstractmethod
    def handle_event(self, event):
        """
        An abstract method that must be overwritten by child classes used to handle events.

        event - the event to be handled

        returns true or false if the event could be handled here

        default code is given for this method, however subclasses must still override this method to insure the subclass has the correct behavior.
        """
        # loop through the handlers associated with the event type.
        for h in self._events.get(event.type, []):

            # Iterate through the handler's dictionary of event parameters 
            for k, v in h.params.items():
                # get the value of event.k, if none, return v
                if not v(getattr(event, k, v)):
                    break
            else:
                h.call_actions(event)
                if self._logger is not None:
                    self._logger.debug("Handle event: {}.".format(event))

                return True

        return False

    @property
    def events(self):
        """Return all event handlers."""
        return self._events

    @property
    def logger(self):
        """Return the curreunt logger if it is not None."""
        return self._logger

    @logger.setter
    def logger(self, logger):
        """Set the logger if is not None, and it is of type Logger."""
        if logger is None or not isinstance(logger, Logger):
            raise ValueError("Logger can not be set to None, and must be of type logging.Logger")

        self._logger = logger

    def add_handler(self, type, actions, **kwargs):
        """
        Add an event handler to be processed by this session.

        type - The type of the event (pygame.QUIT, pygame.KEYUP ETC).

        actions - The methods which should be called when an event matching this specification is received.
        more than one action can be tied to a single event. This allows for secondary actions to occur along side already existing actions such as the down errow in the List.
        You can either pass the actions or action as a single parameter or as a list.

        kwargs - An arbitrary number of parameters which must be satisfied in order for the event to match.
        The keywords are directly matched with the instance variables found in the current event
        Each value for kwargs can optionally be a lambda which must evaluate to True in order for the match to work.

        Example:

        session.add_handler(pygame.QUIT, session.do_quit)

        session.add_handler(pygame.KEYDOWN, lambda: ao2.speak("You pressed the enter key."), key = pygame.K_RETURN)
        """
        l = self._events.get(type, [])
        h = Handler(self, type, kwargs, actions)
        l.append(h)
        self._events[type] = l
        return h

    def remove_handler(self, handler):
        """
        Remove a handler from the list.

        handler - The handler (as returned by add_handler) to remove.

        Returns True on success, False otherwise.
        """
        try:
            self._events[handler.type].remove(handler)
            return True
        except ValueError:
            return False

    def add_keydown(self, actions, **kwargs):
        """
        Add a pygame.KEYDOWN event handler.

        actions - The methods to be called when this key is pressed.

        kwargs - The kwargs to be passed to self.add_handler.

        See the documentation for self.add_handler for examples.
        """
        return self.add_handler(pygame.KEYDOWN, actions, **kwargs)

    def add_keyup(self, actions, **kwargs):
        """See the documentation for self.add_keydown."""
        return self.add_handler(pygame.KEYUP, actions, **kwargs)

    def change_event_params(self, handler, **kwargs):
        """
        This allows the client to change the parameters for an event, in the case that there is a desire for slightly different behavior, such as reasigning keys.

        handler - the handler object that the desired changes are made to.

        kwargs - the variable number of keyword arguments for the parameters that must match the properties of the corresponding event.
            """
        if not isinstance(handler, Handler):
            raise TypeError("given object must be of type Handler.")
        if not self.remove_handler(handler):
            raise ValueError("You must pass in a valid handler that already exists.")

        self.add_handler(handler.type, handler.actions, **kwargs)
        self.event = handler.event

    def change_event_actions(self, handler, actions):
        """
        This allows the client to change the actions for an event, in the case that there is a desire for slightly different behavior, such as reasigning keys.

        handler - the handler object that the desired changes are made to.

        actions - The methods that are called when this handler is varified against the current event.
            """
        if not isinstance(handler, Handler):
            raise TypeError("given object must be of type Handler.")
        if not self.remove_handler(handler):
            raise ValueError("You must pass in a valid handler that already exists.")

        self.add_handler(handler.type, actions, handler.params)
        self.event = handler.event

    # Override
    def __str__(self):
        "return the events for printing"""
        return self._events.__str__()
