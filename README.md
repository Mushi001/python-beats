# python-beats

A Python animation of the **acoustic beat phenomenon**: two travelling sound waves of slightly different frequencies add up, and you can see the amplitude envelope and what a listener actually hears.

Built with NumPy and Matplotlib. It is meant as a teaching aid for waves and superposition.

---

## What are beats?

When two waves of equal amplitude `A` and close frequencies `f1` and `f2` are superposed, the result is a fast oscillation whose amplitude swells and fades slowly. A listener hears this as a periodic rise and fall in loudness.

With `Y1 = A sin(2π f1 t)` and `Y2 = A sin(2π f2 t)`, the sum is:

```
Y = Y1 + Y2 = 2A cos(π (f1 − f2) t) · sin(π (f1 + f2) t)
              └──────── envelope ────┘   └──── carrier ────┘
```

- The **carrier** oscillates at the average frequency `(f1 + f2) / 2`.
- The **envelope** `2A cos(π (f1 − f2) t)` varies slowly.
- The **beat frequency** is `f_beat = |f1 − f2|`, because loudness peaks twice per envelope cycle.

Example: 400 Hz and 410 Hz give a beat frequency of 10 Hz, so the sound gets loud 10 times per second.

In the simulation the waves also travel in space at speed `V = 340 m/s`, so each wave is `A sin(2π f (t − x/V))`.

---

## What the animation shows

The window contains four stacked plots, updated live:

| Plot | Content |
|------|---------|
| 1 | Wave **Y1** (frequency `f1`) travelling in space |
| 2 | Wave **Y2** (frequency `f2`) travelling in space |
| 3 | The sum **Y = Y1 + Y2** in green, with the **envelope** as red dashed lines and a black dot marking the listener at `x = 0` |
| 4 | **What a listener at x = 0 hears**: displacement against time over the last two beat periods, with the envelope as red dashed lines |

The figure title shows `f1`, `f2`, the beat frequency and the elapsed time. The animation runs in slow motion so you can follow the individual oscillations.

---

## Requirements

- Python 3.8 or newer
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

---

## Installation

```bash
git clone https://github.com/Mushi001/python-beats.git
cd python-beats
pip install numpy matplotlib
```

---

## Usage

```bash
python beats.py
```

You will be prompted for three values. Press Enter to accept the default shown.

```
Amplitude A (e.g. 5): 5
Frequency f1 in Hz (e.g. 400): 400
Frequency f2 in Hz (e.g. 410): 410
```

| Prompt | Meaning | Default |
|--------|---------|---------|
| `A` | Amplitude of each wave | 5 |
| `f1` | Frequency of the first wave (Hz) | 400 |
| `f2` | Frequency of the second wave (Hz) | 410 |

Things to try:

- **Close frequencies** (e.g. 400 and 402): slow beats, long envelope.
- **Wider gap** (e.g. 400 and 440): fast beats, the envelope packs together.
- **Equal frequencies** (e.g. 400 and 400): no beats, the waves add constructively into a steady wave of amplitude `2A`. The view then spans 10 wavelengths and 10 carrier periods instead.

### Use it from your own code

```python
from beats import simulate_beats

anim = simulate_beats(A=5, f1=400, f2=410, slow=0.1, interval=30)
```

| Parameter | Meaning | Default |
|-----------|---------|---------|
| `A` | Amplitude of each wave | required |
| `f1`, `f2` | Frequencies in Hz | required |
| `slow` | Simulated time per frame, in carrier periods (smaller is slower) | `0.1` |
| `interval` | Delay between frames in ms | `30` |

Keep a reference to the returned `anim` object, or Matplotlib may garbage-collect the animation.

---

## How it works

- **Time step:** each frame advances time by `dt = slow / f_avg`, so the motion looks the same at any carrier frequency.
- **Space axis:** spans two beat wavelengths, `L = 2V / f_beat`, so two full envelope cycles are visible.
- **Listener window:** the bottom plot shows the last two beat periods, `2 / f_beat`.
- **Envelope:** drawn analytically as `±2A cos(π (f1 − f2)(t − x/V))`, not computed from the signal.
- **Animation:** `matplotlib.animation.FuncAnimation` updates the line data every frame without redrawing the axes.

---

## Project structure

```
python-beats/
├── beats.py     # the simulation
└── README.md
```

---

## Notes

- The wave speed `V = 340 m/s` (sound in air) is a constant at the top of `beats.py`; change it to model another medium.
- The simulation is purely visual. It does not play any sound.
