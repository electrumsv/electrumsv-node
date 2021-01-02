"""This script transfers the bitcoin binaries to electrumsv_node/bin/ to be included in the wheel"""

import os
import shutil
import subprocess
import sys

print(f"Copying compiled bitcoin binaries to electrumsv_node/bin/", flush=True)


def _resolve_bsv_build_path() -> str:
    build_path = os.environ.get("BSV_BUILD_PATH")
    if build_path is None:
        build_path = "bitcoin-sv"
    return build_path


BSV_BUILD_PATH = _resolve_bsv_build_path()

target_names = ("bitcoind", "bitcoin-seeder", "bitcoin-cli", "bitcoin-tx", "bitcoin-miner")

if not os.path.exists(BSV_BUILD_PATH):
    sys.exit(f"Failed to locate the Bitcoin SV build directory: {BSV_BUILD_PATH}")

for target_name in target_names:
    artifact_path = os.path.join(BSV_BUILD_PATH, "src", target_name)
    subprocess.run(f"strip {artifact_path}", shell=True)
    shutil.copy(artifact_path, "electrumsv_node/bin/")
