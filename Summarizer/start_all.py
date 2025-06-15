import subprocess

processes = [
    ["uvicorn", "main:app", "--reload"],
    ["python", "slack_fetcher.py"],
    ["python", "discord_fetcher.py"],
    ["python", "telegram_fetcher.py"],
    ["python", "generating_summary.py"],
]

procs = [subprocess.Popen(p) for p in processes]

try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    print("Shutting down all processes...")
    for p in procs:
        p.terminate()
