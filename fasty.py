import socket

get_routes = {}

def get(route):
    def decorator(func):
        get_routes[route] = func
    return decorator

def fasty():
    print("------- FASTY 0.1 BETA -------")
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Waiting for connections on http://localhost:{PORT}/...")

        while 1:
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                while True:
                    data = conn.recv(2048)
                    if not data:
                        break

                    # Parse the HTTP message.
                    str_data = data.decode()
                    lines = str_data.split("\n")
                    cmd = lines[0].split()

                    method = cmd[0]
                    route = cmd[1]

                    print(f"Serving {method} '{route}'...")

                    if method == "GET":
                        # Snip off trailing slashes.
                        if len(route) > 1 and route.endswith("/"):
                            route = route[:-1]

                        # Look for the registered route and call it.
                        if route in get_routes:
                            route_func = get_routes[route]
                            result = route_func()
                            conn.sendall(f"HTTP/1.1 200 OK\r\n\r\n{result}".encode())
                        else:
                            conn.sendall(b"HTTP/1.1 404 Not Found")                           
                    else:
                        conn.sendall(b"HTTP/1.1 405 Method Not Allowed")

                    # Finish dealing with the client.
                    conn.close()
                    break