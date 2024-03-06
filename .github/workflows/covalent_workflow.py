import covalent as ct
import covalent_cloud as cc
import random
import time
import os

# Set the API key for the cloud
cc.save_api_key(os.environ["CC_API_KEY"])

# Executors define the compute and environment resources for the tasks
# learn more about executors at https://docs.covalent.xyz/
HIGH_COMPUTE = cc.CloudExecutor(num_cpus=2)
LOW_COMPUTE = cc.CloudExecutor(num_cpus=1)


# Electrons are units of tasks that can be executed on the cloud with the defined executor resource
@ct.electron(executor=HIGH_COMPUTE)
def high_compute_function():
    # sleep for 5 minutes
    time.sleep(5 * 60)
    return random.choice(["done", "failed"])


# Lattices are workflows that execute multiple tasks in sequence or parallel with dependencies between them
# They are just python functions that call electrons (tasks) and tie them together
@ct.lattice(executor=LOW_COMPUTE, workflow_executor=LOW_COMPUTE)
def covalent_workflow(num_runs=10):
    results = []
    for _ in range(num_runs):
        results.append(high_compute_function())
    return results
