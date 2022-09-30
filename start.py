import subprocess

def run_bot():
   subprocess.check_call(["python", "all/main.py"])


if __name__ == "__main__":
    run_bot()