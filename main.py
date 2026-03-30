import sys
import re

def run_log_audit(file_path):
    """
    Analyzes a server log file to extract errors, logins, and unique IP addresses.
    Demonstrates: File I/O, Regex, and Set data structures.
    """
    print(f"--- Starting Audit for: {file_path} ---")
    
    # Using a set for IPs ensures we only count unique visitors (O(1) lookup)
    unique_ips = set()
    metrics = {"errors": 0, "logins": 0, "total_lines": 0}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                metrics["total_lines"] += 1
                
                # 1. Identify Errors/Failures
                if any(word in line.upper() for word in ["ERROR", "FAILED", "CRITICAL"]):
                    metrics["errors"] += 1
                
                # 2. Identify Successful Connections
                if any(word in line.lower() for word in ["logged in", "connected", "authorized"]):
                    metrics["logins"] += 1
                
                # 3. Extract IP Addresses using Regex
                # Pattern matches standard IPv4 format (e.g., 192.168.1.1)
                found_ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                for ip in found_ips:
                    unique_ips.add(ip)

        # Output Results to CLI
        print(f"Analysis Complete.")
        print(f"Total Lines Scanned: {metrics['total_lines']}")
        print(f"System Errors Found: {metrics['errors']}")
        print(f"Successful Logins:   {metrics['logins']}")
        print(f"Unique IP Addresses: {len(unique_ips)}")
        print("---------------------------------")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)

if __name__ == "__main__":
    # Check if a filename was provided in the terminal
    if len(sys.argv) > 1:
        run_log_audit(sys.argv[1])
    else:
        print("Usage: python main.py <logfile_name>")