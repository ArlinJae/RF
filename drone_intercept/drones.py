import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the simulation parameters
simulation_time = 100  # seconds
time_step = 0.1  # seconds
total_steps = int(simulation_time / time_step)
speed = 0.0001  # degrees per time step

# Initial positions (latitude, longitude) for the drones
friendly_drone = np.array([37.7749, -122.4194])
rogue_drone = np.array([37.7849, -122.4094])

# Store positions for plotting
friendly_path = np.zeros((total_steps, 2))
rogue_path = np.zeros((total_steps, 2))

# Predefined path for the rogue drone (for simplicity, a circular path)
theta = np.linspace(0, 2 * np.pi, total_steps)
rogue_path[:, 0] = rogue_drone[0] + 0.001 * np.cos(theta)  # Latitude changes
rogue_path[:, 1] = rogue_drone[1] + 0.001 * np.sin(theta)  # Longitude changes

# Function to update drone positions
def update_position(current, target, speed):
    direction = target - current
    distance = np.linalg.norm(direction)
    if distance < speed:
        return target
    return current + speed * direction / distance

# Initialize figure and axes for the animation
fig, ax = plt.subplots()
ax.set_xlim(37.77, 37.79)
ax.set_ylim(-122.43, -122.40)
friendly_plot, = ax.plot([], [], 'bo-', label='Friendly Drone')
rogue_plot, = ax.plot([], [], 'ro-', label='Rogue Drone')

# Initialization function for the animation
def init():
    friendly_plot.set_data([], [])
    rogue_plot.set_data([], [])
    return friendly_plot, rogue_plot

# Animation update function
def animate(i):
    global friendly_drone
    friendly_drone[:] = update_position(friendly_drone, rogue_path[i], speed)
    friendly_path[i, :] = friendly_drone
    friendly_plot.set_data(friendly_path[:i+1, 0], friendly_path[:i+1, 1])
    rogue_plot.set_data(rogue_path[:i+1, 0], rogue_path[:i+1, 1])
    return friendly_plot, rogue_plot

# Create the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=total_steps, interval=100, blit=True)

# Add labels and legend
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.legend()

# Show the plot
plt.show()
