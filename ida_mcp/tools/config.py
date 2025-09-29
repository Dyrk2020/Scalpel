

"""Configuration and management for IDA Pro MCP tools."""

from typing import Any, Dict, List
from ida_mcp.core.decorators import internal, jsonrpc
from ida_mcp.core.rpc_registry import rpc_registry
from ida_mcp.core.security import security_manager


@internal
@jsonrpc
def list_unsafe_tools() -> List[str]:
  """Returns a list of all unsafe tool names."""
  return sorted(list(rpc_registry.unsafe))


@internal
@jsonrpc
def configure_unsafe_tools(
    enable_all_unsafe_tools: bool,
    persistent: bool,
    enabled_unsafe_tools: List[str],
) -> str:
  """Configures which unsafe tools are allowed to run.

  Args:
      enable_all_unsafe_tools: If True, all unsafe tools are allowed.
      persistent: If True, saves the configuration to the IDA database.
      enabled_unsafe_tools: A list of unsafe tool names to allow if enable_all
        is False.
  """
  security_manager.update(enable_all_unsafe_tools, enabled_unsafe_tools)

  if persistent:
    security_manager.save_to_netnode()
    return "Security settings updated and saved to database."

  return "Security settings updated (session only)."


@internal
@jsonrpc
def get_security_config() -> Dict[str, Any]:
  """Returns the current security configuration."""
  return {
      "enable_all_unsafe_tools": security_manager.enable_all_unsafe_tools,
      "enabled_unsafe_tools": list(security_manager.enabled_unsafe_tools),
  }
