import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

dependencies = [
    "beautifulsoup4",  # for BeautifulSoup
    "requests",        # for requests
    "python-uuid",     # for uuid
    "xlsxwriter",      # for xlsxwriter
    "fuzzywuzzy",      # for fuzz
    "keybert",         # for KeyBERT
]

for package in dependencies:
    print(f"Installing {package}...")
    try:
        install(package)
        print(f"Installed {package}")
    except Exception as e:
        print(f"Failed to install {package}. Error: {str(e)}")

print("All dependencies up-to-date.")