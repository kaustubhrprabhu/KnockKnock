#!/usr/bin/env python3

import requests
import threading
import argparse
import sys

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
    found = []

    def __init__(self, url:str) -> None:
        self.url = self.validate_url(url)
        self.load_paths()

    def validate_url(self, url):
        valid_url = url.removesuffix('/')
        if url[:4] != 'http':
            valid_url = 'http://' + url
        return valid_url
    
    def load_paths(self):
        try:
            with open('paths.txt', 'r') as file:
                self.paths = file.read().splitlines()
        except IOError:
            print(f'{self.cred} paths.txt file is missing!{self.cend}')
            sys.exit(1)
    
    def scan(self, path):
        full_url = self.url + path
        try:
            r = requests.get(full_url, timeout=5)
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
        for path in self.paths:
            try:
                self.scan(path)
            except KeyboardInterrupt:
                print(f'\n{self.cred}Session terminated{self.cend}')
                break
    
    def run_multi_thread(self):
        print(f'{self.cgreen}Session started...{self.cend}\n')
        threads = []
        for path in self.paths:
            thread = threading.Thread(target=self.scan, args=(path,))
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
    
    def result(self):
        print(f'\n\t{self.cyellowbg} Total found: {len(self.found)} {self.cend}')
        if self.found:
            for url in self.found:
                print(f'\t{self.cgreen}{url}{self.cend}')


if __name__ == '__main__':
    print('\33[91m' + '''
    
        █▄▀ █▄░█ █▀█ █▀▀ █▄▀ █▄▀ █▄░█ █▀█ █▀▀ █▄▀
        █░█ █░▀█ █▄█ █▄▄ █░█ █░█ █░▀█ █▄█ █▄▄ █░█

        🔥 v0.1.1 made by Kaustubh Prabhu 🔥
          
    ''' + '\33[0m')

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='the base url to search for')
    parser.add_argument('-f', '--fast', help='uses multithreading', dest='fast', action='store_true')
    args = parser.parse_args()

    knockknock = KnockKnock(args.url)
    
    if args.fast:
        knockknock.run_multi_thread()
    else:
        knockknock.run_single_thread()
    
    knockknock.result()
