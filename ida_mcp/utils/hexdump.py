
import sys


def hexdump(data: str | bytes, address: int = 0) -> str:
  """Generates a formatted hexadecimal dump of the provided data.

  The output includes the offset (starting from the given address), hex
  representation in two columns (8 bytes each), and ASCII representation.

  Args:
    data: The data to dump, either as a string or bytes.
    address: The starting address for the dump offsets. Defaults to 0.

  Returns:
    A string containing the formatted hexdump, or an empty string if data is
    empty or invalid.
  """
  if (
      data is None
      or not isinstance(data, (bytes, str))
      or (insize := len(data)) == 0
  ):
    return ""
  if isinstance(data, str):
    data = data.encode()

  lines = [f"[ {insize} bytes ] -> 16 bytes per line"]
  max_address = address + len(data)
  address_hex_len = 16 if max_address > 0xFFFFFFFF else 8

  offset = 0
  while offset < insize:
    chunk = data[offset : offset + 16]

    # Format the first 8 bytes and pad out to 23 characters
    hex_part1 = " ".join(f"{b:02X}" for b in chunk[:8]).ljust(23)

    # Decide if we need a hyphen separator.
    # Only when more than 8 bytes exist in this row.
    sep = "-" if len(chunk) > 8 else " "

    # Format the remaining bytes (up to 8) and pad out to 23 characters
    hex_part2 = " ".join(f"{b:02X}" for b in chunk[8:]).ljust(23)

    # Build the ASCII representation
    ascii_part = "".join(chr(b) if 0x20 <= b < 0x7F else "." for b in chunk)

    # Assemble the line exactly matching the C formatting spacing
    lines.append(
        f"{address + offset:0{address_hex_len}X}: {hex_part1}{sep}{hex_part2}  "
        f"  {ascii_part}"
    )

    offset += 16
  return "\n".join(lines) + "\n"


if __name__ == "__main__":
  # Quick example test case if run directly
  if len(sys.argv) > 1:
    try:
      with open(sys.argv[1], "rb") as f:
        data = f.read()
    except Exception as e:
      print(f"Error reading file: {e}", file=sys.stderr)
      sys.exit(1)
  else:
    data = bytes([
        0x01,
        0x05,
        0x00,
        0x00,
        0x02,
        0x00,
        0x00,
        0x00,
        0x16,
        0x00,
        0x00,
        0x00,
        0x6F,
        0x74,
        0x6B,
        0x6C,
        0xAA,
        0xBB,
        0xCC,
        0xDD,
    ])

  print(hexdump(data))
  print(hexdump("hello world"))
