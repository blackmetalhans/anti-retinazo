import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", res.stdout.strip())
    if res.stderr.strip():
        print("STDERR:", res.stderr.strip())
    return res.returncode

# 1. git add .
run_cmd(["git", "add", "."])

# 2. git commit
run_cmd(["git", "commit", "-m", "feat: Anti-Retinazo - Filtro de luz azul Win32 zero-bloat"])

# 3. Create repo with gh CLI and push
desc = "Filtro de luz azul Win32 ultra-liviano (~12MB RAM, 0% CPU, Hardware GDI) para gente que no quiere quemar 400MB de RAM en un slider de Electron."
code = run_cmd(["gh", "repo", "create", "anti-retinazo", "--public", f"--description={desc}", "--source=.", "--remote=origin", "--push"])

if code != 0:
    print("Trying git push to existing origin...")
    run_cmd(["git", "push", "-u", "origin", "main"])

# Verify remote url
run_cmd(["git", "remote", "-v"])
