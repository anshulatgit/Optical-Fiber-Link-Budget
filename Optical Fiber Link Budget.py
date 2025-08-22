


##############      ##############     ###############

## Optical fiber project



import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

def calculate_link_budget(tx_power, rx_sensitivity, fiber_length, attenuation_per_km, 
                         connector_loss, num_connectors, splice_loss, num_splices, 
                         safety_margin, amplifier_gain=0):
    """
    Calculate the optical link power budget.
    - amplifier_gain: Optional gain from an amplifier (e.g., EDFA) in dB.
    """
    fiber_loss = attenuation_per_km * fiber_length
    connectors_loss = connector_loss * num_connectors
    splices_loss = splice_loss * num_splices
    total_loss = fiber_loss + connectors_loss + splices_loss + safety_margin - amplifier_gain
    received_power = tx_power - total_loss
    is_feasible = received_power >= rx_sensitivity
    return received_power, total_loss, is_feasible

def calculate_dispersion_limit(dispersion_coeff, bit_rate):
    """
    Approximate dispersion-limited length (km) for ~1 dB penalty.
    Formula: L_max ≈ 100000 / (D * B^2), D in ps/nm/km, B in Gbps.
    """
    if dispersion_coeff == 0 or bit_rate == 0:
        return float('inf')
    return 100000 / (dispersion_coeff * bit_rate ** 2)

def calculate_ber(received_power, noise_floor=-30, amplifier_noise_factor=0):
    """
    Estimate BER for QPSK modulation based on OSNR.
    - noise_floor: Receiver noise power in dBm (default -30 dBm).
    - amplifier_noise_factor: Noise added by amplifier in dB (0 if no amplifier).
    """
    # Convert received power to linear scale (mW)
    p_signal_mw = 10 ** (received_power / 10)
    p_noise_mw = 10 ** (noise_floor / 10) + (10 ** (amplifier_noise_factor / 10) if amplifier_noise_factor > 0 else 0)
    
    # Calculate OSNR (linear)
    osnr = p_signal_mw / p_noise_mw if p_noise_mw > 0 else float('inf')
    
    # Q-factor approximation for QPSK
    q_factor = np.sqrt(2 * osnr)
    
    # BER calculation: BER ≈ 0.5 * erfc(Q / √2)
    ber = 0.5 * erfc(q_factor / np.sqrt(2))
    return max(ber, 1e-15)  # Cap at 1e-15 to avoid numerical issues

# Get user inputs
print("Optical Fiber Link Budget Calculator")
tx_power = float(input("Transmitter Power (dBm): "))
rx_sensitivity = float(input("Receiver Sensitivity (dBm): "))
fiber_length = float(input("Fiber Length (km): "))
attenuation_per_km = float(input("Fiber Attenuation (dB/km, e.g., 0.2 for 1550nm SMF): "))
connector_loss = float(input("Loss per Connector (dB, e.g., 0.3): "))
num_connectors = int(input("Number of Connectors: "))
splice_loss = float(input("Loss per Splice (dB, e.g., 0.1): "))
num_splices = int(input("Number of Splices: "))
safety_margin = float(input("Safety Margin (dB, e.g., 3-6): "))
amplifier_gain = float(input("Amplifier Gain (dB, 0 if none): "))
bit_rate = float(input("Bit Rate (Gbps, e.g., 10): "))
dispersion_coeff = float(input("Dispersion Coefficient (ps/nm/km, e.g., 17 for 1550nm SMF): "))
noise_floor = float(input("Receiver Noise Floor (dBm, e.g., -30): "))
amplifier_noise_factor = float(input("Amplifier Noise Factor (dB, 0 if none): "))

# Calculate power budget
received_power, total_loss, is_power_feasible = calculate_link_budget(
    tx_power, rx_sensitivity, fiber_length, attenuation_per_km, 
    connector_loss, num_connectors, splice_loss, num_splices, 
    safety_margin, amplifier_gain
)

# Calculate dispersion limit
disp_limit = calculate_dispersion_limit(dispersion_coeff, bit_rate)
is_disp_feasible = fiber_length <= disp_limit

# Calculate BER
ber = calculate_ber(received_power, noise_floor, amplifier_noise_factor)

# Overall feasibility (considering power and dispersion, BER is informational)
is_overall_feasible = is_power_feasible and is_disp_feasible

# Output results
print("\nResults:")
print(f"Total Loss: {total_loss:.2f} dB")
print(f"Received Power: {received_power:.2f} dBm")
print(f"Power Feasible: {'Yes' if is_power_feasible else 'No'}")
print(f"Dispersion Limit: {disp_limit:.2f} km")
print(f"Dispersion Feasible: {'Yes' if is_disp_feasible else 'No'}")
print(f"Bit Error Rate (BER): {ber:.2e}")
print(f"Overall Feasible: {'Yes' if is_overall_feasible else 'No'}")

# Plot power vs distance
distances = np.linspace(0, fiber_length, 100)
effective_attenuation = (attenuation_per_km * fiber_length - amplifier_gain) / fiber_length if fiber_length > 0 else 0
powers = tx_power - effective_attenuation * distances

plt.plot(distances, powers)
plt.xlabel('Distance (km)')
plt.ylabel('Power (dBm)')
plt.title('Power vs Distance Along the Fiber')
plt.grid(True)
plt.show()


