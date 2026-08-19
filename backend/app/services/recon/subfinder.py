import shutil
import subprocess
from urllib.parse import urlparse


class SubfinderError(Exception):
    pass


def extract_hostname(base_url: str) -> str:
    parsed = urlparse(base_url)

    hostname = parsed.hostname

    if not hostname:
        raise SubfinderError(
            f"Could not extract hostname from target URL: {base_url}"
        )

    return hostname


def run_subfinder(base_url: str) -> list[str]:
    """
    Run Subfinder against a target and return discovered hostnames.
    """

    subfinder_path = shutil.which("subfinder")

    if not subfinder_path:
        raise SubfinderError(
            "Subfinder executable was not found in PATH."
        )

    domain = extract_hostname(base_url)

    command = [
        subfinder_path,
        "-d",
        domain,
        "-silent",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )

    except subprocess.TimeoutExpired as exc:
        raise SubfinderError(
            "Subfinder scan timed out."
        ) from exc

    if result.returncode != 0:
        raise SubfinderError(
            result.stderr.strip()
            or "Subfinder exited with an error."
        )

    hosts = []

    for line in result.stdout.splitlines():
        hostname = line.strip().lower()

        if hostname:
            hosts.append(hostname)

    return sorted(set(hosts))