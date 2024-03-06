import covalent as ct
import covalent_cloud as cc
import random
import time
import os

cc.save_api_key(os.environ["CC_API_KEY"])

HIGH_COMPUTE = cc.CloudExecutor(num_cpus=2)

LOW_COMPUTE = cc.CloudExecutor(num_cpus=1)


@ct.electron(executor=HIGH_COMPUTE)
def high_compute_function():
    # sleep for 5 minutes
    time.sleep(5 * 60)
    return random.choice(["done", "failed"])


@ct.lattice(executor=LOW_COMPUTE, workflow_executor=LOW_COMPUTE)
def covalent_workflow(num_runs=10):
    results = []
    for _ in range(num_runs):
        results.append(high_compute_function())
    return results
