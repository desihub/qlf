from qlf_models import QLFModels
import sys
import os
import json

qlf_models = QLFModels()
qlf_root = os.environ.get('QLF_ROOT')

def migrate_job_outputs():
    metrics_path = os.path.join(
        qlf_root, "framework", "ql_mapping",
        "metrics.json")

    with open(metrics_path) as f:
        metrics = json.load(f)
    qlf_models.migrate_outputs(metrics)


if __name__ == "__main__":
    migrate_job_outputs()
