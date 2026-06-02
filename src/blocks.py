from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    U_LIST = auto()
    O_LIST = auto()


def block_to_block_type(data:str) -> BlockType:
    lines = data.split("\n")

    if data.startswith("```") and data.endswith("```") and len(data) >= 6:
        return BlockType.CODE

    if data.startswith("#"):
        space_idx = data.find(" ")
        if 1 <= space_idx <= 6 and data[:space_idx] == "#" * space_idx:
            return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.U_LIST

    expected = 1
    is_ordered = True
    for line in lines:
        parts = line.split(". ", 1)
        if len(parts) < 2:
            is_ordered = False
            break
        try:
            num = int(parts[0])
        except ValueError:
            is_ordered = False
            break
        if num != expected:
            is_ordered = False
            break
        expected += 1

    if is_ordered and len(lines) > 0:
        return BlockType.O_LIST

    return BlockType.PARAGRAPH
