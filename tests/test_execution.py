
"""Unit tests for the execution module."""

import sys
import unittest
from unittest import mock

# Mock IDA modules before importing the module under test
MOCKED_MODULES = [
    "ida_bytes",
    "ida_dbg",
    "ida_idp",
    "ida_entry",
    "ida_frame",
    "ida_funcs",
    "ida_hexrays",
    "ida_ida",
    "ida_kernwin",
    "ida_lines",
    "ida_nalt",
    "ida_name",
    "ida_segment",
    "ida_typeinf",
    "ida_xref",
    "idaapi",
    "idautils",
    "idc",
]

module_mocks = {}
for module in MOCKED_MODULES:
  if module in sys.modules:
    module_mocks[module] = sys.modules[module]
  else:
    module_mocks[module] = mock.MagicMock()
sys.modules.update(module_mocks)

# Import the module under test
# Note: This import must happen AFTER the mocking above
# pylint: disable=g-import-not-at-top
from ida_mcp.tools.execution import idapython_eval as _idapython_eval

# pylint: enable=g-import-not-at-top

idapython_eval = getattr(_idapython_eval, "sync_call", _idapython_eval)


class TestPyEval(unittest.TestCase):
  """Tests for the idapython_eval function."""

  def test_simple_expression(self):
    """Test evaluating a simple mathematical expression."""
    result = idapython_eval("1 + 1")
    self.assertEqual(result["result"], "2")
    self.assertEqual(result["stderr"], "")

  def test_variable_assignment_and_persistence(self):
    """Test that variables defined in one call are available in the next."""
    idapython_eval("x_var = 42")
    result = idapython_eval("x_var")
    self.assertEqual(result["result"], "42")

  def test_stdout_capture(self):
    """Test capturing standard output."""
    result = idapython_eval("print('Hello, World!')")
    self.assertEqual(result["stdout"].strip(), "Hello, World!")

  def test_syntax_error(self):
    """Test handling of syntax errors."""
    result = idapython_eval("if True")  # Missing colon
    # The exact error message depends on python version, but it should be in
    # stderr
    self.assertIn("SyntaxError", result["stderr"])
    self.assertEqual(result["result"], "")

  def test_runtime_error(self):
    """Test handling of runtime errors."""
    result = idapython_eval("1 / 0")
    self.assertIn("ZeroDivisionError", result["stderr"])

  def test_function_definition(self):
    """Test defining and calling a function."""
    code = """
def add_func(a, b):
    return a + b
"""
    idapython_eval(code)
    result = idapython_eval("add_func(10, 20)")
    self.assertEqual(result["result"], "30")

  def test_ida_api_call(self):
    """Test interacting with mocked IDA API."""
    # Configure the mock return value
    sys.modules["idc"].get_screen_ea.return_value = 0x1234

    result = idapython_eval("idc.get_screen_ea()")
    self.assertEqual(result["result"], str(0x1234))

  def test_multi_statement_with_expression(self):
    """Test a block with statements ending in an expression."""
    code = """
a = 5
b = 6
a * b
"""
    result = idapython_eval(code)
    self.assertEqual(result["result"], "30")

  def test_complex_logic_persistence(self):
    """Test complex logic spanning multiple calls."""
    idapython_eval("my_list = []")
    idapython_eval("for i in range(3): my_list.append(i)")
    result = idapython_eval("my_list")
    self.assertEqual(result["result"], "[0, 1, 2]")


if __name__ == "__main__":
  unittest.main()
