import httpx


class HTTPProbeError(Exception):
    pass


def probe_host(
    hostname: str,
    protocol: str,
    port: int,
    timeout: float = 5.0,
) -> dict | None:
    """
    Probe a single hostname and return HTTP asset information.

    Returns None when the host cannot be reached.
    """

    url = f"{protocol}://{hostname}:{port}"

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
        ) as client:

            response = client.get(url)

            return {
                "hostname": hostname,
                "protocol": protocol,
                "port": port,
                "status": str(response.status_code),
                "source": "httpx",
            }

    except httpx.RequestError:
        return None