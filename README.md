# Optical Fiber Link Budget Calculator

This project is a **Python-based optical fiber link budget calculator** for point-to-point optical communication systems.  

It helps you quickly check whether a given optical link is **power-feasible**, **dispersion-feasible**, and gives an approximate **Bit Error Rate (BER)** for a QPSK-modulated system.

---

## Features

- Calculates **total link loss**:
  - Fiber attenuation  
  - Connector losses  
  - Splice losses  
  - Safety margin  
  - Optional **amplifier gain** (e.g., EDFA)

- Computes **received optical power** at the receiver in dBm.

- Checks **power feasibility**:
  - Compares received power with receiver sensitivity.

- Estimates **dispersion-limited distance**:
  - Uses an approximate formula:  
    \[
    L_{\text{max}} \approx \frac{100000}{D \cdot B^2}
    \]  
    where:
    - \(D\) = dispersion coefficient (ps/nm/km)  
    - \(B\) = bit rate (Gbps)

- Estimates **BER for QPSK** based on OSNR:
  - Converts received power and noise floor to linear scale  
  - Calculates Q-factor and then BER using complementary error function.

- Plots **Power vs Distance** along the fiber.

---

## Technologies Used

- Python 3
- NumPy
- Matplotlib
- SciPy (`scipy.special.erfc`)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
