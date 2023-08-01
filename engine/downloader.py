import subprocess
import sys
import traceback
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

log_dir = os.path.join(os.getenv('APPDATA'), 'MyApp')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'error_log.txt')

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
        with open(log_file, 'a') as f:
            f.write(traceback.format_exc())
        print(f"Failed to install {package}. Error: {str(e)}")

print("All dependencies up-to-date.")