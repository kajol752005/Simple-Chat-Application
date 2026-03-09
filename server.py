import socket
import threading
import datetime

HOST = "localhost"
PORT = 12345
BUFFER_SIZE = 1024

clients = {}
clients_lock = threading.Lock()

def broadcast(message):
    with clients_lock:
        targets = list(clients.keys())
    for sock in targets:
        try:
            sock.sendall((message + "\n").encode("utf-8"))
        except:
            pass

def handle_client(conn, addr):
    username = None
    buffer = ""
    try:
        conn.sendall(b"SERVER Send: JOIN <username>\n")
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                return
            buffer += data.decode("utf-8")
            if "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                break

        if not line.startswith("JOIN "):
            conn.sendall(b"SERVER ERROR: First message must be JOIN <username>\n")
            return

        username = line[5:].strip()
        if not username:
            conn.sendall(b"SERVER ERROR: Username cannot be empty\n")
            return

        with clients_lock:
            if username in clients.values():
                conn.sendall(b"SERVER ERROR: Username already taken\n")
                return
            clients[conn] = username

        conn.sendall(f"SERVER Joined as '{username}'. Type /quit to exit.\n".encode())
        broadcast(f"SERVER {username} has joined the chat.")
        print(f"[+] {username} joined from {addr}")

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            buffer += data.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                if line == "QUIT":
                    conn.sendall(b"SERVER Goodbye!\n")
                    return
                elif line.startswith("MSG "):
                    text = line[4:].strip()
                    if not text:
                        continue
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    broadcast(f"[{timestamp}] {username}: {text}")
                else:
                    conn.sendall(b"SERVER ERROR: Unknown command\n")
    except:
        pass
    finally:
        with clients_lock:
            if conn in clients:
                del clients[conn]
        conn.close()
        if username:
            broadcast(f"SERVER {username} has left the chat.")
            print(f"[-] {username} disconnected")

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Server running on {HOST}:{PORT}. Press Ctrl+C to stop.")
    try:
        while True:
            conn, addr = server_sock.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()