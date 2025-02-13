import sys
from cx_Freeze import setup, Executable
from pathlib import Path
import spacy
import transformers
import os

# Increase maximum recursion depth
sys.setrecursionlimit(50000)  # Adjust as necessary (default is usually 1000)

# Locate site-packages directory for spacy and transformers
site_packages = Path(spacy.__file__).parent.parent

# Locate spacy model path
spacy_model_path = site_packages / "en_core_web_md"

# Find subfolder starting with 'en_core_web_md-'
model_version_folder = None
for subfolder in os.listdir(spacy_model_path):
    if subfolder.startswith("en_core_web_md-"):
        model_version_folder = spacy_model_path / subfolder
        break

if model_version_folder is None:
    raise Exception("Could not find the versioned model folder starting with 'en_core_web_md-'")

# Locate transformers package folder
transformers_path = Path(transformers.__file__).parent

# Define the executable and options
executables = [
    Executable(
        "antivirus.py",  # Your script
        target_name="antivirus.exe",  # Output executable name
        base="Win32GUI",  # Win32GUI application
        icon="assets/HydraDragonAV.ico",  # Path to your .ico file
        uac_admin=True  # Request admin privileges
    )
]

# Fine-tune build options
build_options = {
    "packages": ["scapy", "srsly", "blis", "spacy", "transformers", "torch"],
    "includes": ["preshed.maps", "numpy.f2py"],
    "excludes": ["tkinter"],
    "include_files": [
        (str(model_version_folder), "en_core_web_md"),  # Include the spacy model folder
        (str(transformers_path), "lib/transformers"),       # Include the transformers folder
    ],
}

# Setup configuration for cx_Freeze
setup(
    name="Hydra Dragon Antivirus",  # Application name
    version="0.1",  # Version number
    description="Hydra Dragon Antivirus",
    options={"build_exe": build_options},  # Build options
    executables=executables,  # List of executables
)
