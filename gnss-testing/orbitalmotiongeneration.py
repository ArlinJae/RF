import csv
import numpy as np

# Orbital parameters
semi_major_axis = 6778137  # Using 6778137 meters for a typical LEO as value - cross check accuracy of value
eccentricity = 0.001       # Eccentricity of the orbit (close to circular)
inclination = 51.6         # Inclination in degrees (example: 51.6 degrees)
num_points = 100           # Number of points in the trajectory
time_step = 60             # Time step in seconds
orbital_period = 90 * 60   # Orbital period in seconds (example: 90 minutes)

# Earth parameters
earth_radius = 6378137

def mean_anomaly(time, period):
    return 2 * np.pi * (time / period)

def eccentric_anomaly(M, e, tolerance=1e-6):
    E = M  # Initial guess
    while True:
        delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        E -= delta_E
        if abs(delta_E) < tolerance:
            break
    return E

def true_anomaly(E, e):
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

def generate_orbital_trajectory(semi_major_axis, eccentricity, inclination, num_points, time_step, period):
    trajectory = []
    for i in range(num_points):
        time = i * time_step
        M = mean_anomaly(time, period)
        E = eccentric_anomaly(M, eccentricity)
        v = true_anomaly(E, eccentricity)
        r = semi_major_axis * (1 - eccentricity * np.cos(E))
        x = r * np.cos(v)
        y = r * np.sin(v)
        z = 0
        # Rotate to account for inclination
        x_rot = x
        y_rot = y * np.cos(np.radians(inclination)) - z * np.sin(np.radians(inclination))
        z_rot = y * np.sin(np.radians(inclination)) + z * np.cos(np.radians(inclination))
        trajectory.append((time, x_rot, y_rot, z_rot))
    return trajectory

# Generate the trajectory data
trajectory_data = generate_orbital_trajectory(semi_major_axis, eccentricity, inclination, num_points, time_step, orbital_period)

# Write to CSV file
csv_filename = 'orbital_motion.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['# time(s)', 'x(m)', 'y(m)', 'z(m)'])
    for data in trajectory_data:
        writer.writerow(data)

print(f"Generated {csv_filename} with {num_points} points.")
