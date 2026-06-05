"""
DR Code Generator (3x3 Block Arrangement) - Version 15
Original C++ program by Thawatchai Chomsiri and Wiwat Sriphum
Converted to Python and refactored for readability.

Version: 15
File: DR15.py

This program searches for arrangements of characters in a 3x3 grid
such that no row or column contains repeated characters from the same "row" group.
- Row 0: 'A', '1', 'A'^'1'
- Row 1: 'M', '5', 'M'^'5'
- Row 2: 'Z', '9', 'Z'^'9'
"""

from itertools import permutations

# ===== Constants =====
OUTPUT_FILE = "DR_Code.txt"
GRID_SIZE = 9  # 3x3 = 9 cells

# Base characters
CHAR_A, CHAR_M, CHAR_Z = ord('A'), ord('M'), ord('Z')
CHAR_1, CHAR_5, CHAR_9 = ord('1'), ord('5'), ord('9')

# XOR characters (recovery values)
CHAR_A_XOR_1 = CHAR_A ^ CHAR_1
CHAR_M_XOR_5 = CHAR_M ^ CHAR_5
CHAR_Z_XOR_9 = CHAR_Z ^ CHAR_9

# Mapping: character -> code to write to file
CHAR_TO_CODE = {
    CHAR_A:       "A0",
    CHAR_M:       "A1",
    CHAR_Z:       "A2",
    CHAR_1:       "B0",
    CHAR_5:       "B1",
    CHAR_9:       "B2",
    CHAR_A_XOR_1: "C0",
    CHAR_M_XOR_5: "C1",
    CHAR_Z_XOR_9: "C2",
}

# Mapping: character -> row number (0, 1, 2)
CHAR_TO_ROW = {
    CHAR_A:       0, CHAR_1: 0, CHAR_A_XOR_1: 0,
    CHAR_M:       1, CHAR_5: 1, CHAR_M_XOR_5: 1,
    CHAR_Z:       2, CHAR_9: 2, CHAR_Z_XOR_9: 2,
}

# Initial values of cube/line, following the original source code
LINE_ORG = [
    CHAR_A, CHAR_M, CHAR_Z,         # cube[0][0..2]
    CHAR_1, CHAR_5, CHAR_9,         # cube[1][0..2]
    CHAR_A_XOR_1, CHAR_M_XOR_5, CHAR_Z_XOR_9,  # cube[2][0..2]
]

# Indices of each row and column in line[0..8]
# line is interpreted such that: line[i] is at position (col=i//3, row=i%3)
# following the original source code
ROWS_AND_COLS = [
    (0, 3, 6),  # row 1
    (1, 4, 7),  # row 2
    (2, 5, 8),  # row 3
    (0, 1, 2),  # col 1
    (3, 4, 5),  # col 2
    (6, 7, 8),  # col 3
]


# ===== Helper Functions =====
def write_char_code(file_handle, ch):
    """Write the character's code to the file (e.g., 'A' -> 'A0 ')"""
    code = CHAR_TO_CODE.get(ch)
    if code is not None:
        file_handle.write(code + " ")


def three_chars_not_repeat(c1, c2, c3):
    """
    Check whether the 3 characters come from 3 different rows (groups).
    Returns True if all 3 characters are in different rows, False otherwise.
    """
    rows = (CHAR_TO_ROW[c1], CHAR_TO_ROW[c2], CHAR_TO_ROW[c3])
    return len(set(rows)) == 3


def is_valid_arrangement(line):
    """Check every row and column to ensure no character groups are repeated."""
    for i1, i2, i3 in ROWS_AND_COLS:
        if not three_chars_not_repeat(line[i1], line[i2], line[i3]):
            return False
    return True


def write_arrangement(file_handle, line, r, count, count_not_repeat):
    """Write one valid arrangement to the file."""
    # Rows 1, 2, 3 (following the original format)
    for row_indices in [(0, 3, 6), (1, 4, 7), (2, 5, 8)]:
        for idx in row_indices:
            write_char_code(file_handle, line[idx])
        file_handle.write("\n")

    # Summary line with r values and counts
    r_str = ",".join(f"r{i}={r[i]}" for i in range(GRID_SIZE))
    file_handle.write(f"{r_str}, count={count}, count_nr={count_not_repeat} \n")


# ===== Main =====
def main():
    count = 1
    count_not_repeat = 1

    with open(OUTPUT_FILE, "w") as p_file:
        # Iterate over every permutation of indices 0..8 (9! = 362,880 arrangements in total)
        for r in permutations(range(GRID_SIZE)):
            # Build the line according to the permutation order
            line = [LINE_ORG[r[i]] for i in range(GRID_SIZE)]

            if is_valid_arrangement(line):
                write_arrangement(p_file, line, r, count, count_not_repeat)
                count += 1

            count_not_repeat += 1

    print("## OK ## -- Done! (DR15)")
    print(f"Total valid arrangements (count)              = {count - 1}")
    print(f"Total permutations checked (count_not_repeat) = {count_not_repeat - 1}")


if __name__ == "__main__":
    main()
