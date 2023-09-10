#!/usr/bin/env python3

import requests
import threading
import argparse
import sys
import random

class KnockKnock:
    cend = '\33[0m'
    cred = '\33[91m'
    cgreen = '\33[92m'
    cyellow = '\33[93m'
    credbg = '\33[30;41m'
    cgreenbg = '\33[30;42m'
    cyellowbg = '\33[30;43m'

    timeout = 5
    headers = None
    proxies = None

    print_lock_ = threading.Lock()
    paths = None
    agents = None
    total_found = 0
    total_scanned = 0

    def __init__(self, url:str, multithread:bool, random_agent:bool) -> None:
        self.get_paths()
        if random_agent:
            self.get_agents()
        self.url = self.validate_url(url)
        self.multithread = multithread
        self.random_agent = random_agent
    
    def get_agents(self):
        try:
            with open('user-agents.txt', 'r') as file:
                self.agents = file.read().splitlines()
        except IOError:
            print(f'{self.cred}user-agents.txt file is missing!{self.cend}')
            sys.exit(1)

    def validate_url(self, url):
        valid_url = url.removesuffix('/')
        if url[:4] != 'http':
            valid_url = 'http://' + url
        print(f'\n{self.cyellow}Verifying url, please wait...{self.cend}', end='')
        try:
            requests.get(valid_url)
        except requests.exceptions.RequestException:
            print(f'\x1b[1K\r{self.cred}Failed to validate:{self.cend} {valid_url}')
            print(f'\t╟═══ Check the url format')
            print(f'\t╟═══ Check whether url is valid')
            print(f'\t╚═══ Check your network connection')
            sys.exit(1)
        print(f'\x1b[1K\r{self.cgreen}Valid:{self.cend} {valid_url}\n')
        return valid_url
    
    def get_paths(self):
        try:
            with open('paths.txt', 'r') as file:
                self.paths = file.read().splitlines()
        except IOError:
            print(f'{self.cred} paths.txt file is missing!{self.cend}')
            sys.exit(1)
    
    def scan(self, path):
        full_url = self.url + path
        if self.random_agent:
            self.headers = {'user-agent': random.choice(self.agents)}
        sys.stdout.write(f'\x1b[1K\r{self.cyellow}Scanning:{self.cend} {path}')
        try:
            r = requests.get(full_url, timeout=self.timeout, headers=self.headers, proxies=self.proxies)
        except requests.exceptions.RequestException:
            with self.print_lock_:
                sys.stdout.write(f'\x1b[1K\r{self.cred}Unable to scan:{self.cend} {path}')
        else:
            self.total_scanned += 1
            if r.status_code == 200:
                self.total_found += 1
                with self.print_lock_:
                    sys.stdout.write(f'\x1b[1K\r{self.cgreen}[+] {self.cend}{full_url}\n')
            else:
                with self.print_lock_:
                    sys.stdout.write(f'\x1b[1K\r{self.cred}[-] {self.cend}{full_url}')

    def run_scan(self):
        print(f'{self.cgreen}Session started...{self.cend}\n')
        try:
            if self.multithread:
                threads = []
                for path in self.paths:
                    thread = threading.Thread(target=self.scan, args=(path,))
                    threads.append(thread)
                    thread.daemon = True
                    thread.start()
                for t in threads:
                    t.join()
            else:
                for path in self.paths:
                    self.scan(path)
            print(f'\n\n{self.cgreen}Session completed!{self.cend}')
            print(f'\t╟═══[📄] Total pages found: {self.total_found}')
            print(f'\t╚═══[📚] Total pages scanned: {self.total_scanned}')
        except KeyboardInterrupt:
            sys.stdout.write(f'\x1b[1K\r\n{self.cred}Session terminated!{self.cend}\n\x1b[1K\r')
            sys.exit(1)


if __name__ == '__main__':
    print('\33[91m' + '''
    
        █▄▀ █▄░█ █▀█ █▀▀ █▄▀ █▄▀ █▄░█ █▀█ █▀▀ █▄▀
        █░█ █░▀█ █▄█ █▄▄ █░█ █░█ █░▀█ █▄█ █▄▄ █░█

            🔥 v0.2.1 made by Kaustubh Prabhu 🔥
    [https://github.com/kaustubhrprabhu/KnockKnock.git]
          
    ''' + '\33[0m')

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='target url (eg. http://example.com)')
    parser.add_argument('-f', '--fast', help='use multithreads', dest='fast', action='store_true')
    parser.add_argument('-r', '--random-agent', help='use random user-agents', dest='ragent', action='store_true')
    args = parser.parse_args()

    knockknock = KnockKnock(args.url, args.fast, args.ragent)
    knockknock.run_scan()
