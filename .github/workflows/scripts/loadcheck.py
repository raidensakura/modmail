import os
import signal
import subprocess
import sys
import time

from dotenv import load_dotenv

load_dotenv(".env")

python_version = subprocess.check_output(["python", "-V"]).decode("utf-8")

print(f"Starting Modmail with {python_version}")

file = open("modmail.log", "w")
proc = subprocess.Popen(
    "pipenv run bot",
    stdout=file,
    stderr=subprocess.STDOUT,
    shell=True,
)

# let Modmail boot up
time.sleep(15)

exit_code = 1 if proc.poll() else 0

print("Stopping Modmail")

os.kill(proc.pid, signal.SIGINT)

time.sleep(5)

sys.exit(exit_code)
