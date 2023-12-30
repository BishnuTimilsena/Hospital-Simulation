import simpy
import random

# This function generates patient
def patient_generator(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter):
    p_id = 0  
    while p_id < num_patients:  
        # Generate a new patient
        patient = activity_generator(env, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, p_id)
        env.process(patient)  # Add the patient to the simulation environment
        t = random.expovariate(1.0 / ed_inter)  # Time until the next patient arrives
        yield env.timeout(t)  # Wait for the next patient
        p_id += 1 

# This function generates the activities for each patient
def activity_generator(env, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, p_id):
    entry_times = {  # Dictionary to store the times at which each activity starts
        'registration': env.now,
        'triage': None,
        'acu_assessment': None,
        'ed_assessment': None,
        'leave_system': None
    }

    # Add a delay before registration
    if p_id != 0:
        delay_before_registration = random.expovariate(1.0 / mean_register)
        yield env.timeout(delay_before_registration)

    # Registration process
    with receptionist.request() as req:
        yield req
        entry_times['triage'] = env.now
        print("Patient", p_id, "queued for registration for ", entry_times['triage'] - entry_times['registration'], " minutes", sep="")
        sampled_registration_time = random.expovariate(1.0 / mean_register)
        yield env.timeout(sampled_registration_time)

    # Triage process
    with nurse.request() as req:
        yield req
        entry_times['triage'] = env.now
        print("Patient ", p_id, " queued for triage for ", entry_times['triage'] - entry_times['registration'], " minutes", sep="")
        sampled_triage_time = random.expovariate(1.0 / mean_triage)
        yield env.timeout(sampled_triage_time)

    # Decide if patient goes to ACU or ED
    decide_acu_branch = random.uniform(0, 1)
    if decide_acu_branch < 0.2:  # Patient goes to ACU
        with acu_doctor.request() as req:
            yield req
            entry_times['acu_assessment'] = env.now
            print("Patient ", p_id, "queued for acu assessment for ", entry_times['acu_assessment'] - entry_times['triage'], " minutes", sep="")
            sampled_acu_assess_time = random.expovariate(1.0 / mean_acu_assess)
            yield env.timeout(sampled_acu_assess_time)
    else:  # Patient goes to ED
        with ed_doctor.request() as req:
            yield req
            entry_times['ed_assessment'] = env.now
            print("Patient ", p_id, "queued for ed assessment for ", entry_times['ed_assessment'] - entry_times['triage'], " minutes", sep="")
            sampled_ed_assess_time = random.expovariate(1.0 / mean_ed_assess)
            yield env.timeout(sampled_ed_assess_time)

    # Patient leaves the system
    entry_times['leave_system'] = env.now
    print("Patient", p_id, "left the system after ", entry_times['leave_system'] - entry_times['registration'], " minutes", sep="")

# This function runs the simulation
def run_simulation(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter):
    env.process(patient_generator(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter))  # Start the patient generator
    env.run(until=450)  # Run the simulation until the specified time
