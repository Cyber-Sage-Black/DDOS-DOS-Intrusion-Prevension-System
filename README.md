# DDOS-Prevention-IPS

# Windows Anti-DDoS Protection System

A lightweight and efficient Anti-DDoS system for Windows that uses Windows Firewall to protect against DDoS and brute force attacks. The system monitors network traffic in real-time and automatically blocks suspicious IP addresses.

## Features

- Real-time network traffic monitoring
- Automatic rate limiting
- Windows Firewall integration
- Automatic IP blocking and unblocking
- Clean shutdown and cleanup
- Detailed logging system

## Requirements

- Windows 10/11
- Python 3.7 or higher
- Administrator privileges
- Scapy package

## Installation

1. Install Python from [python.org](https://python.org) if not already installed

2. Install the required package:
```bash
pip install scapy
```

## Usage

1. Open Command Prompt as Administrator:
   - Right-click on Command Prompt
   - Select "Run as administrator"

2. Navigate to the script directory:
```bash
cd path/to/anti_ddos
```

3. Run the script:
```bash
python anti_ddos.py
```

## How It Works

The system:
1. Monitors incoming network traffic using Scapy
2. Tracks request rates per IP address
3. Automatically blocks IPs that exceed the rate limit using Windows Firewall
4. Unblocks IPs after the block duration expires
5. Cleans up all firewall rules on shutdown

## Configuration

You can modify these parameters in `anti_ddos.py`:

```python
self.RATE_LIMIT = 100      # Maximum requests per minute
self.BLOCK_DURATION = 300  # Block duration in seconds (5 minutes)
```

## Logging

The system logs all activities including:
- Blocked IP addresses
- Unblocked IP addresses
- Rate limit violations
- System status
- Error messages

## Security Notes

1. Always run as administrator
2. Keep Windows Firewall enabled
3. Monitor the logs regularly
4. Adjust rate limits based on your network traffic patterns

## Troubleshooting

1. "Access Denied" errors:
   - Make sure you're running as administrator
   - Check Windows Firewall is enabled

2. Import errors:
   - Verify Scapy is installed: `pip install scapy`

3. Network interface errors:
   - Check your network adapter settings
   - Verify Windows Firewall service is running

## License

This project is open source and available under the MIT License.

## Safety Warning

This tool modifies Windows Firewall rules. Use with caution and ensure you understand the implications of blocking IP addresses.
