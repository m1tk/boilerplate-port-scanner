import socket

from common_ports import ports_and_services

TIMEOUT = 5.0

def get_open_ports(target, port_range, verbose = False):
    if verbose:
        open_ports = ""
    else:
        open_ports = []

    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        if verbose:
            open_ports += "Open ports for {} ({})\nPORT\tSERVICE\n"\
                .format(target, sock.getpeername()[0])

        try:
            sock.connect((target, port))
            if verbose:
                open_ports += "{}\t{}\n"\
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