import subprocess

def authenticate_with_touch_id():
    try:
        # Run the Swift script
        result = subprocess.run(
            ["swift", "touch_di.swift"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Result:", result.stdout.strip())
        else:
            print("Error:", result.stderr.strip())
    except Exception as e:
        print("An error occurred:", str(e))

authenticate_with_touch_id()
