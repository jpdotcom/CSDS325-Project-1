# CSDS325-Project-1

# Echo Server - README

## Program Environment (as used in my setup)

- **Python Version**: Python 3.12.3
- **Linux Kernel**: 2.6 or higher (epoll was introduced in version 2.5.44, my device has 6.8)
- **Library Dependencies**: None as it uses standard Python Libraries
  - `socket`
  - `select`
  - `sys`

**Platform**: Linux only (epoll is Linux-specific). Use kqueue for MacOS

## Running the Server

```bash
python3 echo_server.py
```

**No command line arguments.** Following contants can be modified 
- `ECHO_PORT = 9999` - Port number
- `BUF_SIZE = 4096` - Buffer size in bytes


### Checker script to verify echo_server.py
```bash
python3 checker.py <ip> <port> <trials> <writes_per_trial> <max_bytes> <connections>
```

Example (as provided in PDF):
```bash
python3 checker.py localhost 9999 10 100 10000 100
```

