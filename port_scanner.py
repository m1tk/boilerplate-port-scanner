import socket
import ipaddress
import re

from common_ports import ports_and_services

TIMEOUT = 2.0

def resolve_target(target):
    if re.match(r'^(?:\d{1,3}\.){3}\d{1,3}$', target) is not None:
        try:
            ip = str(ipaddress.ip_address(target))
            try:
                domains = socket.gethostbyaddr(ip)
                return (ip, domains[0] if domains.count != 0 else None)
            except Exception:
                return (ip, None)
        except Exception:
            raise Exception("Error: Invalid IP address")
    else:
        try:
            return socket.gethostbyname(target)
        except Exception:
            raise Exception("Error: Invalid hostname")

def get_open_ports(target, port_range, verbose = False):
    if verbose:
        open_ports = ""
    else:
        open_ports = []
    try:
        ip = resolve_target(target)
    except Exception as e:
        return str(e)
    if isinstance(ip, tuple):
        target = ip[1]
        ip     = ip[0]
    if verbose:
        print("rgegeger", target, ip)
        open_ports += "Open ports for {}\n{:<7}  SERVICE"\
            .format(
                f"{target} ({ip})" if target is not None else f"{ip}",
                "PORT"
                )

    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        try:
            sock.connect((ip, port))
            if verbose:
                open_ports += "\n{:<7}  {}"\
                    .format(
                        port,
                        ports_and_services.get(port, "Unknown")
                    )
            else:
                open_ports.append(port)
        except Exception as e:
            continue
        finally:
            sock.close()


    return(open_ports)