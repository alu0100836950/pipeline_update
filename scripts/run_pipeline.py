import subprocess
import sys
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

def load_plugins():

    with open("../config/plugins.json") as f:
        return json.load(f)


def run_test():
    """Run the test suite using pytest."""

    #use load_plugins to get the list of plugins to test, this is for future use, for now we will test only one plugin, but in the future we can test multiple plugins, this is for future scalability
    plugins = load_plugins()
    print(f"Running tests for plugins: {', '.join(plugins)}")


    #for each plugin, run the tests, this is for future use, for now we will test only one plugin, but in the future we can test multiple plugins, this is for future scalability


    result = subprocess.run(
        ['pytest', "-v", "-s", "../tests/plugins/delivery_date"],
        text=True,
    )
    if result.returncode == 0:
        print("Tests completed successfully.")
        return True
    else:
        print(f"Tests failed with exit code {result.returncode}.")
        return False

def run_release_script():
    """Run the release script."""
    try:
        result = subprocess.run([ 'python3', 'release_script.py'], capture_output=True, text=True)
        print("Release script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Release script failed with exit code {e.returncode}.")

if __name__ == "__main__":
    if run_test():
        print("Tests passed, running release script...")
        run_release_script()
    else:
        print("Tests failed, skipping release script.")
        sys.exit(1)
