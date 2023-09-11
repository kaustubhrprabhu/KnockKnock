# KnockKnock
KnockKnock is a Python script to find admin panel of a website. (Illegal use is strictly prohibited. Make sure you use this tool responsibly.)

## Features
- Multiplatform
- Multithreaded
- Random User-Agents
- Proxy
- Big path list

More features are coming soon

## Requirements
```bash
# Install requirements
$ pip3 install -r requirements.txt
```

## Usage
```bash
# Check all paths
$ python3 knockknock.py http://example.com

# Check all paths with threads
$ python3 knockknock.py http://example.com -f

# Check all paths with random user-agent
$ python3 knockknock.py http://example.com -r

# Use HTTP(S) or SOCKS(4/5) proxy
$ python3 knockknock.py http://example.com --proxy http://127.0.0.1:8080
# OR
$ python3 knockknock.py http://example.com --proxy socks5h://127.0.0.1:8080

# Help
$ python3 knockknock.py -h
```