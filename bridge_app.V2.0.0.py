import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
from fpdf import FPDF
import matplotlib.pyplot as plt

# --- Physics Formulas ---


def quantum_correction(alpha=0.0072973525643, HQS=0.235, x=16.450911914534554):
    return (alpha / HQS) ** (1 / x)


def bridge_radius(a0_prime, n, LZ=1.23498228, alpha=0.0072973525643, HQS=0.235, x=16.450911914534554):
    qc = quantum_correction(alpha, HQS, x)
    scaling = LZ ** (n / 3.141592653589793)
    return a0_prime * scaling * qc


def bridge_mass(m0_prime, n, LZ=1.23498228, alpha=0.0072973525643, HQS=0.235, x=16.450911914534554):
    qc = quantum_correction(alpha, HQS, x)
    scaling = LZ ** (-n / 3.141592653589793)
    return m0_prime * scaling * qc


def solve_n_from_m(m, m0_prime, LZ=1.23498228, alpha=0.0072973525643, HQS=0.235, x=16.450911914534554):
    qc = quantum_correction(alpha, HQS, x)
    n = -math.pi * math.log(m / (m0_prime * qc)) / math.log(LZ)
    return n


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
        self.geometry("700x600")
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

        # --- Tab 5: Log/Export ---
        tab5 = ttk.Frame(notebook)
        notebook.add(tab5, text='Log & Export')
        self.setup_log_tab(tab5)

    def setup_bridge_tab(self, frame):
        ttk.Label(frame, text="Reference Length a (meters):").pack()
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
        self.append_output(
            f"Bridge Orbit: a0={a0}, n={n}, Radius={radius:.3e} m, QC={qc:.6f}")

    def setup_mass_tab(self, frame):
        ttk.Label(frame, text="Reference Mass m (kg):").pack()
        self.m0_var = tk.DoubleVar(value=2.176e-8)
        ttk.Entry(frame, textvariable=self.m0_var).pack()

        ttk.Label(frame, text="Collatz Octave n:").pack()
        self.n_mass_var = tk.DoubleVar(value=0)
        ttk.Entry(frame, textvariable=self.n_mass_var).pack()

        ttk.Button(frame, text="Calculate Mass",
                   command=self.calc_mass).pack(pady=10)
        self.mass_result = tk.Label(frame, text="", font=("Consolas", 11))
        self.mass_result.pack(pady=10)

        # Input for mass to find n
        ttk.Label(frame, text="Mass to find n (kg):").pack()
        self.find_n_mass_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.find_n_mass_var).pack()

        ttk.Button(frame, text="Find n from m",
                   command=self.calc_n_from_m).pack(pady=10)
        self.find_n_result = tk.Label(frame, text="", font=("Consolas", 11))
        self.find_n_result.pack(pady=10)

    def calc_mass(self):
        m0 = self.m0_var.get()
        n = self.n_mass_var.get()
        mass = bridge_mass(m0, n)
        qc = quantum_correction()
        self.mass_result.config(
            text=f"Quantum Correction: {qc:.6f}\nMass: {mass:.3e} kg"
        )
        self.append_output(
            f"Mass Calculation: n={n}, m0={m0}, Mass={mass:.3e} kg, QC={qc:.6f}")

    def calc_n_from_m(self):
        m = self.find_n_mass_var.get()
        m0 = self.m0_var.get()
        try:
            n = solve_n_from_m(m, m0)
            self.find_n_result.config(text=f"n = {n:.3f}")
            self.append_output(f"Find n from m: m={m}, m0={m0}, n={n:.3f}")
        except Exception as e:
            self.find_n_result.config(text=f"Error: {str(e)}")
            self.append_output(f"Error finding n: {str(e)}")

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
        self.append_output(
            f"Error Calculation: calc={calc}, known={known}, error={err:.3f}%")

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
            self.append_output(f"Approximation: {msg.replace('\n', ', ')}")
        else:
            self.approx_result.config(text="Select a known particle.")

    def setup_log_tab(self, frame):
        # Output log
        self.output_text = tk.Text(
            frame, height=15, font=("Consolas", 12), wrap=tk.WORD)
        scroll = ttk.Scrollbar(frame, orient="vertical",
                               command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Export buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Export as Text", command=self.export_text,
                  font=("Consolas", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Export as PDF", command=self.export_pdf,
                  font=("Consolas", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Export as Plot", command=self.export_plot,
                  font=("Consolas", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear Log", command=self.clear_log,
                  font=("Consolas", 10)).pack(side="left", padx=5)

    def append_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def export_text(self):
        content = self.output_text.get("1.0", tk.END)
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                f.write(content)
            self.append_output(f"Log exported to: {filename}")

    def export_pdf(self):
        content = self.output_text.get("1.0", tk.END)
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in content.split("\n"):
                pdf.cell(0, 10, txt=line, ln=1)
            pdf.output(filename)
            self.append_output(f"Log exported to: {filename}")

    def export_plot(self):
        # Example: plot the last 10 calculation results (adapt as needed)
        # Here, we just show how to save a dummy plot
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
        plt.title("Sample Plot")
        filename = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            plt.savefig(filename)
            plt.close()
            self.append_output(f"Plot exported to: {filename}")

    def clear_log(self):
        self.output_text.delete("1.0", tk.END)
        self.append_output("Log cleared.")


if __name__ == "__main__":
    app = BridgeTabsGUI()
    app.mainloop()
