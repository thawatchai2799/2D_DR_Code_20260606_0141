#!/usr/bin/env python3
"""
verify_2d_group.py
==================================================================
Verification of the symmetry-group structure of the 2D (3x3) DR Code.

Goal: settle the reviewers' point that the closure of the five
generators is NOT the direct product D4 x C3 x C3, but the
semi-direct product  (C3 x C3) ⋊ D4  of the SAME order 72.

Method
------
* The 3x3 grid has 9 cells. Cell (x,y) with x = column in {0,1,2},
  y = row in {0,1,2} is given the linear index  idx = 3*y + x.
* Each geometric / combinatorial operation is realised as a
  permutation of the 9 cell-indices (an element of S9).  Acting on
  cells is equivalent to acting on templates (a template is a
  bijection cells -> blocks), so the group generated inside S9 is
  isomorphic to the group G acting on the 2,592 templates.
* We build the closure by BFS, then test the subgroup lattice:
  normality, intersection, product cover, and (critically) whether
  the two C3 factors are fixed (direct product) or permuted/inverted
  (semi-direct product) by D4.

No third-party libraries; pure standard library.
==================================================================
"""

from itertools import product
from collections import deque

# ---------- permutation helpers (functions on {0,...,8}) ----------

N = 9
ID = tuple(range(N))

def compose(p, q):
    """Return p∘q : first apply q, then p.  (p∘q)(i) = p[q[i]]."""
    return tuple(p[q[i]] for i in range(N))

def inverse(p):
    inv = [0] * N
    for i, pi in enumerate(p):
        inv[pi] = i
    return tuple(inv)

def order(p):
    o, cur = 1, p
    while cur != ID:
        cur = compose(p, cur)
        o += 1
    return o

# ---------- build generators from geometric maps on (x,y) ----------

def cell(x, y):
    return 3 * y + x

def perm_from_map(f):
    """f maps (x,y) -> (x',y'); return the induced permutation of indices."""
    p = [0] * N
    for x, y in product(range(3), range(3)):
        nx, ny = f(x, y)
        p[cell(x, y)] = cell(nx, ny)
    return tuple(p)

# Geometric symmetries of the square grid (D4)
MIRROR = perm_from_map(lambda x, y: (2 - x, y))        # left <-> right
FLIP   = perm_from_map(lambda x, y: (x, 2 - y))        # top  <-> bottom
ROT90  = perm_from_map(lambda x, y: (2 - y, x))        # 90 deg clockwise

# Combinatorial (cyclic) symmetries unique to the recoverability constraint
SHIFT_ROW = perm_from_map(lambda x, y: (x, (y + 1) % 3))   # rows shift down
SHIFT_COL = perm_from_map(lambda x, y: ((x + 1) % 3, y))   # cols shift right

GENS = {
    "Mirror   (σ_M)": MIRROR,
    "Flip     (σ_F)": FLIP,
    "Rot90    (σ_R)": ROT90,
    "ShiftRow (σ_W)": SHIFT_ROW,
    "ShiftCol (σ_C)": SHIFT_COL,
}

# ---------- generic closure (BFS) ----------

def closure(generators):
    gens = list(generators)
    seen = {ID}
    frontier = deque([ID])
    while frontier:
        g = frontier.popleft()
        for s in gens:
            h = compose(s, g)
            if h not in seen:
                seen.add(h)
                frontier.append(h)
    return seen

def is_subgroup_closed(elements):
    s = set(elements)
    for a in s:
        for b in s:
            if compose(a, b) not in s:
                return False
    return True

def is_normal(H, G):
    """Is subgroup H normal in G?  (g h g^-1 in H for all g in G, h in H)"""
    for g in G:
        gi = inverse(g)
        for h in H:
            if compose(compose(g, h), gi) not in H:
                return False
    return True

# ==================================================================
print("=" * 66)
print(" 2D DR Code — symmetry group structure verification")
print("=" * 66)

# sanity: generator orders
print("\n[1] Generator orders")
for name, p in GENS.items():
    print(f"    {name:16s} order = {order(p)}")

# full group
G = closure(GENS.values())
print(f"\n[2] |G| = {len(G)}   (closure of all five generators)")
assert len(G) == 72, "expected |G| = 72"

# D4 subgroup
D4 = closure([MIRROR, FLIP, ROT90])
print(f"[3] |D4| = |<Mirror,Flip,Rot90>| = {len(D4)}")
assert len(D4) == 8
assert is_subgroup_closed(D4)

# N = C3 x C3 subgroup (row & column cyclic shifts)
Ncyc = closure([SHIFT_ROW, SHIFT_COL])
print(f"[4] |N| = |<ShiftRow,ShiftCol>| = {len(Ncyc)}  (should be 9 = C3xC3)")
assert len(Ncyc) == 9
assert is_subgroup_closed(Ncyc)
# confirm N is abelian and ≅ C3 x C3 (every non-id elt has order 3)
assert all(order(g) in (1, 3) for g in Ncyc)
assert all(compose(a, b) == compose(b, a) for a in Ncyc for b in Ncyc)
print("      N is abelian, every non-identity element has order 3  -> C3 x C3")

# ---------- the decisive tests ----------
print("\n[5] Normality")
N_normal  = is_normal(Ncyc, G)
D4_normal = is_normal(D4, G)
print(f"    N  = C3xC3 normal in G ?  {N_normal}")
print(f"    D4         normal in G ?  {D4_normal}")
assert N_normal is True
assert D4_normal is False

