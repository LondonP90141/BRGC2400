# Binary Reflected Gray Code Visualization
# I generated the Gray code logic myself.
# Animation setup (matplotlib FuncAnimation) was assisted by OpenAI ChatGPT — cited for transparency.

import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import animation

rc("animation", html="jshtml")

# Gray code generation (my part)
def gray_code(n):
    if n == 0:
        return ["0"]
    if n == 1:
        return ["0", "1"]

    prev = gray_code(n - 1)
    result = []

    for code in prev:
        result.append("0" + code)

    for code in reversed(prev):
        result.append("1" + code)

    return result

n_bits = 4
codes = gray_code(n_bits)

num_codes = len(codes)
bit_matrix = [[int(b) for b in code] for code in codes]

# Animation setup (GenAI-assisted part)
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title(f"{n_bits}-bit Binary Reflected Gray Code", pad=10)
ax.set_xlabel("Bit Position")
ax.set_ylabel("Code Index")
ax.set_xticks(range(n_bits))
ax.set_xticklabels([f"b{n_bits-1-i}" for i in range(n_bits)])
ax.set_yticks(range(num_codes))
ax.set_yticklabels(range(num_codes))

ax.set_xlim(-0.5, n_bits - 0.5)
ax.set_ylim(-0.5, num_codes - 0.5)
ax.invert_yaxis()

cells = []
for y in range(num_codes):
    row_cells = []
    for x in range(n_bits):
        rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1,
                             edgecolor="black",
                             facecolor="white")
        ax.add_patch(rect)
        row_cells.append(rect)
    cells.append(row_cells)

texts = []
for y in range(num_codes):
    row_texts = []
    for x in range(n_bits):
        t = ax.text(x, y, "", ha="center", va="center", fontsize=12)
        row_texts.append(t)
    texts.append(row_texts)

status_text = ax.text(0.02, 1.02, "",
                      transform=ax.transAxes,
                      fontsize=10)

def changed_bit_index(prev_code, curr_code):
    if prev_code is None:
        return None
    for i, (p, c) in enumerate(zip(prev_code, curr_code)):
        if p != c:
            return i
    return None

def init():
    for y in range(num_codes):
        for x in range(n_bits):
            cells[y][x].set_facecolor("white")
            texts[y][x].set_text("")
    status_text.set_text("")
    return [c for row in cells for c in row] + [t for row in texts for t in row] + [status_text]

def update(frame):
    for y in range(num_codes):
        for x in range(n_bits):
            if y < frame:
                cells[y][x].set_facecolor("lightgray")
            else:
                cells[y][x].set_facecolor("white")

            if y <= frame:
                texts[y][x].set_text(bit_matrix[y][x])
            else:
                texts[y][x].set_text("")

    for x in range(n_bits):
        cells[frame][x].set_facecolor("aliceblue")

    prev_code = codes[frame - 1] if frame > 0 else None
    curr_code = codes[frame]
    idx_changed = changed_bit_index(prev_code, curr_code)

    if idx_changed is not None:
        cells[frame][idx_changed].set_facecolor("lightcoral")
        status_text.set_text(
            f"Step {frame}: {curr_code} (bit {idx_changed} flipped)"
        )
    else:
        status_text.set_text(
            f"Step {frame}: {curr_code} (starting code)"
        )

    return [c for row in cells for c in row] + [t for row in texts for t in row] + [status_text]

anim = animation.FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=num_codes,
    interval=800,
    blit=True,
    repeat=False
)

plt.show()