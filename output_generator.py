#!/usr/bin/env python3
"""
Output generation module for network consolidation.
Handles network configuration generation, file writing, and console output.
"""

import ipaddress
from typing import List, Dict, Tuple

def make_object_name(network_str: str) -> str:
	"""Generate a simple object name using the base IP address with dots."""
	network = ipaddress.IPv4Network(network_str, strict=False)
	return str(network.network_address)

def generate_asa_output(networks: List[str], threshold: int) -> Tuple[List[str], List[str]]:
	"""Generate ASA object definitions and group references."""
	object_definitions_lines = []
	group_reference_lines = []
	
	for network_str in networks:
		network = ipaddress.IPv4Network(network_str, strict=False)
		obj_name = make_object_name(network_str)
		if network.prefixlen == 32:
			group_reference_lines.append(f"network-object host {network.network_address}")
		else:
			object_definitions_lines.append(f"object network {obj_name}")
			object_definitions_lines.append(f" subnet {network.network_address} {network.netmask}")
			group_reference_lines.append(f"network-object object {obj_name}")
	
	return object_definitions_lines, group_reference_lines

def write_asa_file(object_lines: List[str], group_lines: List[str], threshold: int, filename: str = "asa_objects_and_list.txt"):
	"""Write network configuration to file."""
	with open(filename, 'w') as f:
		f.write(f"! Generated with {threshold}% missing threshold\n")
		f.write("! === Object definitions ===\n")
		for line in object_lines:
			f.write(line + "\n")
		f.write("\n! === Group member list ===\n")
		for line in group_lines:
			f.write(line + "\n")



def print_analysis_summary(results: List[Dict], frontier: List[Dict], recommended: Dict):
	"""Print formatted analysis summary to console."""
	print("\n" + "="*80)
	print("CONSOLIDATION ANALYSIS SUMMARY")
	print("="*80)
	print(f"{'Threshold':<10} {'Objects':<8} {'Missing':<8} {'Score':<8} {'Expansion%':<10}")
	print("-"*80)
	
	for r in results:
		print(f"{r['threshold']:<10} {r['objects_defined']:<8} {r['missing_ips_included']:<8} {r['score']:<8.3f} {r['expansion_percent']:<10.1f}")
	
	print("\nPareto frontier (best trade-offs):")
	for r in frontier:
		print(f" - {r['threshold']}%: objects={r['objects_defined']}, missing={r['missing_ips_included']}, score={r['score']:.3f}")
	
	print("\n" + "="*80)
	print(f"RECOMMENDED THRESHOLD: {recommended['threshold']}% (best trade-off)")
	print(f"Objects: {recommended['objects_defined']}, Missing added: {recommended['missing_ips_included']}")
	print(f"Score: {recommended['score']:.3f}, Expansion: {recommended['expansion_percent']:.1f}%")
	print("="*80)
