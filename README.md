# Simple Chat Application

### Commands to run

```bash
python3 server.py
python3 client.py
python3 client.py
kajol (as username)
MSG hello!
/quit
```

### Example session
#### 1. server.py

```
kajol@hp-kajol-kashipuri:~/chat-app$ python3 server.py
Server running on localhost:12345. Press Ctrl+C to stop.
[+] kk joined from ('127.0.0.1', 38746)
[+] k2 joined from ('127.0.0.1', 49696)
[-] kk disconnected
[-] k2 disconnected
```
#### 2. client.py

```
kajol@hp-kajol-kashipuri:~/chat-app$ python3 client.py
Connected to localhost:12345
Enter username: SERVER Send: JOIN <username>
kk
SERVER Joined as 'kk'. Type /quit to exit.
SERVER kk has joined the chat.
SERVER k2 has joined the chat.
[10:23:32] k2: MSG k2!
MSG kk!
[10:23:42] kk: MSG kk!
/quit
Disconnected.



kajol@hp-kajol-kashipuri:~/chat-app$ python3 client.py
Connected to localhost:12345
Enter username: SERVER Send: JOIN <username>
k2
SERVER Joined as 'k2'. Type /quit to exit.
SERVER k2 has joined the chat.
MSG k2!
[10:23:32] k2: MSG k2!
[10:23:42] kk: MSG kk!
SERVER kk has left the chat.
^CDisconnected.

```