
"""Module for registering and managing JSON-RPC methods."""

import re
from typing import Callable
from shared.config import load_config


class RPCRegistry:
  """A registry for JSON-RPC methods."""

  def __init__(self):
    self.methods = set()
    self.unsafe: set[str] = set()
    self._config = None

  def register(self, func: Callable) -> Callable:
    """Registers a function as a JSON-RPC method."""
    if self._config is None:
      try:
        self._config = load_config()
      except Exception:  # pylint: disable=broad-exception-caught
        self._config = {}

    disabled_tools = self._config.get("disabled_tools", [])
    for pattern in disabled_tools:
      try:
        if re.search(pattern, func.__name__, re.IGNORECASE):
          return func
      except Exception:  # pylint: disable=broad-exception-caught
        pass

    self.methods.add(func)
    if getattr(func, "unsafe", False):
      self.unsafe.add(func.__name__)
    return func


rpc_registry = RPCRegistry()
