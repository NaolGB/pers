import os
import subprocess

def run_tests():
    # Command to run pytest
    pytest_command = "pytest"

    # Set the DJANGO_SETTINGS_MODULE environment variable if needed
    os.environ["DJANGO_SETTINGS_MODULE"] = "pers.settings"

    # Find all test files in 'tests' folders recursively
    test_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))

    # Run tests for each discovered test file
    for test_file in test_files:
        subprocess.run(f"{pytest_command} {test_file}", shell=True)

if __name__ == "__main__":
    run_tests()
