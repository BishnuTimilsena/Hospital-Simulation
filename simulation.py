import simpy
import random

def patient_generator_ed(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter):
    p_id = 0
    while p_id < num_patients:
        patient = activity_generator_ed(env, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, p_id)
        env.process(patient)
        t = random.expovariate(1.0 / ed_inter)
        yield env.timeout(t)
        p_id += 1

def activity_generator_ed(env, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, p_id):
    entry_times = {
        'registration': env.now,
        'triage': None,
        'acu_assessment': None,
        'ed_assessment': None,
        'leave_system': None
    }

    with receptionist.request() as req:
        yield req
        entry_times['triage'] = env.now
        print("Patient", p_id, "queued for registration for ", entry_times['triage'] - entry_times['registration'], " minutes", sep="")
        sampled_registration_time = random.expovariate(1.0 / mean_register)
        yield env.timeout(sampled_registration_time)

    with nurse.request() as req:
        yield req
        entry_times['acu_assessment'] = env.now
        print("Patient ", p_id, " queued for triage for ", entry_times['acu_assessment'] - entry_times['triage'], " minutes", sep="")
        sampled_triage_time = random.expovariate(1.0 / mean_triage)
        yield env.timeout(sampled_triage_time)

    decide_acu_branch = random.uniform(0, 1)
    if decide_acu_branch < 0.2:
        with acu_doctor.request() as req:
            yield req
            entry_times['ed_assessment'] = env.now
            print("Patient ", p_id, "queued for acu assessment for ", entry_times['ed_assessment'] - entry_times['acu_assessment'], " minutes", sep="")
            sampled_acu_assess_time = random.expovariate(1.0 / mean_acu_assess)
            yield env.timeout(sampled_acu_assess_time)
    else:
        with ed_doctor.request() as req:
            yield req
            entry_times['ed_assessment'] = env.now
            print("Patient ", p_id, "queued for ed assessment for ", entry_times['ed_assessment'] - entry_times['acu_assessment'], " minutes", sep="")
            sampled_ed_assess_time = random.expovariate(1.0 / mean_ed_assess)
            yield env.timeout(sampled_ed_assess_time)

    entry_times['leave_system'] = env.now
    print("Patient", p_id, "left the system after ", entry_times['leave_system'] - entry_times['registration'], " minutes", sep="")

def run_simulation(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter):
    env.process(patient_generator_ed(env, num_patients, mean_register, mean_triage, mean_ed_assess, mean_acu_assess, receptionist, nurse, ed_doctor, acu_doctor, ed_inter))
    env.run(until=2880)
