import tkinter as tk
from tkinter import ttk

# --- Your formulas from the images ---


def quantum_correction(alpha=1/137, HQS=0.235, x=16.45):
    return (alpha / HQS) ** (1 / x)


def bridge_radius(a0_prime, n, LZ=1.23498228, alpha=1/137, HQS=0.235, x=16.45):
    qc = quantum_correction(alpha, HQS, x)
    scaling = LZ ** (n / 3.14159)
    return a0_prime * scaling * qc


def bridge_mass(m0_prime, n, LZ=1.23498228, alpha=1/137, HQS=0.235, x=16.45):
    qc = quantum_correction(alpha, HQS, x)
    scaling = LZ ** (-n / 3.14159)
    return m0_prime * scaling * qc


def error_percent(calculated, known):
    return 100 * abs(calculated - known) / known


# Known values for demonstration
known_particles = {
    "Electron": {"n": 768.5, "mass": 9.10938356e-31, "radius": None},
    "Proton":   {"n": 220,   "mass": 1.67262192369e-27, "radius": None},
    "Muon":     {"n": 45,    "mass": 1.883531627e-28, "radius": None},
}


class BridgeTabsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bridge Formula GUI with Tabs")
        self.geometry("600x400")
        self.create_tabs()

    def create_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill='both')

        # --- Tab 1: Bridge Orbit ---
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text='Bridge Orbits')
        self.setup_bridge_tab(tab1)

        # --- Tab 2: Mass Formula ---
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text='Mass')
        self.setup_mass_tab(tab2)

        # --- Tab 3: Error ---
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text='Error')
        self.setup_error_tab(tab3)

        # --- Tab 4: Approximation ---
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text='Approximation')
        self.setup_approx_tab(tab4)

    def setup_bridge_tab(self, frame):
        ttk.Label(frame, text="Reference Length a₀′ (meters):").pack()
        self.a0_var = tk.DoubleVar(value=1.616e-35)
        ttk.Entry(frame, textvariable=self.a0_var).pack()

        ttk.Label(frame, text="Collatz Octave n:").pack()
        self.n_var = tk.DoubleVar(value=0)
        ttk.Entry(frame, textvariable=self.n_var).pack()

        ttk.Button(frame, text="Calculate Bridge Orbit",
                   command=self.calc_bridge).pack(pady=10)
        self.bridge_result = tk.Label(frame, text="", font=("Consolas", 11))
        self.bridge_result.pack(pady=10)

    def calc_bridge(self):
        a0 = self.a0_var.get()
        n = self.n_var.get()
        radius = bridge_radius(a0, n)
        qc = quantum_correction()
        self.bridge_result.config(
            text=f"Quantum Correction: {qc:.6f}\nRadius: {radius:.3e} m"
        )

    def setup_mass_tab(self, frame):
        ttk.Label(frame, text="Reference Mass m₀′ (kg):").pack()
        self.m0_var = tk.DoubleVar(value=2.176e-8)
        ttk.Entry(frame, textvariable=self.m0_var).pack()

        ttk.Label(frame, text="Collatz Octave n:").pack()
        self.n_mass_var = tk.DoubleVar(value=0)
        ttk.Entry(frame, textvariable=self.n_mass_var).pack()

        ttk.Button(frame, text="Calculate Mass",
                   command=self.calc_mass).pack(pady=10)
        self.mass_result = tk.Label(frame, text="", font=("Consolas", 11))
        self.mass_result.pack(pady=10)

    def calc_mass(self):
        m0 = self.m0_var.get()
        n = self.n_mass_var.get()
        mass = bridge_mass(m0, n)
        qc = quantum_correction()
        self.mass_result.config(
            text=f"Quantum Correction: {qc:.6f}\nMass: {mass:.3e} kg"
        )

    def setup_error_tab(self, frame):
        ttk.Label(frame, text="Calculated Value:").pack()
        self.calc_val_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.calc_val_var).pack()

        ttk.Label(frame, text="Known Value:").pack()
        self.known_val_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.known_val_var).pack()

        ttk.Button(frame, text="Calculate Error",
                   command=self.calc_error).pack(pady=10)
        self.error_result = tk.Label(frame, text="", font=("Consolas", 11))
        self.error_result.pack(pady=10)

    def calc_error(self):
        calc = self.calc_val_var.get()
        known = self.known_val_var.get()
        if known == 0:
            self.error_result.config(text="Known value must not be zero.")
            return
        err = error_percent(calc, known)
        if err < 1:
            msg = f"Error: {err:.3f}%\nStable particle found (matches known value)"
        else:
            msg = f"Error: {err:.3f}%\nUnknown particle"
        self.error_result.config(text=msg)

    def setup_approx_tab(self, frame):
        ttk.Label(frame, text="Select Known Particle:").pack()
        self.particle_var = tk.StringVar()
        particle_names = [""] + list(known_particles.keys())
        self.particle_menu = ttk.Combobox(
            frame, textvariable=self.particle_var, values=particle_names)
        self.particle_menu.pack()

        ttk.Button(frame, text="Approximate",
                   command=self.calc_approx).pack(pady=10)
        self.approx_result = tk.Label(frame, text="", font=("Consolas", 11))
        self.approx_result.pack(pady=10)

    def calc_approx(self):
        name = self.particle_var.get()
        if name in known_particles:
            d = known_particles[name]
            n = d["n"]
            mass = d["mass"]
            m0 = 2.176e-8  # Planck mass
            calc_mass_val = bridge_mass(m0, n)
            err = error_percent(calc_mass_val, mass)
            if err < 1:
                msg = f"{name}\nn={n}\nMass: {calc_mass_val:.3e} kg\nError: {err:.3f}%\nStable particle found"
            else:
                msg = f"{name}\nn={n}\nMass: {calc_mass_val:.3e} kg\nError: {err:.3f}%\nUnknown particle"
            self.approx_result.config(text=msg)
        else:
            self.approx_result.config(text="Select a known particle.")


if __name__ == "__main__":
    app = BridgeTabsGUI()
    app.mainloop()
