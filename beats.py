import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

V = 340.0  # wave speed (m/s), used to show the waves travelling in space


def simulate_beats(A, f1, f2, slow=0.1, interval=30):
    """Animate the beat phenomenon for two travelling waves of amplitude A.

    slow     : simulated time per frame, in carrier periods (smaller = slower)
    interval : delay between frames in ms
    """
    f_beat = abs(f1 - f2)
    f_avg = (f1 + f2) / 2
    dt = slow / f_avg                              # time step per frame

    # Space axis: two beat wavelengths (or 10 wavelengths if f1 == f2)
    L = 2 * V / f_beat if f_beat else 10 * V / f_avg
    x = np.linspace(0, L, 6000)
    # Listener's time window: two beat periods (or 10 carrier periods)
    window = 2 / f_beat if f_beat else 10 / f_avg
    tau = np.linspace(-window, 0, 4000)            # time relative to "now"

    def wave(f, xx, t):
        return A * np.sin(2 * np.pi * f * (t - xx / V))

    def env(xx, t):
        return 2 * A * np.cos(np.pi * (f1 - f2) * (t - xx / V))

    fig, ax = plt.subplots(4, 1, figsize=(10, 9))
    ymax = 1.15 * A
    titles = [f"Y1 = A sin(2π·{f1:g}·t)   (travelling wave)",
              f"Y2 = A sin(2π·{f2:g}·t)   (travelling wave)",
              "Y = Y1 + Y2   (dashed = envelope)",
              "What a listener at x = 0 hears (displacement vs time)"]
    for a, title in zip(ax, titles):
        a.set_title(title, fontsize=10)
        a.grid(True)
        a.set_ylabel("Amplitude")
    for a in ax[:3]:
        a.set_xlim(0, L)
        a.set_ylim(-2.3 * A if a is ax[2] else -ymax,
                   2.3 * A if a is ax[2] else ymax)
    ax[2].set_xlabel("Position x (m)")
    ax[3].set_xlim(-window, 0)
    ax[3].set_ylim(-2.3 * A, 2.3 * A)
    ax[3].set_xlabel("Time relative to now (s)")

    l1, = ax[0].plot(x, wave(f1, x, 0), color="tab:blue")
    l2, = ax[1].plot(x, wave(f2, x, 0), color="tab:orange")
    ls, = ax[2].plot(x, wave(f1, x, 0) + wave(f2, x, 0), color="g")
    le1, = ax[2].plot(x, env(x, 0), "r--", lw=1)
    le2, = ax[2].plot(x, -env(x, 0), "r--", lw=1)
    dot, = ax[2].plot([0], [0], "ko")              # the listener
    lt, = ax[3].plot(tau, np.zeros_like(tau), color="purple")
    lte, = ax[3].plot(tau, np.zeros_like(tau), "r--", lw=1)
    lte2, = ax[3].plot(tau, np.zeros_like(tau), "r--", lw=1)
    clock = fig.suptitle("", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    def update(frame):
        t = frame * dt
        y1 = wave(f1, x, t)
        y2 = wave(f2, x, t)
        l1.set_ydata(y1)
        l2.set_ydata(y2)
        ls.set_ydata(y1 + y2)
        e = env(x, t)
        le1.set_ydata(e)
        le2.set_ydata(-e)
        dot.set_data([0], [wave(f1, 0, t) + wave(f2, 0, t)])
        ts = t + tau
        lt.set_ydata(wave(f1, 0, ts) + wave(f2, 0, ts))
        et = env(0, ts)
        lte.set_ydata(et)
        lte2.set_ydata(-et)
        clock.set_text(f"Beats: f1={f1:g} Hz, f2={f2:g} Hz  |  "
                       f"beat frequency = {f_beat:g} Hz  |  t = {t * 1000:.1f} ms "
                       f"(slow motion)")
        return l1, l2, ls, le1, le2, dot, lt, lte, lte2, clock

    anim = FuncAnimation(fig, update, frames=None, interval=interval,
                         blit=False, cache_frame_data=False)
    plt.show()
    return anim


if __name__ == "__main__":
    A = float(input("Amplitude A (e.g. 5): ") or 5)
    f1 = float(input("Frequency f1 in Hz (e.g. 400): ") or 400)
    f2 = float(input("Frequency f2 in Hz (e.g. 410): ") or 410)
    simulate_beats(A, f1, f2)
