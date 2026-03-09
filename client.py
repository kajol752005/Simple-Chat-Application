import socket
import threading

HOST = "localhost"
PORT = 12345
BUFFER_SIZE = 1024

stop = threading.Event()

def receive_loop(sock):
    buffer = ""
    try:
        while not stop.is_set():
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("\n[Disconnected from server]")
                stop.set()
                break
            buffer += data.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(line.strip())
    except:
        stop.set()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    recv_thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    recv_thread.start()

    username = input("Enter username: ").strip()
    sock.sendall(f"JOIN {username}\n".encode())

    try:
        while not stop.is_set():
            text = input()
            if text == "/quit":
                sock.sendall(b"QUIT\n")
                break
            if text:
                sock.sendall(f"MSG {text}\n".encode())
    except KeyboardInterrupt:
        sock.sendall(b"QUIT\n")

    stop.set()
    sock.close()
    print("Disconnected.")

if __name__ == "__main__":
    main()