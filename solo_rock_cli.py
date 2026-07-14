#!/usr/bin/env python3
"""
SOLO ROCK CLI — Production-grade command-line interface for the AI orchestrator.

Detects communication protocol issues (retry storms, queue buildup, thermal mismanagement),
measures dispatch reduction under load, and reports exactly what SOLO ROCK is controlling
and what issues it detected in real-time.

Usage:
    python solo_rock_cli.py diagnose      # Detect system communication issues
    python solo_rock_cli.py monitor       # Live telemetry + SOLO ROCK decisions
    python solo_rock_cli.py benchmark     # Run dispatch reduction benchmark
    python solo_rock_cli.py report        # Generate issue report + remediation
"""

import argparse
import sys
import os
import logging
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from diagnostics.core import DiagnosticsEngine
from monitor_realtime import LiveMonitor
from benchmark_gpu import run_gpu_benchmark, print_report
from report import ReportGenerator
from config import load_config, ConfigError

# Setup logging (quiet by default, verbose with --verbose flags)
logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] %(message)s',
    stream=sys.stderr
)


def cmd_diagnose(args):
    """Run system diagnostics to detect communication issues."""
    print("=" * 70)
    print("  SOLO ROCK DIAGNOSTICS — Detecting System Communication Issues")
    print("=" * 70)
    print()

    # Enable verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load config if provided
    config = None
    if hasattr(args, 'config') and args.config:
        try:
            config = load_config(args.config)
            print(f"[Config] Loaded thresholds from {args.config}\n")
        except ConfigError as e:
            print(f"[Error] Configuration failed: {e}", file=sys.stderr)
            print(f"[Hint] Check config file syntax and threshold ranges:", file=sys.stderr)
            print(f"  - thermal.warning_celsius: 0-100", file=sys.stderr)
            print(f"  - thermal.critical_celsius: > warning_celsius", file=sys.stderr)
            print(f"  - cpu.load_high_percent: 0-100", file=sys.stderr)
            print(f"  - ram.critical_percent: 0-100", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"[Error] Failed to load config: {e}", file=sys.stderr)
            if args.verbose:
                traceback.print_exc(file=sys.stderr)
            return 2

    try:
        engine = DiagnosticsEngine(config=config)
        issues = engine.run_diagnostics(verbose=args.verbose)
    except Exception as e:
        print(f"[Fatal Error] Diagnostics failed: {e}", file=sys.stderr)
        if args.verbose:
            traceback.print_exc(file=sys.stderr)
        return 2

    if not issues:
        print("✓ No critical communication issues detected.")
        print()
        print("SOLO ROCK is operating normally. The system has adequate")
        print("headroom and is not experiencing retry storms, thermal")
        print("mismanagement, or queue buildup.")
        return 0

    print(f"⚠ Found {len(issues)} issue(s):\n")
    critical_count = 0
    for i, issue in enumerate(issues, 1):
        severity_icon = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
        }.get(issue.get('severity', 'info'), 'ℹ️')

        if issue['severity'] == 'critical':
            critical_count += 1

        print(f"{i}. {severity_icon} {issue['title']}")
        print(f"   Severity: {issue['severity']}")
        print(f"   Details: {issue['description']}")
        if 'remediation' in issue:
            print(f"   Remediation: {issue['remediation']}")
        print()

    if critical_count > 0:
        print(f"⚠ {critical_count} critical issue(s) require immediate attention")
        return 1

    return 1


def cmd_monitor(args):
    """Live monitoring of telemetry + SOLO ROCK decisions + issues."""
    print("=" * 70)
    print("  SOLO ROCK LIVE MONITOR — Real-time Orchestration + Issue Detection")
    print("=" * 70)
    print()

    # Load config if provided
    config = None
    if hasattr(args, 'config') and args.config:
        try:
            config = load_config(args.config)
            print(f"[Config] Loaded thresholds from {args.config}\n")
        except ConfigError as e:
            print(f"[Error] Configuration failed: {e}", file=sys.stderr)
            print(f"[Hint] Check config file syntax at: {args.config}", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"[Error] Failed to load config: {e}", file=sys.stderr)
            return 2

    try:
        monitor = LiveMonitor(duration_seconds=args.duration, refresh_interval=args.interval, config=config)
        monitor.run()
        return 0
    except KeyboardInterrupt:
        print("\n[Monitor] Stopped by user.")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\n[Fatal Error] Monitor crashed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 2


