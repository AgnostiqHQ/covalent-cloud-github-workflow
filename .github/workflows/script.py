import sys
import os

sys.path.append(".")

import covalent_cloud as cc
from covalent_workflow import covalent_workflow

from utils import (
    Status,
    update_runid,
    check_and_update_status,
)

if __name__ == "__main__":

    # Set the API key
    cc.save_api_key(os.environ["CC_API_KEY"])

    RUNID_FILE = "runid_status.csv"
    RESULTS_FILE = "results.csv"

    runid = cc.dispatch(covalent_workflow)(num_runs=10)
    update_runid(runid, Status.PENDING, runid_file=RUNID_FILE)
    check_and_update_status(
        runid_file=RUNID_FILE,
        results_file=RESULTS_FILE,
    )
