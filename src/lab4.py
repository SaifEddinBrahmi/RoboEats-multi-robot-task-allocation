import irsim
import numpy as np
import my_solver as ms
import argparse
import os

##### STEP 1: Create the environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config", "RoboEatsCafe_config.yaml")
env = irsim.make(CONFIG_PATH)

##### STEP 2: Point to the two robots
R1 = env.robot_list[0].ego_object
R2 = env.robot_list[1].ego_object

##### STEP 3: Get the list of tables from command line arguments 
parser = argparse.ArgumentParser()
parser.add_argument("tables", type=int, nargs="+",
                    help="List of Tables to be served")
args = parser.parse_args()
tables_to_serve = args.tables
print(f"The list of tables to serve is: {tables_to_serve}")

##### STEP 4: Plan the routes
waypoints_R1, waypoints_R2 = ms.call(tables_to_serve)

R1.set_goal(waypoints_R1)
R2.set_goal(waypoints_R2)

##### STEP 5: Execute the planned routes
for i in range(10000):
    env.step()
    env.render()
    
    if env.done():
        break
env.end()

##### STEP 6: Evaluate the performance
# Calculate trajectory length
def calculate_trajectory_length(traj):
    """Calculate the total path length from trajectory points"""
    if len(traj) < 2:
        return 0.0
    total_length = 0.0
    for i in range(1, len(traj)):
        dx = traj[i][0][0] - traj[i-1][0][0]
        dy = traj[i][1][0] - traj[i-1][1][0]
        total_length += np.sqrt(dx**2 + dy**2)
    
    return total_length


traj_length = calculate_trajectory_length(R1.trajectory)
print(f"Trajectory length R1: {traj_length:.2f} meters")

traj_length = calculate_trajectory_length(R2.trajectory)
print(f"Trajectory length R2: {traj_length:.2f} meters")

total_time = env.time
print(f"Time spent: {total_time:.2f} seconds")

