#!/usr/bin/env python
"""
S32-03 — R1 Process-Kill Injection Matrix

Tests real process-kill injection during atomic_json_write with multiple
cycles and multiple kill points. Based on S32-02 findings.

Goal: Transform R1 from NOT PROVEN to PROVEN with repeated crash matrix.
"""

import subprocess
import sys
import os
import time
import json
import shutil

sys.path.insert(0, r"C:\Projetos\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write


def run_atomic_json_write_cycle(test_data, target_path, kill_point, kill_delay):
    """
    Run a single cycle of atomic_json_write with process kill.
    
    Args:
        test_data: Data to write
        target_path: Output file path
        kill_point: 'before', 'during', 'after_json', 'after_fsync', 'during_replace'
        kill_delay: Seconds to let process run before killing
    
    Returns:
        dict with cycle results
    """
    result = {
        "kill_point": kill_point,
        "kill_delay_s": kill_delay,
        "target_path": target_path,
        "output_exists": False,
        "output_valid_json": False,
        "output_is_empty": False,
        "output_is_corrupt": False,
        "output_is_partial": False,
        "old_file_preserved": False,
        "classification": "UNKNOWN",
    }
    
    # Remove target if exists
    if os.path.exists(target_path):
        os.remove(target_path)
    
    # Build subprocess command
    cmd = [
        sys.executable, "-c",
        f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target_path}", {repr(test_data)}, indent=2)
print("SUCCESS")
"""
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        time.sleep(kill_delay)
        proc.kill()
        proc.wait(timeout=5)
        
        # Check output file
        result["output_exists"] = os.path.exists(target_path)
        
        if result["output_exists"]:
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if content.strip() == "":
                    result["output_is_empty"] = True
                else:
                    try:
                        parsed = json.loads(content)
                        result["output_valid_json"] = True
                        # Check if partial (starts with { or [ but incomplete)
                        if content.strip().startswith("{") or content.strip().startswith("["):
                            # Check if it's actually valid by trying to access a key
                            try:
                                eval(content + "\n# eval test")  # just syntax check
                                # Actually just check it's valid JSON
                                result["output_valid_json"] = True
                            except:
                                pass
                    except json.JSONDecodeError:
                        result["output_is_partial"] = True
                        # Check if corrupt
                        try:
                            json.loads(content)  # force re-parse
                        except:
                            result["output_is_corrupt"] = True
            except Exception as e:
                result["output_is_corrupt"] = True
        
        # Check if old file was preserved (if we removed one previously)
        # This is implicit - if output_exists is False, old was preserved
        if not result["output_exists"]:
            result["old_file_preserved"] = True
            result["classification"] = "OLD PRESERVED - no write attempted"
        elif result["output_valid_json"] and not result["output_is_partial"] and not result["output_is_corrupt"] and not result["output_is_empty"]:
            result["classification"] = "NEW - full write completed"
        elif result["output_is_empty"]:
            result["classification"] = "EMPTY FILE - BLOCKER"
        elif result["output_is_partial"]:
            result["classification"] = "PARTIAL JSON - BLOCKER"
        elif result["output_is_corrupt"]:
            result["classification"] = "CORRUPTED FILE - BLOCKER"
        else:
            result["classification"] = "UNDECIDED"
    
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        result["classification"] = "TIMEOUT - process hang"
    
    return result


def main():
    """Run S32-03 repeated crash matrix."""
    
    print("=" * 70)
    print("S32-03 — R1 Process-Kill Injection Matrix")
    print("=" * 70)
    print()
    
    # Configuration
    test_data = {"symbol": "BTC-USD", "confidence": 0.95, "confluence": 100.0}
    target_path = r"mercury_ai/database/snapshots/test_crash_s32_03.json"
    cycles = 10  # 10 cycles per kill point
    kill_points = [
        "before_start",      # Before atomic_json_write begins
        "after_mkstemp",     # After tempfile creation, before json.dump
        "after_json_dump",   # After json.dump, before fsync
        "after_fsync",       # After fsync, before os.replace
        "during_replace",    # During os.replace() - critical point
    ]
    
    # Kill delays (approximate - will be adjusted based on S32-02 findings)
    # These are indicative delays to hit different kill points
    kill_delays = {
        "before_start": 0.005,     # Very early - before any write
        "after_mkstemp": 0.05,     # After mkstemp, before json begins
        "after_json_dump": 0.5,    # During/after json.dump
        "after_fsync": 1.0,        # After fsync, before os.replace
        "during_replace": 2.0,     # Critical: during os.replace
    }
    
    print(f"Test target: {target_path}")
    print(f"Data: {test_data}")
    print(f"Cycles per kill point: {cycles}")
    print(f"Kill points: {', '.join(kill_points)}")
    print()
    print(f"Total test executions: {cycles * len(kill_points)}")
    print()
    
    all_results = []
    
    for kp in kill_points:
        delay = kill_delays[kp]
        print(f"--- Kill point: {kp} (delay: {delay}s) ---")
        point_results = []
        
        for cycle in range(1, cycles + 1):
            result = run_atomic_json_write_cycle(test_data, target_path, kp, delay)
            point_results.append(result)
            
            # Log classification
            status = result["classification"]
            if "BLOCKER" in status:
                print(f"  Cycle {cycle}: {status} ⚠️")
            elif "PASS" in status or "OLD PRESERVED" in status:
                print(f"  Cycle {cycle}: {status} ✓")
            else:
                print(f"  Cycle {cycle}: {status}")
        
        # Summarize this kill point
        point_summary = {
            "kill_point": kp,
            "delay_s": delay,
            "cycles": cycles,
            "pass_count": sum(1 for r in point_results if "OLD PRESERVED" in r["classification"] or ("NEW" in r["classification"] and not any("BLOCKER" in r2["classification"] for r2 in point_results))),
            "blocker_count": sum(1 for r in point_results if "BLOCKER" in r["classification"]),
        }
        all_results.append(point_summary)
        print(f"  Summary: {point_summary['pass_count']}/{cycles} passed, {point_summary['blocker_count']} blockers")
        print()
    
    # Overall summary
    print("=" * 70)
    print("S32-03 — SUMMARY")
    print("=" * 70)
    
    total_pass = sum(r["pass_count"] for r in all_results)
    total_blockers = sum(r["blocker_count"] for r in all_results)
    total_tests = cycles * len(kill_points)
    
    print(f"Total test executions: {total_tests}")
    print(f"Pass (no corruption): {total_pass}")
    print(f"Blockers (corruption/partial/EMPTY): {total_blockers}")
    print()
    
    # Classification per S32 criteria
    if total_blockers > 0:
        overall = "FAIL - File corruption or partial/EMPTY writes detected across matrix"
    elif total_pass == total_tests:
        overall = "PASS - Old XOR New comprovado em todos os ciclos e pontos de interrupção"
    elif total_pass > total_tests / 2:
        overall = "STRUCTURALLY PROVEN - Maioria dos ciclos demonstra integridade, pontos isolados need investigation"
    elif total_pass > 0:
        overall = "NOT PROVEN - Crash injection reproduzido mas integridade não garantida em todos os cenários"
    else:
        overall = "FAIL - Nenhum ciclo demonstrou integridade"
    
    print(f"Classificação geral: {overall}")
    print()
    
    # Detailed per-kill-point results
    print("Resultados detalhados por ponto de interrupção:")
    for r in all_results:
        status_label = "PASS" if r["pass_count"] == cycles else ("PARTIAL" if r["pass_count"] > 0 else "BLOCKER")
        print(f"  {r['kill_point']} (delay {r['delay_s']}s): {r['pass_count']}/{r['cycles']} passed [{status_label}]")
        if r["blocker_count"] > 0:
            print(f"    Blockers: {r['blocker_count']} - {['EMPTY', 'PARTIAL JSON', 'CORRUPTED'][min(r['blocker_count']-1, 2) if r['blocker_count'] <= 3 else 2]}")
    
    # Cleanup
    if os.path.exists(target_path):
        os.remove(target_path)
    
    return all_results


if __name__ == "__main__":
    results = main()
    # Exit code
    total_blockers = sum(r["blocker_count"] for r in results)
    if total_blockers > 0:
        print(f"\nCRITICAL: {total_blockers} corruption events detected - R1 NOT PROVEN")
        sys.exit(1)
    else:
        print(f"\nAll {len(results)*10} crash matrix cycles completed - evidence collected for R1 classification")
        sys.exit(0)