def cmd_benchmark(args):
    """Run dispatch reduction benchmark with real compute workload."""
    print("=" * 70)
    print("  SOLO ROCK GPU BENCHMARK — Proving Dispatch Reduction Under Load")
    print("=" * 70)
    print()

    def on_tick(i, total, snapshot, action, reason, result):
        print(f"[{i+1}/{total}] cpu_load={snapshot['cpu_load']:.1f}% "
              f"cpu_temp={snapshot['cpu_temp']:.1f}C -> {action} | "
              f"compute_result={result:.2e}")

    try:
        results = run_gpu_benchmark(
            ticks=args.ticks,
            workload_size=args.workload_size,
            on_tick=on_tick
        )
        print()
        print_report(results)
        return 0
    except KeyboardInterrupt:
        print("\n[Benchmark] Stopped by user.")
        return 130
    except Exception as e:
        print(f"\n[Fatal Error] Benchmark failed: {e}", file=sys.stderr)
        print(f"[Hint] Try reducing --workload-size if memory is insufficient", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 2


def cmd_report(args):
    """Generate comprehensive issue report + remediation guide."""
    print("=" * 70)
    print("  SOLO ROCK ISSUE REPORT — Global Communication Gap Analysis")
    print("=" * 70)
    print()

    try:
        generator = ReportGenerator()
        report = generator.generate()

        if args.format == "json":
            import json
            print(json.dumps(report, indent=2))
        elif args.format == "html":
            html = generator.to_html(report)
            filename = args.output or "solo_rock_report.html"
            try:
                with open(filename, 'w') as f:
                    f.write(html)
                print(f"✓ Report saved to: {filename}")
            except IOError as e:
                print(f"[Error] Failed to write report to {filename}: {e}", file=sys.stderr)
                print(f"[Hint] Check disk space and file permissions", file=sys.stderr)
                return 2
        else:  # text/markdown
            print(generator.to_text(report))

        return 0
    except Exception as e:
        print(f"[Fatal Error] Report generation failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 2


def main():
    parser = argparse.ArgumentParser(
        description="SOLO ROCK — Production AI Hardware Orchestrator CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python solo_rock_cli.py diagnose                    # Detect communication issues
  python solo_rock_cli.py --config custom.yaml diagnose  # Use custom thresholds
  python solo_rock_cli.py monitor --duration 60       # Monitor for 60 seconds
  python solo_rock_cli.py benchmark --ticks 30        # Run 30-tick benchmark
  python solo_rock_cli.py report --format text        # Generate text report
        """
    )

    # Global arguments (before subcommands)
    parser.add_argument('--config', '-c', help='Path to YAML configuration file')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # diagnose subcommand
    diag = subparsers.add_parser('diagnose', help='Detect system communication issues')
    diag.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    diag.set_defaults(func=cmd_diagnose)

    # monitor subcommand
    mon = subparsers.add_parser('monitor', help='Live monitoring of orchestration + issues')
    mon.add_argument('--duration', type=int, default=60, help='Monitor duration (seconds)')
    mon.add_argument('--interval', type=float, default=2.0, help='Refresh interval (seconds)')
    mon.set_defaults(func=cmd_monitor)

    # benchmark subcommand
    bench = subparsers.add_parser('benchmark', help='Run dispatch reduction benchmark')
    bench.add_argument('--ticks', type=int, default=20, help='Number of compute iterations')
    bench.add_argument('--workload-size', type=int, default=512, help='GPU matrix size')
    bench.set_defaults(func=cmd_benchmark)

    # report subcommand
    rep = subparsers.add_parser('report', help='Generate issue report + remediation')
    rep.add_argument('--format', choices=['text', 'json', 'html'], default='text',
                     help='Output format')
    rep.add_argument('--output', '-o', help='Output file (for HTML)')
    rep.set_defaults(func=cmd_report)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[Interrupted] Stopped by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n[Fatal Error] Unexpected error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(255)
