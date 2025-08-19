#!/usr/bin/env python3
"""
Analysis and optimization module for network consolidation.
Handles multi-threshold analysis, Pareto frontier computation, and scoring.
"""

import ipaddress
from typing import List, Dict, Tuple
from core_consolidation import consolidate_with_bias

def analyze_consolidation(host_ips: List[str], threshold: int) -> Dict:
	"""Analyze consolidation with a given threshold and return summary stats."""
	collapsed_networks = consolidate_with_bias(host_ips, max_missing_percent=threshold)
	
	original_ip_set = set(ipaddress.IPv4Address(ip) for ip in host_ips)
	final_ip_set = set()
	
	for net in collapsed_networks:
		if net.prefixlen == 32:
			final_ip_set.add(net.network_address)
		else:
			final_ip_set.update(net.hosts())
	
	missing_ips_included = final_ip_set - original_ip_set
	total_ips_in_final = len(final_ip_set)
	original_ips = len(original_ip_set)
	objects_defined_count = sum(1 for net in collapsed_networks if net.prefixlen != 32)
	
	return {
		'threshold': threshold,
		'objects_defined': objects_defined_count,
		'original_ips': original_ips,
		'total_ips_final': total_ips_in_final,
		'missing_ips_included': len(missing_ips_included),
		'expansion_percent': (len(missing_ips_included) / original_ips) * 100,
		'networks': collapsed_networks
	}

def pareto_front(results: List[Dict]) -> List[Dict]:
	"""Return the Pareto frontier minimizing (objects_defined, missing_ips_included)."""
	sorted_res = sorted(results, key=lambda r: (r['objects_defined'], r['missing_ips_included']))
	frontier = []
	best_missing = None
	for r in sorted_res:
		if best_missing is None or r['missing_ips_included'] < best_missing:
			frontier.append(r)
			best_missing = r['missing_ips_included']
	return frontier

def equal_weight_score(results: List[Dict]) -> List[Dict]:
	"""Compute normalized 0-1 scores for objects and missing, minimize avg score."""
	objs = [r['objects_defined'] for r in results]
	miss = [r['missing_ips_included'] for r in results]
	min_o, max_o = min(objs), max(objs)
	min_m, max_m = min(miss), max(miss)
	
	for r in results:
		obj_norm = (r['objects_defined'] - min_o) / (max_o - min_o) if max_o > min_o else 0
		mis_norm = (r['missing_ips_included'] - min_m) / (max_m - min_m) if max_m > min_m else 0
		r['score'] = (obj_norm + mis_norm) / 2.0
	return results

def run_consolidation_analysis(host_ips: List[str], thresholds: List[int] = None) -> Tuple[List[Dict], List[Dict]]:
	"""Run consolidation analysis across multiple thresholds and return results + Pareto frontier."""
	if thresholds is None:
		thresholds = [0, 10, 20, 25, 30, 35, 40, 45, 50]
	
	results = []
	total_thresholds = len(thresholds)
	
	print(f"Starting analysis of {len(host_ips)} IPs across {total_thresholds} thresholds...")
	
	for i, threshold in enumerate(thresholds, 1):
		# Progress indicator for large datasets
		if len(host_ips) > 10000:
			progress = (i / total_thresholds) * 100
			print(f"Processing threshold {threshold}% ({i}/{total_thresholds}) - {progress:.1f}% complete")
		
		result = analyze_consolidation(host_ips, threshold)
		results.append(result)
	
	results = equal_weight_score(results)
	frontier = pareto_front(results)
	
	print(f"Analysis complete. Found {len(frontier)} Pareto optimal solutions.")
	
	return results, frontier
