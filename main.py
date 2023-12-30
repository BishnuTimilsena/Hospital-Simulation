import simpy
import random
from simulation import run_simulation

# Set up simulation environment
env = simpy.Environment()

# Set up resources
receptionist = simpy.Resource(env, capacity=1)
nurse = simpy.Resource(env, capacity=2)
ed_doctor = simpy.Resource(env, capacity=1)
acu_doctor = simpy.Resource(env, capacity=1)

# Set up parameter values
ed_inter = 5
mean_register = 2
mean_triage = 5
mean_ed_assess = 20
mean_acu_assess = 10

# Number of patients to simulate
num_patients = 20

# Run the simulation
run_simulation(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter)