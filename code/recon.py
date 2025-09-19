#!/usr/bin/env python3
"""
Automated Recon - starter script
--------------------------------
This is a minimal starter that:
 - runs `subfinder` to list subdomains
 - runs `httpx` to check which are live
 - saves outputs to the `reports/` folder

Requirements (install on your machine):
 - subfinder (https://github.com/projectdiscovery/subfinder)
 - httpx (https://github.com/projectdiscovery/httpx)
 - Python 3.8+

Usage:
    python3 recon.py -d target.com
    python3 recon.py -d target.com -o myreports
"""
from pathlib import Path
import subprocess
import shlex
import argparse
import shutil
import sys

OUT_DIR_DEFAULT = "reports"

def check_tool(toolname):
    """Return True if `toolname` is found in PATH."""
    return shutil.which(toolname) is not None

def run_command(cmd, timeout=None):
    """Run shell command (safe split) and return stdout as str.
       Prints stderr if command fails but does not raise.
    """
    print(f"[+] Running: {cmd}")
    args = shlex.split(cmd)
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        if proc.returncode != 0:
            print(f"[-] Command exited {proc.returncode}. stderr:\n{proc.stderr.strip()}")
        return proc.stdout
    except subprocess.TimeoutExpired:
        print("[-] Command timed out.")
        return ""

def subfinder_run(domain):
    """Run subfinder and return stdout (subdomains)."""
    return run_command(f"subfinder -d {domain} -silent")

def httpx_run(input_file, output_file):
    """Run httpx to check live hosts from a file of domains."""
    return run_command(f"httpx -l {input_file} -silent -status-code -o {output_file}")

def ensure_out_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True)
        print(f"[+] Created {path}")

def write_file(path: Path, content: str):
    path.write_text(content)
    print(f"[+] Saved -> {path} ({len(content.splitlines())} lines)")

def main():
    parser = argparse.ArgumentParser(description="Automated Recon - starter")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("-o", "--out", default=OUT_DIR_DEFAULT, help="Output folder (default: reports)")
    args = parser.parse_args()

    domain = args.domain.strip()
    out_dir = Path(args.out)
    ensure_out_dir(out_dir)

    # Tool checks
    missing = []
    for t in ("subfinder", "httpx"):
        if not check_tool(t):
            missing.append(t)
    if missing:
        print(f"[-] Missing required tools in PATH: {', '.join(missing)}")
        print("    Install them before running this script. Example: https://github.com/projectdiscovery/subfinder")
        sys.exit(1)

    # Filenames
    subs_file = out_dir / f"{domain}_subs.txt"
    live_file = out_dir / f"{domain}_live.txt"

    # 1) subfinder
    subs_output = subfinder_run(domain)
    if subs_output.strip():
        write_file(subs_file, subs_output)
    else:
        print("[-] subfinder returned no output or failed.")

    # 2) httpx (live check) - uses the subs_file as input
    if subs_file.exists() and subs_file.stat().st_size > 0:
        httpx_out = httpx_run(str(subs_file), str(live_file))
        # httpx already writes to file (via -o), but capture helps when httpx output is printed
        if Path(live_file).exists():
            print(f"[+] httpx results available: {live_file}")
        else:
            # fallback: save whatever stdout we captured
            if httpx_out.strip():
                write_file(live_file, httpx_out)
            else:
                print("[-] httpx produced no output.")
    else:
        print("[-] No subdomains to pass to httpx. Check subfinder output.")

    print("[+] Done. Check the reports folder for results.")

if __name__ == "__main__":
    main()
