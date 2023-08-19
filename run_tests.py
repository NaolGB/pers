import os
import subprocess

def run_tests(test_file=None):
    # Command to run pytest
    pytest_command = "pytest"

    # environment variable
    os.environ["DJANGO_SETTINGS_MODULE"] = "pers.settings"
    
    # tests
    if test_file:
        pytest_command += f" {test_file}"

    
    # Use subprocess to run the command
    subprocess.run(pytest_command, shell=True)

if __name__ == "__main__":
    run_tests(test_file="user_management/tests/test_models.py")
    run_tests(test_file="user_management/tests/test_views.py")
