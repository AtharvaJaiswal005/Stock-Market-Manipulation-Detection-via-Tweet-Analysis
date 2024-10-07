import gdown
import subprocess
import os

# Step 1: Download the Google Drive folder
url = 'https://drive.google.com/drive/folders/1VaRjz7jibiyqnhSESDJ_h1U33Vvhu_xh?usp=sharing'
gdown.download_folder(url, quiet=False, use_cookies=False)
print('All project data files downloaded.')

# Step 2: Check if requirements.txt exists in the current directory
requirements_path = 'requirements.txt'

if os.path.exists(requirements_path):
    print('requirements.txt found. Installing dependencies...')
    try:
        # Install the requirements using pip
        subprocess.check_call(['pip', 'install', '-r', requirements_path])
        print('All dependencies from requirements.txt have been installed.')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
else:
    print('No requirements.txt file found. Skipping dependency installation.')
