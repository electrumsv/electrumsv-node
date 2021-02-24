"""This script transfers the bitcoin binaries to electrumsv_node/bin/ to be included in the wheel"""

import os
import shutil
import subprocess
from pathlib import Path

print(f"Copying official binaries to electrumsv_node/bin/", flush=True)

target_names = ("bitcoind", "bitcoin-cli")

subprocess.run(['wget https://download.bitcoinsv.io/bitcoinsv/1.0.7/bitcoin-sv-1.0.7-x86_64-linux-gnu.tar.gz'],
    shell=True)
subprocess.run(f"tar xvf bitcoin-sv-1.0.7-x86_64-linux-gnu.tar.gz", shell=True)
print(os.listdir())

for target_name in target_names:
    file_path = Path(os.getcwd()).joinpath(f"bitcoin-sv-1.0.7/bin/{target_name}")
    print(f"copying file: {file_path} to: {file_path}")
    shutil.copy(file_path, "electrumsv_node/bin/")
