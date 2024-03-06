import sys

sys.path.append(".")

import time
from enum import Enum
import os
import csv

import covalent_cloud as cc


class Status(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


def update_runid(runid, status=Status.PENDING, runid_file="runid_status.csv"):
    """Update the status of the runid in the CSV file. If the runid does not exist, add it to the CSV file."""
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
    runid_file="runid_status.csv",
    results_file="results.csv",
):
    """Check the status of the runids in the CSV file and update the status if the task is completed. Write the results to the results file."""
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
    """Write the result of a runid to the results file. If the results file does not exist, create it."""
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
