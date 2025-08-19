#!/usr/bin/env python3
"""
Core consolidation logic for network IP consolidation.
Handles basic CIDR consolidation and bias-based expansion.
"""

import ipaddress
import re
import os
from typing import List

def extract_host_ips(filename: str, chunk_size: int = 10000) -> List[str]:
    """Extract all IP addresses and CIDR networks from any file format using chunked processing."""
    host_ips = []
    # Pattern for individual IPs and CIDR networks
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:/[0-9]{1,2})?\b'
    
    # Get file size for progress estimation
    file_size = os.path.getsize(filename)
    processed_bytes = 0
    
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        chunk = []
        for line_num, line in enumerate(file, 1):
            chunk.append(line)
            processed_bytes += len(line.encode('utf-8'))
            
            # Process chunk when it reaches the specified size
            if len(chunk) >= chunk_size:
                host_ips.extend(process_chunk(chunk, ip_pattern))
                chunk = []
                
                # Optional: Log progress for very large files
                if file_size > 10 * 1024 * 1024:  # 10MB
                    progress = (processed_bytes / file_size) * 100
                    print(f"Processing progress: {progress:.1f}%")
        
        # Process remaining lines
        if chunk:
            host_ips.extend(process_chunk(chunk, ip_pattern))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_ips = []
    for ip in host_ips:
        if ip not in seen:
            seen.add(ip)
            unique_ips.append(ip)
    
    return unique_ips

def process_chunk(chunk: List[str], ip_pattern: str) -> List[str]:
    """Process a chunk of lines to extract IP addresses."""
    chunk_ips = []
    
    # Common subnet masks to exclude
    subnet_masks = {
        '0.0.0.0', '128.0.0.0', '192.0.0.0', '224.0.0.0', '240.0.0.0', '248.0.0.0', '252.0.0.0', '254.0.0.0', '255.0.0.0',
        '255.128.0.0', '255.192.0.0', '255.224.0.0', '255.240.0.0', '255.248.0.0', '255.252.0.0', '255.254.0.0', '255.255.0.0',
        '255.255.128.0', '255.255.192.0', '255.255.224.0', '255.255.240.0', '255.255.248.0', '255.255.252.0', '255.255.254.0', '255.255.255.0',
        '255.255.255.128', '255.255.255.192', '255.255.255.224', '255.255.255.240', '255.255.255.248', '255.255.255.252', '255.255.255.254', '255.255.255.255'
    }
    
    for line in chunk:
        line = line.strip()
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue
        
        # Find all IP addresses and CIDR networks in the line
        matches = re.findall(ip_pattern, line)
        for match in matches:
            try:
                if '/' in match:  # CIDR notation
                    network = ipaddress.IPv4Network(match, strict=False)
                    # Add all host IPs from the network (excluding network and broadcast)
                    for ip in network.hosts():
                        chunk_ips.append(str(ip))
                else:  # Individual IP
                    ip = ipaddress.IPv4Address(match)
                    ip_str = str(ip)
                    # Skip if it's a subnet mask
                    if ip_str not in subnet_masks:
                        chunk_ips.append(ip_str)
            except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError):
                continue
    
    return chunk_ips

def consolidate_networks(ip_list: List[str]) -> List[ipaddress.IPv4Network]:
	"""Collapse all host IPs into the smallest set of congruent CIDR networks."""
	host_networks = [ipaddress.IPv4Network(f"{ip}/32") for ip in ip_list]
	collapsed = list(ipaddress.collapse_addresses(host_networks))
	collapsed.sort(key=lambda n: (int(n.network_address), n.prefixlen))
	return collapsed

def consolidate_with_bias(ip_list: List[str], max_missing_percent: int = 25) -> List[ipaddress.IPv4Network]:
	"""Consolidate IPs with bias for missing addresses up to max_missing_percent."""
	ip_set = set(ipaddress.IPv4Address(ip) for ip in ip_list)
	basic_networks = consolidate_networks(ip_list)
	
	expanded_networks = []
	processed_ips = set()
	
	for net in basic_networks:
		if net.prefixlen == 32:
			expanded_networks.append(net)
			processed_ips.add(net.network_address)
			continue
			
		best_network = net
		current_net = net
		
		while current_net.prefixlen > 8:
			parent_net = current_net.supernet()
			parent_ips = set(parent_net.hosts())
			matching_ips = parent_ips & ip_set
			
			total_ips_in_parent = parent_net.num_addresses - 2
			covered_percent = (len(matching_ips) / total_ips_in_parent) * 100 if total_ips_in_parent > 0 else 0
			missing_percent = 100 - covered_percent
			
			if missing_percent <= max_missing_percent:
				best_network = parent_net
				current_net = parent_net
			else:
				break
		
		expanded_networks.append(best_network)
		
		if best_network.prefixlen == 32:
			processed_ips.add(best_network.network_address)
		else:
			processed_ips.update(best_network.hosts())
	
	# Remove duplicates and sort
	unique_networks = []
	seen_networks = set()
	
	for net in expanded_networks:
		net_key = (net.network_address, net.prefixlen)
		if net_key not in seen_networks:
			seen_networks.add(net_key)
			unique_networks.append(net)
	
	unique_networks.sort(key=lambda n: (int(n.network_address), n.prefixlen))
	return unique_networks
