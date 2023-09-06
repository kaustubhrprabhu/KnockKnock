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

    def __init__(self, url:str, useThreads:bool) -> None:
        self.url = url
        self.useThreads = useThreads
        self.load_paths()
        self.print_banner()

    def print_banner(self):
        print(f"""{self.cred}
                                                  
        █▄▀ █▄░█ █▀█ █▀▀ █▄▀ █▄▀ █▄░█ █▀█ █▀▀ █▄▀
        █░█ █░▀█ █▄█ █▄▄ █░█ █░█ █░▀█ █▄█ █▄▄ █░█
        
        🔥 version 0.1 made by Kaustubh Prabhu 🔥
              
        {self.cend}""")
    
    def load_paths(self):
        try:
            with open('paths.txt', 'r') as file:
                self.paths = file.read().splitlines()
        except IOError:
            print(f'{self.cred} paths.txt file is missing!{self.cend}')
    
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
    
    def start(self):
        if self.useThreads:
            threads = []
            for path in self.paths:
                thread = threading.Thread(target=self.scan, args=(path,))
                threads.append(thread)
                thread.start()
            for t in threads:
                t.join()
        else:
            for path in self.paths:
                self.scan(path)
        print(f'\n\t{self.cyellowbg} Total found: {len(self.found)} {self.cend}\n')
        if self.found:
            for link in self.found:
                print(f'\t{self.cgreenbg} {link} {self.cend}')


if __name__ == '__main__':
    cend = '\33[0m'
    cred = '\33[91m'
    cgreen = '\33[92m'
    cyellow = '\33[93m'
    credbg = '\33[30;41m'
    cgreenbg = '\33[30;42m'
    cyellowbg = '\33[30;43m'

    parser = argparse.ArgumentParser(prog='knockknock')
    parser.add_argument('url', type=str, help='the base url to search for')
    parser.add_argument('-f', '--fast', help='uses multithreading', dest='fast', action='store_true')
    args = parser.parse_args()

    try:
        knockknock = KnockKnock(args.url, args.fast)
        knockknock.start()
    except KeyboardInterrupt:
        print(f'\n\t{cred}Session terminated{cend}\n\tThank you for using KnockKnock')
        sys.exit(1)
