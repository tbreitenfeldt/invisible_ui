"""Handler class."""

from inspect import getdoc

class Handler(object):
 """Event handler."""
 def __init__(self, session, type, params, func, docstring = None, always_active = False):
  """
  Create a new event handler.
  
  session - The session to which this handler is attached.
  
  type - The type of this handler.
  
  params - A dictionary containing parameters the calling event must conform to in order to succeed.
  
  func - The function which should be called when this handler has been verified.
  
  docstring - The docstring for func. If docstring is not specified, inspect.getdoc(func) will be used.
  
  always_active - If True, this handler will be called even when the game is paused.
  
  To call the provided function properly, use Handler.call_func(*args, **kwargs).
  """
  self.session = session
  self.type = type
  self.params = params
  self.func = func
  self.docstring = docstring
  self.always_active = always_active
 
 def get_help(self):
  """Return help for self.func."""
  if self.docstring:
   return self.docstring
  else:
   return getdoc(self.func)
 
 def call_func(self, *args, **kwargs):
  """Call self.func."""
  if self.session.running or self.always_active:
   return self.func(self, *args, **kwargs)
