"""Find a *good-looking* Wend grid: three-plus snaking paths that tile 6x6 exactly.

A valid tiling is easy; a fun one is not. Straight-down columns make a trivial puzzle,
so this runs the solver many times with randomised search order and keeps the layout
whose words bend the most.
"""
import random
from collections import deque

W, H = 6, 6
WORDS = ["ANNIVERSARY", "HAPPY", "SAUCE", "CRAB", "BABY", "TIME", "SOY"]
N = W * H
assert sum(len(x) for x in WORDS) == N, sum(len(x) for x in WORDS)

ORTHOGONAL_ONLY = True          # no diagonal steps
STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1)] if ORTHOGONAL_ONLY else [
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]

NB = []
for i in range(N):
    x, y = i % W, i // W
    n = []
    for dx, dy in STEPS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H:
            n.append(ny * W + nx)
    NB.append(n)


def components(free):
    seen, out = set(), []
    for s in free:
        if s in seen:
            continue
        seen.add(s)
        q, size = deque([s]), 0
        while q:
            c = q.popleft()
            size += 1
            for m in NB[c]:
                if m in free and m not in seen:
                    seen.add(m)
                    q.append(m)
        out.append(size)
    return out


def can_pack(sizes, lens):
    sizes, lens = sorted(sizes, reverse=True), sorted(lens, reverse=True)
    if sum(sizes) != sum(lens):
        return False

    def fit(i, remaining):
        if i == len(sizes):
            return not remaining
        target = sizes[i]

        def sub(j, left, used):
            if left == 0:
                return fit(i + 1, [remaining[k] for k in range(len(remaining)) if k not in used])
            if j >= len(remaining):
                return False
            if remaining[j] <= left and sub(j + 1, left - remaining[j], used | {j}):
                return True
            return sub(j + 1, left, used)

        return sub(0, target, set())

    return fit(0, lens)


def solve(rng, budget=[0]):
    grid = [None] * N
    paths = [[] for _ in WORDS]
    budget[0] = 300000

    def lay(wi, ci, cell):
        budget[0] -= 1
        if budget[0] <= 0:
            return False
        word = WORDS[wi]
        grid[cell] = word[ci]
        paths[wi].append(cell)
        if ci + 1 < len(word):
            nbs = NB[cell][:]
            rng.shuffle(nbs)
            for nxt in nbs:
                if grid[nxt] is None and lay(wi, ci + 1, nxt):
                    return True
        else:
            if wi + 1 == len(WORDS):
                return True
            free = {i for i in range(N) if grid[i] is None}
            if can_pack(components(free), [len(x) for x in WORDS[wi + 1:]]):
                starts = sorted(free)
                rng.shuffle(starts)
                for s in starts:
                    if lay(wi + 1, 0, s):
                        return True
        grid[cell] = None
        paths[wi].pop()
        return False

    starts = list(range(N))
    rng.shuffle(starts)
    for s in starts:
        if lay(0, 0, s):
            return grid, paths
    return None


def wiggle(paths):
    """Reward direction changes; punish long straight runs."""
    score = 0
    for p in paths:
        dirs = [((b % W) - (a % W), (b // W) - (a // W)) for a, b in zip(p, p[1:])]
        turns = sum(1 for a, b in zip(dirs, dirs[1:]) if a != b)
        score += turns * 3
        if len(p) >= 4 and turns == 0:
            score -= 25                      # a dead-straight word is a dud
        run = 1
        for a, b in zip(dirs, dirs[1:]):
            run = run + 1 if a == b else 1
            if run >= 4:
                score -= 4
    return score


def placements(grid, word):
    """Every path through `grid` that spells `word`."""
    out = []

    def go(i, cell, used):
        if grid[cell] != word[i]:
            return
        used = used | {cell}
        if i + 1 == len(word):
            out.append(used)
            return
        for m in NB[cell]:
            if m not in used:
                go(i + 1, m, used)

    for s in range(N):
        go(0, s, set())
    return out


def unambiguous(grid):
    """A word with two possible placements lets a player strand the board."""
    for w in WORDS:
        if len(placements(grid, w)) != 1:
            return False
    return True


rng = random.Random(20260817)
best = None
tried = kept = 0
for attempt in range(4000):
    got = solve(rng)
    if not got:
        continue
    tried += 1
    if not unambiguous(got[0]):
        continue
    kept += 1
    s = wiggle(got[1])
    if best is None or s > best[0]:
        best = (s, got[0][:], [list(p) for p in got[1]])

print("solutions %d, unambiguous %d" % (tried, kept))
if best is None:
    raise SystemExit("no unambiguous grid found")

score, grid, paths = best
print("wiggle score", score)
for y in range(H):
    print("   " + "  ".join(grid[y * W + x] for x in range(W)))
print()
for wi, word in enumerate(WORDS):
    print("%-12s %s" % (word, [(c % W, c // W) for c in paths[wi]]))
print()
print("GRID  = " + repr("".join(grid)))
print("PATHS = " + repr({WORDS[i]: paths[i] for i in range(len(WORDS))}))
