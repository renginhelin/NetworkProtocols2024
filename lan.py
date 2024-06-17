import random
import matplotlib.pyplot as plt

# Constants
PACKET_TIME = 1.0  # Time taken for one packet to transmit
TIME_SLOTS = 10000  # Number of time slots to simulate

# Simulation parameters
device_counts = list(range(5, 55, 5))
protocols = ["Pure ALOHA", "Slotted ALOHA", "1-persistent CSMA", "0.5-persistent CSMA", "CSMA/CD"]

# Function to simulate Pure ALOHA
def simulate_pure_aloha(device_count, attempts_per_time_unit):
    successful_transmissions = 0
    total_transmissions = 0
    
    for _ in range(TIME_SLOTS):
        transmissions = 0
        for _ in range(device_count):
            if random.random() < attempts_per_time_unit / device_count:
                transmissions += 1
        total_transmissions += transmissions
        if transmissions == 1:
            successful_transmissions += 1
            
    return successful_transmissions / total_transmissions if total_transmissions else 0

# Function to simulate Slotted ALOHA
def simulate_slotted_aloha(device_count, attempts_per_time_unit):
    successful_transmissions = 0
    total_transmissions = 0
    
    for _ in range(TIME_SLOTS):
        transmissions = 0
        for _ in range(device_count):
            if random.random() < attempts_per_time_unit / device_count:
                transmissions += 1
        total_transmissions += transmissions
        if transmissions == 1:
            successful_transmissions += 1
            
    return successful_transmissions / total_transmissions if total_transmissions else 0

# Function to simulate 1-persistent CSMA
def simulate_1_persistent_csma(device_count, attempts_per_time_unit):
    successful_transmissions = 0
    total_transmissions = 0
    channel_busy = False
    
    for _ in range(TIME_SLOTS):
        transmissions = 0
        for _ in range(device_count):
            if not channel_busy and random.random() < attempts_per_time_unit / device_count:
                transmissions += 1
        total_transmissions += transmissions
        if transmissions == 1:
            successful_transmissions += 1
            channel_busy = True
        else:
            channel_busy = False
            
    return successful_transmissions / total_transmissions if total_transmissions else 0

# Function to simulate 0.5-persistent CSMA
def simulate_0_5_persistent_csma(device_count, attempts_per_time_unit):
    successful_transmissions = 0
    total_transmissions = 0
    channel_busy = False
    
    for _ in range(TIME_SLOTS):
        transmissions = 0
        for _ in range(device_count):
            if not channel_busy and random.random() < 0.5 * attempts_per_time_unit / device_count:
                transmissions += 1
        total_transmissions += transmissions
        if transmissions == 1:
            successful_transmissions += 1
            channel_busy = True
        else:
            channel_busy = False
            
    return successful_transmissions / total_transmissions if total_transmissions else 0

# Function to simulate CSMA/CD
def simulate_csma_cd(device_count, attempts_per_time_unit):
    successful_transmissions = 0
    total_transmissions = 0
    collision_window = 0  # Time remaining in the collision window
    
    for _ in range(TIME_SLOTS):
        transmissions = 0
        for _ in range(device_count):
            if collision_window == 0 and random.random() < attempts_per_time_unit / device_count:
                transmissions += 1
        total_transmissions += transmissions
        if transmissions == 1:
            successful_transmissions += 1
            collision_window = PACKET_TIME
        elif transmissions > 1:
            collision_window = PACKET_TIME
        else:
            if collision_window > 0:
                collision_window -= 1
                
    return successful_transmissions / total_transmissions if total_transmissions else 0

# Main function to run simulations
def run_simulations():
    results = {protocol: [] for protocol in protocols}
    
    for device_count in device_counts:
        print(f"Simulating for {device_count} devices...")
        G_values = []
        S_values = {protocol: [] for protocol in protocols}
        
        for G in range(1, 11):
            print(f"  Simulating for G={G} attempts per packet time...")
            attempts_per_time_unit = G / PACKET_TIME
            
            # Pure ALOHA
            S_pure_aloha = simulate_pure_aloha(device_count, attempts_per_time_unit)
            S_values["Pure ALOHA"].append(S_pure_aloha)
            
            # Slotted ALOHA
            S_slotted_aloha = simulate_slotted_aloha(device_count, attempts_per_time_unit)
            S_values["Slotted ALOHA"].append(S_slotted_aloha)
            
            # 1-persistent CSMA
            S_1_persistent_csma = simulate_1_persistent_csma(device_count, attempts_per_time_unit)
            S_values["1-persistent CSMA"].append(S_1_persistent_csma)
            
            # 0.5-persistent CSMA
            S_0_5_persistent_csma = simulate_0_5_persistent_csma(device_count, attempts_per_time_unit)
            S_values["0.5-persistent CSMA"].append(S_0_5_persistent_csma)
            
            # CSMA/CD
            S_csma_cd = simulate_csma_cd(device_count, attempts_per_time_unit)
            S_values["CSMA/CD"].append(S_csma_cd)
            
            G_values.append(G)
        
        for protocol in protocols:
            results[protocol].append((G_values, S_values[protocol]))
    
    return results

# Plot results
def plot_results(results):
    for protocol in protocols:
        plt.figure()
        for device_count_index, device_count in enumerate(device_counts):
            G_values, S_values = results[protocol][device_count_index]
            plt.plot(G_values, S_values, label=f'{device_count} devices')
        
        plt.xlabel('G (attempts per packet time)')
        plt.ylabel('S (throughput per packet time)')
        plt.title(f'{protocol} - Channel Utilization vs Load')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    print("Starting simulations...")
    results = run_simulations()
    print("Simulations completed. Plotting results...")
    plot_results(results)
    print("Results plotted.")
