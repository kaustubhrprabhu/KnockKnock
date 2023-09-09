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

    print_lock_ = threading.Lock()
    paths = None
    agents = None
    found = []

    def __init__(self, url:str, random_agent:bool) -> None:
        self.url = self.validate_url(url)
        self.get_paths()
        self.random_agent = random_agent
        if random_agent:
            self.get_agents()
    
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
        return valid_url
    
    def get_paths(self):
        try:
            with open('paths.txt', 'r') as file:
                self.paths = file.read().splitlines()
        except IOError:
            print(f'{self.cred} paths.txt file is missing!{self.cend}')
            sys.exit(1)
    
    def scan(self, path, headers=None):
        full_url = self.url + path
        try:
            r = requests.get(full_url, timeout=5, headers=headers)
            if r.status_code == 200:
                self.found.append(full_url)
                with self.print_lock_:
                    return print(f'{self.cgreen}[+]{self.cend} {full_url}')
            with self.print_lock_:
                return print(f'{self.cred}[-]{self.cend} {full_url}')
        except requests.exceptions.RequestException:
            pass
    
    def run_single_thread(self):
        print(f'{self.cgreen}Session started...{self.cend}\n')
        header = None
        try:
            for path in self.paths:
                if self.random_agent:
                    header = {'user-agent': random.choice(self.agents)}
                self.scan(path, header)
        except KeyboardInterrupt:
            print(f'\n{self.cred}Session terminated{self.cend}')
    
    def run_multi_thread(self):
        print(f'{self.cgreen}Session started...{self.cend}\n')
        header = None
        threads = []
        for path in self.paths:
            try:
                if self.random_agent:
                    header = {'user-agent': random.choice(self.agents)}
                thread = threading.Thread(target=self.scan, args=(path, header))
                threads.append(thread)
                thread.start()
            except KeyboardInterrupt:
                print(f'\n{self.cred}Session is about to stop...{self.cend}\n')
                break
        for t in threads:
            try:
                t.join()
            except KeyboardInterrupt:
                print(f'\n{self.cred}Please wait...{self.cend}\n')
                pass
    
    def result(self):
        print(f'\n\t{self.cyellowbg} Total found: {len(self.found)} {self.cend}')
        if self.found:
            for url in self.found:
                print(f'\t{self.cgreen}{url}{self.cend}')


if __name__ == '__main__':
    print('\33[91m' + '''
    
        █▄▀ █▄░█ █▀█ █▀▀ █▄▀ █▄▀ █▄░█ █▀█ █▀▀ █▄▀
        █░█ █░▀█ █▄█ █▄▄ █░█ █░█ █░▀█ █▄█ █▄▄ █░█

            🔥 v0.2 made by Kaustubh Prabhu 🔥
    [https://github.com/kaustubhrprabhu/KnockKnock.git]
          
    ''' + '\33[0m')

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='target url (eg. http://example.com)')
    parser.add_argument('-f', '--fast', help='use multithreads', dest='fast', action='store_true')
    parser.add_argument('-r', '--random-agent', help='use random user-agents', dest='ragent', action='store_true')
    args = parser.parse_args()

    knockknock = KnockKnock(args.url, args.ragent)
    
    if args.fast:
        knockknock.run_multi_thread()
    else:
        knockknock.run_single_thread()
    
    knockknock.result()
