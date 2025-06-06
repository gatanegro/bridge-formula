# Universal Bridge Formula Calculator

This software implements the universal bridge formula for characteristic mass and radii:

**Mass Formula:**
$$m = m_e \cdot \text{LZ}^{n/\pi} \cdot \left(\frac{\alpha}{\text{HQS}}\right)^{1/x}$$

**Radius Formula:**
$$r = r_e \cdot \text{LZ}^{n/\pi} \cdot \left(\frac{\alpha}{\text{HQS}}\right)^{1/x}$$

Where:
- m, r: predicted mass or radius
- m_e, r_e: Reference mass or radius
- LZ: Collatz attractor constant (1.23498228)
- n: Collatz octave (recursion number)
- π: Pi (3.141592653589793)
- α: Fine-structure constant (0.0072973525643)
- HQS: Ricci threshold (0.235)
- x: Lyapunov inverse (16.450911914534554)

## Features

The calculator provides the following functionality:

1. **Mass Calculations:**
   - Calculate mass (m) given n and a reference mass
   - Calculate n given mass and reference mass
   - Reference masses: Planck, Electron, Atomic, Earth

2. **Radius Calculations:**
   - Calculate radius (r) given n and a reference radius
   - Calculate n given radius and reference radius
   - Reference radii: Planck length, Electron radius, Bohr radius, Venus radius

## How to Use
2. The interface has three main tabs:
   - **Mass Calculations:** For calculating mass from n or n from mass
   - **Radius Calculations:** For calculating radius from n or n from radius
   - **Constants:** View all constants and reference values used in the calculations

3. For each calculation:
   - Select the appropriate reference value (mass or radius)
   - Enter the input value (n, mass, or radius)
   - Click "Calculate" to see the result and visualization

## Reference Values

### Mass References
- Planck Mass: 2.176434e-08 kg
- Electron Mass: 9.109384e-31 kg
- Atomic Mass Unit: 1.660539e-27 kg
- Earth Mass: 5.972200e+24 kg

### Radius References
- Planck Length: 1.616255e-35 m
- Electron Radius: 2.817940e-15 m
- Bohr Radius: 5.291772e-11 m
- Venus Radius: 6.051800e+06 m

## Formula Constants
- LZ (Collatz attractor): 1.23498228
- π (Pi): 3.141592653589793
- α (Fine-structure): 0.0072973525643
- x (Lyapunov inverse): 16.450911914534554
- HQS (Ricci threshold): 0.235

