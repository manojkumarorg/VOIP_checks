import subprocess
import os
import sys

def run_scripts():
    scripts = [
        "network_sniffer.py",
        "audio_extractor.py",
        "speech_recognition.py",
        "get_location.py",
    ]

    for script in scripts:
        script_path = os.path.join("D:/voip/scripts", script)
        print(f"Running script: {script_path}")
        subprocess.run([sys.executable, script_path])

if __name__ == "__main__":
    run_scripts()
