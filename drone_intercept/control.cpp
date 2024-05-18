#include <iostream>
#include <cmath>
#include <vector>

// Structure to represent the position of a drone
struct Position {
    double latitude;
    double longitude;
};

// Function to update the position of the friendly drone
Position update_position(Position current, Position target, double speed) {
    double direction_lat = target.latitude - current.latitude;
    double direction_lon = target.longitude - current.longitude;
    double distance = std::sqrt(direction_lat * direction_lat + direction_lon * direction_lon);
    if (distance < speed) {
        return target;
    }
    Position new_position;
    new_position.latitude = current.latitude + speed * direction_lat / distance;
    new_position.longitude = current.longitude + speed * direction_lon / distance;
    return new_position;
}

// Function to generate a circular path for the rogue drone
std::vector<Position> generate_rogue_path(Position start, double radius, int total_steps) {
    std::vector<Position> path(total_steps);
    for (int i = 0; i < total_steps; ++i) {
        double theta = 2 * M_PI * i / total_steps;
        path[i].latitude = start.latitude + radius * std::cos(theta);
        path[i].longitude = start.longitude + radius * std::sin(theta);
    }
    return path;
}

int main() {
    // Simulation parameters
    int total_steps = 1000;
    double speed = 0.0001; // Movement speed per time step
    double radius = 0.001; // Radius of the rogue drone's circular path

    // Initial positions
    Position friendly = {37.7749, -122.4194};
    Position rogue_start = {37.7849, -122.4094};

    // Generate the rogue drone's path
    std::vector<Position> rogue_path = generate_rogue_path(rogue_start, radius, total_steps);

    // Run the simulation
    for (int i = 0; i < total_steps; ++i) {
        friendly = update_position(friendly, rogue_path[i], speed);
        std::cout << "Step " << i << ": Friendly Position: (" << friendly.latitude << ", " << friendly.longitude << ")\n";
        std::cout << "Step " << i << ": Rogue Position: (" << rogue_path[i].latitude << ", " << rogue_path[i].longitude << ")\n";
        if (std::abs(friendly.latitude - rogue_path[i].latitude) < 0.0001 && std::abs(friendly.longitude - rogue_path[i].longitude) < 0.0001) {
            std::cout << "Rogue drone intercepted at step " << i << "!\n";
            break;
        }
    }

    return 0;
}
