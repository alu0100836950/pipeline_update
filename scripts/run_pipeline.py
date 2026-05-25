import subprocess
import sys
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

def load_plugins():

    with open("../config/plugins.json") as f:
        return json.load(f)


def run():
    """Run the test suite using pytest."""

    #use load_plugins to get the list of plugins to test, this is for future use, for now we will test only one plugin, but in the future we can test multiple plugins, this is for future scalability
    plugins = load_plugins()
    print(f"Running tests for plugins: {', '.join([plugin['slug'] for plugin in plugins])}")

    #TODO: for each plugin, run the tests, this is for future use, for now we will test only one plugin, but in the future we can test multiple plugins, this is for future scalability
    
    result = subprocess.run(
        ['pytest', "-v", "-s", "../tests/plugins/delivery_date"],
        text=True,
    )
    if result.returncode == 0:
        print("Tests completed successfully.")
        run_release_script(plugins[0])  # Pass the first plugin for release
    else:
        print(f"Tests failed with exit code {result.returncode}.")
        print("Tests failed, skipping release script.")
        sys.exit(1)
    

def type_plugins():
    while True:
        choice = input("Selecciona el tipo de plugins a actualizar (1: free, 2: premium): ").strip()
        if choice == "1":
            return "free"
        elif choice == "2":
            return "premium"
        else:
            print("Opción no válida. Por favor, selecciona 1 o 2.")
   
        return choice

def version_request():
    #Una vez iniciado el programa, se selecciona que tipo de actualizacion va a realizar
    type_version = input("Selecciona el tipo de versión a actualizar (1: wc, 2: wp, 3: both): ").strip()

    # Diccionario donde guardaremos las versiones seleccionadas
    versions = {}

    # Según la elección, pedimos la(s) versión(es)
    if type_version == "1":
        versions["wc"] = input("Introduce la nueva versión de WooCommerce: ").strip()

    elif type_version == "2":
        versions["wp"] = input("Introduce la nueva versión de WordPress: ").strip()

    elif type_version == "3":
        versions["wc"] = input("Introduce la nueva versión de WooCommerce: ").strip()
        versions["wp"] = input("Introduce la nueva versión de WordPress: ").strip()

    else:
        print("Opción no válida.")
        return None

    return type_version, versions

def run_release_script(plugin):
    """Run the release script."""
    selected_plugin_type = type_plugins()
    type_version, versions = version_request()
    try:
        result = subprocess.run(["python3", "release_script.py", "--type_plugins", selected_plugin_type, "--gitpath", plugin["gitpath"], "--type_version", type_version, "--versions", json.dumps(versions)])
        if result.returncode == 0:
            print("Release script executed successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"Release script failed with exit code {e.returncode}.")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
if __name__ == "__main__":
    run()
