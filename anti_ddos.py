import time
from collections import defaultdict
import subprocess
from scapy.all import sniff, IP, TCP
import logging
import os
import ctypes

class AntiDDoS:
    def __init__(self):
        # Configuration
        self.RATE_LIMIT = 100  # Maximum requests per minute
        self.BLOCK_DURATION = 300  # Block for 5 minutes
        self.RULE_NAME_PREFIX = "AntiDDoS_Block_"
        
        # Initialize counters and blocked IPs
        self.ip_counters = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})
        self.blocked_ips = {}  # IP: unblock_time
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _block_ip(self, ip):
        """Block an IP using Windows Firewall"""
        if ip in self.blocked_ips:
            return
            
        try:
            rule_name = f"{self.RULE_NAME_PREFIX}{ip.replace('.', '_')}"
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
            subprocess.run(cmd, shell=True, check=True)
            self.blocked_ips[ip] = time.time() + self.BLOCK_DURATION
            logging.info(f"Blocked IP: {ip}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to block IP {ip}: {e}")
            
    def _unblock_ip(self, ip):
        """Unblock an IP using Windows Firewall"""
        try:
            rule_name = f"{self.RULE_NAME_PREFIX}{ip.replace('.', '_')}"
            cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
            subprocess.run(cmd, shell=True, check=True)
            del self.blocked_ips[ip]
            logging.info(f"Unblocked IP: {ip}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to unblock IP {ip}: {e}")
            
    def _check_blocked_ips(self):
        """Check and unblock IPs that have served their block duration"""
        current_time = time.time()
        for ip, unblock_time in list(self.blocked_ips.items()):
            if current_time >= unblock_time:
                self._unblock_ip(ip)
                
    def _packet_callback(self, packet):
        """Process each packet"""
        if IP in packet:
            ip_src = packet[IP].src
            
            # Skip if it's localhost
            if ip_src == "127.0.0.1":
                return
                
            # Check if IP is already blocked
            if ip_src in self.blocked_ips:
                return
                
            current_time = time.time()
            
            # Reset counter if minute has passed
            if current_time - self.ip_counters[ip_src]['last_reset'] >= 60:
                self.ip_counters[ip_src] = {'count': 0, 'last_reset': current_time}
                
            # Increment counter
            self.ip_counters[ip_src]['count'] += 1
            
            # Check rate limit
            if self.ip_counters[ip_src]['count'] > self.RATE_LIMIT:
                self._block_ip(ip_src)
                logging.warning(f"Rate limit exceeded for IP: {ip_src}")
                
            # Periodically check blocked IPs
            if current_time % 10 < 1:  # Check every ~10 seconds
                self._check_blocked_ips()

    def _is_admin(self):
        """Check if the script is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _cleanup_rules(self):
        """Clean up all firewall rules created by this script"""
        try:
            cmd = f'netsh advfirewall firewall show rule name="{self.RULE_NAME_PREFIX}*"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "No rules match the specified criteria." not in result.stdout:
                cmd = f'netsh advfirewall firewall delete rule name="{self.RULE_NAME_PREFIX}*"'
                subprocess.run(cmd, shell=True, check=True)
                logging.info("Cleaned up all firewall rules")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error cleaning up firewall rules: {e}")
                
    def start(self):
        """Start monitoring network traffic"""
        try:
            # Check if running with sufficient privileges
            if not self._is_admin():
                logging.error("This program must be run as administrator!")
                return
                
            logging.info("Starting Anti-DDoS monitoring...")
            
            # Clean up any existing rules from previous runs
            self._cleanup_rules()
            
            # Start packet sniffing
            sniff(prn=self._packet_callback, store=0)
            
        except KeyboardInterrupt:
            logging.info("Stopping Anti-DDoS monitoring...")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        finally:
            # Clean up firewall rules
            self._cleanup_rules()
            logging.info("Monitoring stopped")

if __name__ == "__main__":
    anti_ddos = AntiDDoS()
    anti_ddos.start()