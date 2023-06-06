import os
import subprocess
import sys
import time

from dotenv import load_dotenv

load_dotenv(".env")

python_version = subprocess.check_output(["python", "-V"]).decode("utf-8")

print(f"Starting Modmail with {python_version}")

file = open("modmail.log", "w")
proc = subprocess.Popen(
    f"pipenv run bot",
    stdout=file,
    stderr=subprocess.STDOUT,
    shell=True,
)

# let Modmail boot up
time.sleep(10)

print("Stopping Modmail")

proc.terminate()

print(f"Modmail stopped with exit code {proc.returncode()}")

sys.exit(proc.returncode())
