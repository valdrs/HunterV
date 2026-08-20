import shutil
import subprocess
from urllib.parse import urlparse


class SubfinderError(Exception):
    pass


def extract_hostname(base_url: str) -> str:
    """
    Extract a clean hostname from either a full URL or a bare domain.
    """

    value = base_url.strip()

    if not value:
        raise SubfinderError(
            "Target URL cannot be empty."
        )

    # urlparse treats "example.com" as a path,
    # so add a scheme when one is missing.
    if "://" not in value:
        value = f"https://{value}"

    parsed = urlparse(value)

    hostname = parsed.hostname

    if not hostname:
        raise SubfinderError(
            f"Could not extract hostname from target URL: {base_url}"
        )

    return hostname.lower().rstrip(".")


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
        "subfinder",
        "-d",
        domain,
        "-silent",
        "-timeout",
        "10",
        "-max-time",
        "2",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
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