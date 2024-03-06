import sys

sys.path.append(".")

import covalent_cloud as cc
from covalent_workflow import covalent_workflow

from utils import (
    Status,
    update_runid,
    check_and_update_status,
)

if __name__ == "__main__":

    RUNID_FILE = "runid_status.csv"
    RESULTS_FILE = "results.csv"

    # Dispatch the workflow to the Covalent Cloud
    runid = cc.dispatch(covalent_workflow)(num_runs=10)
    print(f"Dispatched runid: {runid} Submitted")

    # Update the runid status to PENDING
    update_runid(runid, Status.PENDING, runid_file=RUNID_FILE)
    print(f"Runid: {runid} Status: {Status.PENDING.value} Updated")

    # Check and update the runid status
    check_and_update_status(
        runid_file=RUNID_FILE,
        results_file=RESULTS_FILE,
    )
    print(
        f"Old runid status updated in {RUNID_FILE} and results written to {RESULTS_FILE}"
    )