print("\n[6] Intersection and product cover")
inter = D4 & Ncyc
print(f"    D4 ∩ N = {{e}} ?  {inter == {ID}}   (|intersection| = {len(inter)})")
prod = {compose(n, d) for n in Ncyc for d in D4}
print(f"    N · D4 = G ?      {prod == G}   (|N·D4| = {len(prod)} = |N|·|D4| = {len(Ncyc)*len(D4)})")
assert inter == {ID}
assert prod == G
assert len(Ncyc) * len(D4) == len(G)

# ---------- direct vs semi-direct: does D4 act trivially on N? ----------
print("\n[7] Does D4 act trivially on N?  (direct product test)")
# Direct product  <=>  every element of D4 commutes with every element of N.
commutes_all = all(compose(d, n) == compose(n, d) for d in D4 for n in Ncyc)
print(f"    [D4, N] = 1 (all commute) ?  {commutes_all}")
assert commutes_all is False, "if this were True the product would be direct"

# the explicit witnessing relation the reviewers point to
lhs = compose(compose(ROT90, SHIFT_ROW), inverse(ROT90))   # R · W · R^-1
print("\n[8] Explicit conjugation witness  Rot90 · ShiftRow · Rot90⁻¹ :")
print(f"    equals ShiftCol      ?  {lhs == SHIFT_COL}")
print(f"    equals ShiftCol⁻¹    ?  {lhs == inverse(SHIFT_COL)}")
print(f"    equals ShiftRow      ?  {lhs == SHIFT_ROW}   (would-be direct-product behaviour)")
# rotation by 90 deg swaps the row-shift and column-shift directions:
assert lhs in (SHIFT_COL, inverse(SHIFT_COL))
assert lhs != SHIFT_ROW

# show the swap-and-invert action of the 90-degree rotation on the C3 generators
print("\n[9] Action of Rot90 (conjugation) on the two C3 generators:")
def name_in_N(p):
    table = {
        SHIFT_ROW: "σ_W  (ShiftRow)",
        inverse(SHIFT_ROW): "σ_W⁻¹",
        SHIFT_COL: "σ_C  (ShiftCol)",
        inverse(SHIFT_COL): "σ_C⁻¹",
        ID: "e",
    }
    return table.get(p, "other elt of N")
for gen, nm in ((SHIFT_ROW, "σ_W"), (SHIFT_COL, "σ_C")):
    conj = compose(compose(ROT90, gen), inverse(ROT90))
    print(f"    Rot90 · {nm} · Rot90⁻¹  =  {name_in_N(conj)}")

print("\n" + "=" * 66)
print(" CONCLUSION")
print("=" * 66)
print("""    |G| = 72,  N = C3xC3 is normal,  D4 is NOT normal,
    D4 ∩ N = {e},  N · D4 = G,  and D4 does NOT centralise N
    (Rot90 conjugates ShiftRow to ShiftCol). Therefore

        G  ≅  (C3 x C3) ⋊ D4        [semi-direct product]
           ≇  D4 x C3 x C3          [the direct product is REFUTED]

    Both groups have order 72, so all orbit counts (36 under G,
    324 under D4) are unaffected; only the structural claim changes.""")
print("=" * 66)


# ==================================================================
# Appendix: the structure homomorphism  φ : D4 -> Aut(C3 x C3)
# Write N additively as (Z/3)^2 with basis  a = σ_W (row shift),
# b = σ_C (col shift).  For each D4 generator g we record the matrix
# (over F3) of  x ↦ g x g^-1  in the (a,b) basis, and confirm the
# map is an injective homomorphism (faithful action), so D4 embeds
# in GL(2,3) and the semi-direct product is non-trivial.
# ==================================================================
print("\n[10] Structure map  φ: D4 -> Aut(C3xC3) = GL(2,F3),  basis (a=σ_W, b=σ_C)")

a, b = SHIFT_ROW, SHIFT_COL
# express any element of N as a vector (i,j) meaning a^i b^j
vec_of = {}
for i in range(3):
    for j in range(3):
        el = ID
        for _ in range(i): el = compose(a, el)
        for _ in range(j): el = compose(b, el)
        vec_of[el] = (i, j)

def phi_matrix(g):
    gi = inverse(g)
    col_a = vec_of[compose(compose(g, a), gi)]   # image of a
    col_b = vec_of[compose(compose(g, b), gi)]   # image of b
    # matrix columns = images of basis vectors
    return (col_a[0], col_b[0], col_a[1], col_b[1])  # (m00,m01,m10,m11)

for name, g in (("Mirror σ_M", MIRROR), ("Flip σ_F", FLIP), ("Rot90 σ_R", ROT90)):
    m00, m01, m10, m11 = phi_matrix(g)
    print(f"    φ({name:10s}) = [[{m00} {m01}] [{m10} {m11}]]  (mod 3)")

# faithfulness: only identity of D4 maps to the identity matrix
ker = [g for g in D4 if phi_matrix(g) == (1, 0, 0, 1)]
print(f"\n    |ker φ| = {len(ker)}  -> {'faithful (trivial kernel)' if ker==[ID] else 'NOT faithful'}")
assert ker == [ID]
print("    D4 embeds in Aut(C3xC3); the semi-direct product is non-trivial.")
