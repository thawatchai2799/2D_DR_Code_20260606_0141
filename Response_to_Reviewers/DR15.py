#!/usr/bin/env python3
# DR15.py - enumerator and verifier for recoverable 2D DR Code templates.
# Companion code for "On the Equivalence Classes of Recoverable Patterns in DR Code".
# Pure standard library; runs on Windows, Linux, and macOS.
#
# Data model (Section 3).
#   A payload is split into six data blocks A0,A1,A2 (first half) and
#   B0,B1,B2 (second half).  Three parity blocks are derived index-wise by
#       Ci = Ai XOR Bi,   i = 0,1,2.
#   The three blocks that share an index form a RECOVERY GROUP
#       G0 = {A0,B0,C0},  G1 = {A1,B1,C1},  G2 = {A2,B2,C2},
#   a RAID-5 triple in which any block equals the XOR of the other two.
#
# Definition 1 (Recoverability).
#   A 3x3 placement of the nine blocks is recoverable iff every row and every
#   column contains exactly one block from each recovery group -- equivalently,
#   the three recovery-group indices in each line are pairwise distinct.
#   (It is the index that matters for recovery, NOT the role letter A/B/C.)

from itertools import permutations

# Each block is (role, index): role 0,1,2 = A,B,C ; index 0,1,2.
BLOCKS = [(role, idx) for role in range(3) for idx in range(3)]
ROLE = "ABC"


def name(block):
    role, idx = block
    return f"{ROLE[role]}{idx}"


def group_index(block):
    """Recovery-group index of a block (the subscript). This is what governs recovery."""
    return block[1]


# Grid cell (r, c) holds placement[3 * r + c]. The six lines are the 3 rows + 3 cols.
ROWS = [[3 * r + c for c in range(3)] for r in range(3)]
COLS = [[3 * r + c for r in range(3)] for c in range(3)]
LINES = ROWS + COLS


def is_recoverable(placement):
    """True iff every line carries one block of each recovery group (Definition 1)."""
    for line in LINES:
        if len({group_index(placement[k]) for k in line}) != 3:
            return False
    return True


def enumerate_recoverable():
    """Return the list of all recoverable placements among the 9! arrangements."""
    return [p for p in permutations(BLOCKS) if is_recoverable(p)]


def recover_strip(placement, line):
    """Demonstrate the Recovery Theorem: rebuild a lost row/column by index-wise XOR.

    Returns, for each erased cell, the (block, two surviving group-mates) used.
    Works because a recoverable line holds one block of each group, so every
    group keeps two of its three members -- enough to XOR back the third.
    """
    lost = set(line)
    steps = []
    for k in line:
        idx = group_index(placement[k])
        mates = [placement[j] for j in range(9)
                 if j not in lost and group_index(placement[j]) == idx]
        assert len(mates) == 2, "unrecoverable: group-mate missing"
        steps.append((name(placement[k]), name(mates[0]), name(mates[1])))
    return steps


def show(placement):
    return "\n".join(" ".join(name(placement[3 * r + c]) for c in range(3))
                      for r in range(3))


def main():
    templates = enumerate_recoverable()
    n = len(templates)

    # Headline result (Theorem 1).
    print(f"Recoverable DR Code templates: {n}")

    # Analytical cross-check (Theorem 1 proof): 12 order-3 Latin squares x (3!)^3.
    print(f"Analytical 12 x (3!)^3        : {12 * (6 ** 3)}")
    assert n == 12 * (6 ** 3) == 2592

    # Recovery Theorem demo on the original Sriphum template: A0 B2 C1 / A1 B0 C2 / A2 B1 C0.
    original = ((0, 0), (1, 2), (2, 1),
                (0, 1), (1, 0), (2, 2),
                (0, 2), (1, 1), (2, 0))
    assert is_recoverable(original)
    print("\nOriginal template (Sriphum 2013):")
    print(show(original))
    print("Recovering the lost bottom row {A2, B1, C0} by index-wise XOR:")
    for blk, m1, m2 in recover_strip(original, ROWS[2]):
        print(f"  {blk} = {m1} XOR {m2}")

    # Save the full enumeration (one template per record).
    with open("DR_Code.txt", "w") as f:
        for i, p in enumerate(templates, 1):
            f.write(show(p) + f"\ncount={i}\n")
    print(f"\nWrote {n} templates to DR_Code.txt")


if __name__ == "__main__":
    main()
