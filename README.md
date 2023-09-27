# KnockKnock

![GitHub release (with filter)](https://img.shields.io/github/v/release/kaustubhrprabhu/KnockKnock?style=flat-square&color=green)
![Static Badge](https://img.shields.io/badge/python-3-blue?style=flat-square)


**KnockKnock is a Python script to find admin panel of a website**

> [!WARNING]
> This tool is only for educational purpose, developer is not responsible for any misuse or illegal activities.


## Features

- Fast (Multithreaded)
- Random user-agents
- Proxy
- Big path list


## Requirements

1. Make sure you have python3 and pip3 installed on your device.

2. Install the requirements:

    ```sh
    pip3 install -r requirements.txt
    ```


## Usage

Start the scan:

```sh
python3 knockknock.py http://example.com
```

## Options

- `-f` or `--fast` to enable multithreads:

    ```sh
    python3 knockknock.py http://example.com --fast
    ```

- `-r` or `--random-agent` to enable random user-agents:

    ```sh
    python3 knockknock.py http://example.com --random-agent
    ```

- `-p` or `--proxy` to use HTTP(s) or SOCKS(4/5) proxy:

    ```sh
    python3 knockknock.py http://example.com --proxy http://127.0.0.1:8080
    ```

    or

    ```sh
    python3 knockknock.py http://example.com --proxy socks5://127.0.0.1:8080
    ```


## License

[MIT](LICENSE) © [Kaustubh Prabhu](https://github.com/kaustubhrprabhu)
