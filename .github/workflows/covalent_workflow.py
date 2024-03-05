from enum import Enum
import covalent as ct
import covalent_cloud as cc
import random

import sys

sys.path.append(".")
import os

import time
import csv


class Status(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


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


def update_runid(
    runid, status=Status.PENDING, runid_file=".github/workflows/runid_status.csv"
):
    # Check if the CSV file exists
    if not os.path.exists(runid_file):
        # Create a new CSV file with headers
        with open(runid_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["runid", "status"])

    # Check if the runid already exists in the CSV file
    with open(runid_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == runid:
                # Update the status for the existing runid
                row[1] = status.value
                break
        else:
            # Add the new runid and status to the CSV file
            with open(runid_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([runid, status.value])


def check_and_update_status(
    runid_file=".github/workflows/runid_status.csv",
    results_file=".github/workflows/results.csv",
):
    with open(runid_file, "r") as file:
        reader = csv.reader(file)
        updated_data = []
        for row in reader:
            if row and row[1] == Status.PENDING.value:
                result = cc.get_result(row[0])
                if result.status == "COMPLETED":

                    # Update status in runid_file
                    row[1] = Status.COMPLETED.value
                    # Write result to the results file
                    write_result_to_file(row[0], result, results_file)
                elif result.status in ["FAILED", "CANCELLED"]:
                    row[1] = result.status
            updated_data.append(row)

    # Rewrite the runid_status.csv with updated statuses
    with open(runid_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_data)


def write_result_to_file(runid, result, results_file):
    result.result.load()
    value = result.result.value

    # Check if results file exists
    if not os.path.exists(results_file):
        with open(results_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["runid", "timestamp", "status", "result"])

    with open(results_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([runid, time.time(), result.status, value])


if __name__ == "__main__":
    # Set the API key
    cc.save_api_key(os.environ["CC_API_KEY"])

    runid = cc.dispatch(covalent_workflow)(num_runs=10)
    update_runid(runid, Status.PENDING)
    check_and_update_status(
        runid_file=".github/workflows/runid_status.csv",
        results_file=".github/workflows/results.csv",
    )
