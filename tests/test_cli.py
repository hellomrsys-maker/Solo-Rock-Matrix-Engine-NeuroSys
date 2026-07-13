"""
Unit tests for SOLO ROCK CLI.
"""

import pytest
import os
import sys
import tempfile
from unittest.mock import patch, Mock, MagicMock
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solo_rock_cli
from config import SoloRockConfig, ConfigError


class TestCLIDiagnoseCommand:
    """Test diagnose subcommand."""

    def test_diagnose_no_issues(self, mock_psutil):
        """Test diagnose command on healthy system."""
        with patch('solo_rock_cli.DiagnosticsEngine') as mock_diag_class:
            mock_engine = Mock()
            mock_engine.run_diagnostics.return_value = []
            mock_diag_class.return_value = mock_engine

            args = Mock()
            args.config = None
            args.verbose = False

            result = solo_rock_cli.cmd_diagnose(args)

            # No issues: should return 0
            assert result == 0
            mock_engine.run_diagnostics.assert_called_once()

    def test_diagnose_with_issues(self, mock_psutil):
        """Test diagnose command detects issues."""
        with patch('solo_rock_cli.DiagnosticsEngine') as mock_diag_class:
            mock_engine = Mock()
            mock_engine.run_diagnostics.return_value = [
                {
                    'title': 'Test Issue',
                    'severity': 'high',
                    'description': 'Test description',
                }
            ]
            mock_diag_class.return_value = mock_engine

            args = Mock()
            args.config = None
            args.verbose = False

            result = solo_rock_cli.cmd_diagnose(args)

            # Issues found: should return 1
            assert result == 1

    def test_diagnose_with_config(self, temp_config_file, mock_psutil):
        """Test diagnose command with custom config."""
        with patch('solo_rock_cli.DiagnosticsEngine') as mock_diag_class:
            mock_engine = Mock()
            mock_engine.run_diagnostics.return_value = []
            mock_diag_class.return_value = mock_engine

            args = Mock()
            args.config = temp_config_file
            args.verbose = False

            result = solo_rock_cli.cmd_diagnose(args)

            # Should return 0 (no issues)
            assert result == 0
            # Should pass config to engine
            call_args = mock_diag_class.call_args
            assert call_args is not None

    def test_diagnose_invalid_config(self, mock_psutil):
        """Test diagnose with invalid config file."""
        args = Mock()
        args.config = '/nonexistent/config.yaml'
        args.verbose = False

        result = solo_rock_cli.cmd_diagnose(args)

        # Invalid config: should return 2
        assert result == 2

    def test_diagnose_verbose_flag(self, mock_psutil):
        """Test diagnose with verbose flag."""
        with patch('solo_rock_cli.DiagnosticsEngine') as mock_diag_class:
            mock_engine = Mock()
            mock_engine.run_diagnostics.return_value = []
            mock_diag_class.return_value = mock_engine

            args = Mock()
            args.config = None
            args.verbose = True

            result = solo_rock_cli.cmd_diagnose(args)

            assert result == 0
            # Verify verbose was passed
            call_kwargs = mock_engine.run_diagnostics.call_args[1]
            assert call_kwargs.get('verbose') == True


class TestCLIMonitorCommand:
    """Test monitor subcommand."""

    def test_monitor_basic(self, mock_psutil):
        """Test monitor command basic execution."""
        with patch('solo_rock_cli.LiveMonitor') as mock_monitor_class:
            mock_monitor = Mock()
            mock_monitor.run.return_value = None
            mock_monitor_class.return_value = mock_monitor

            args = Mock()
            args.config = None
            args.duration = 10
            args.interval = 2.0

            result = solo_rock_cli.cmd_monitor(args)

            assert result == 0
            mock_monitor.run.assert_called_once()

    def test_monitor_with_config(self, temp_config_file, mock_psutil):
        """Test monitor with custom config."""
        with patch('solo_rock_cli.LiveMonitor') as mock_monitor_class:
            mock_monitor = Mock()
            mock_monitor.run.return_value = None
            mock_monitor_class.return_value = mock_monitor

            args = Mock()
            args.config = temp_config_file
            args.duration = 5
            args.interval = 1.0

            result = solo_rock_cli.cmd_monitor(args)

            assert result == 0

    def test_monitor_keyboard_interrupt(self, mock_psutil):
        """Test monitor handles keyboard interrupt."""
        with patch('solo_rock_cli.LiveMonitor') as mock_monitor_class:
            mock_monitor = Mock()
            mock_monitor.run.side_effect = KeyboardInterrupt()
            mock_monitor_class.return_value = mock_monitor

            args = Mock()
            args.config = None
            args.duration = 10
            args.interval = 2.0

            result = solo_rock_cli.cmd_monitor(args)

            # Should handle gracefully and return 0
            assert result == 0

    def test_monitor_custom_duration(self, mock_psutil):
        """Test monitor with custom duration."""
        with patch('solo_rock_cli.LiveMonitor') as mock_monitor_class:
            mock_monitor = Mock()
            mock_monitor.run.return_value = None
            mock_monitor_class.return_value = mock_monitor

            args = Mock()
            args.config = None
            args.duration = 30
            args.interval = 1.5

            result = solo_rock_cli.cmd_monitor(args)

            # Verify duration was passed
            call_kwargs = mock_monitor_class.call_args[1]
            assert call_kwargs.get('duration_seconds') == 30


class TestCLIBenchmarkCommand:
    """Test benchmark subcommand."""

    def test_benchmark_basic(self, mock_psutil):
        """Test benchmark command basic execution."""
        with patch('solo_rock_cli.run_gpu_benchmark') as mock_benchmark:
            mock_benchmark.return_value = {
                'total_ticks': 10,
                'dispatch_reduction': 0.75,
            }

            args = Mock()
            args.ticks = 10
            args.workload_size = 512

            result = solo_rock_cli.cmd_benchmark(args)

            assert result == 0
            mock_benchmark.assert_called_once()

    def test_benchmark_custom_params(self, mock_psutil):
        """Test benchmark with custom parameters."""
        with patch('solo_rock_cli.run_gpu_benchmark') as mock_benchmark:
            mock_benchmark.return_value = {
                'total_ticks': 20,
                'dispatch_reduction': 0.70,
            }

            args = Mock()
            args.ticks = 20
            args.workload_size = 1024

            result = solo_rock_cli.cmd_benchmark(args)

            assert result == 0
            # Verify parameters passed
            call_kwargs = mock_benchmark.call_args[1]
            assert call_kwargs.get('ticks') == 20
            assert call_kwargs.get('workload_size') == 1024


class TestCLIReportCommand:
    """Test report subcommand."""

    def test_report_text_format(self, mock_psutil):
        """Test report command with text format."""
        with patch('solo_rock_cli.ReportGenerator') as mock_gen_class:
            mock_gen = Mock()
            mock_gen.generate.return_value = {'issues': []}
            mock_gen.to_text.return_value = "Report text"
            mock_gen_class.return_value = mock_gen

            args = Mock()
            args.format = 'text'
            args.output = None

            result = solo_rock_cli.cmd_report(args)

            assert result == 0

    def test_report_json_format(self, mock_psutil):
        """Test report command with JSON format."""
        with patch('solo_rock_cli.ReportGenerator') as mock_gen_class:
            mock_gen = Mock()
            mock_gen.generate.return_value = {'issues': []}
            mock_gen_class.return_value = mock_gen

            args = Mock()
            args.format = 'json'
            args.output = None

            result = solo_rock_cli.cmd_report(args)

            assert result == 0

    def test_report_html_format(self, mock_psutil, tmp_path):
        """Test report command with HTML format."""
        with patch('solo_rock_cli.ReportGenerator') as mock_gen_class:
            mock_gen = Mock()
            mock_gen.generate.return_value = {'issues': []}
            mock_gen.to_html.return_value = "<html>Report</html>"
            mock_gen_class.return_value = mock_gen

            output_file = str(tmp_path / "report.html")

            args = Mock()
            args.format = 'html'
            args.output = output_file

            result = solo_rock_cli.cmd_report(args)

            assert result == 0


class TestCLIArgumentParsing:
    """Test CLI argument parsing."""

    def test_main_with_no_args(self):
        """Test main function with no arguments."""
        with patch('sys.argv', ['solo_rock_cli.py']):
            result = solo_rock_cli.main()

            # No command: should print help
            assert result == 0

    def test_main_with_diagnose_command(self, mock_psutil):
        """Test main function dispatches to diagnose."""
        with patch('sys.argv', ['solo_rock_cli.py', 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.return_value = 0

                result = solo_rock_cli.main()

                assert result == 0
                mock_cmd.assert_called_once()

    def test_main_with_monitor_command(self, mock_psutil):
        """Test main function dispatches to monitor."""
        with patch('sys.argv', ['solo_rock_cli.py', 'monitor']):
            with patch('solo_rock_cli.cmd_monitor') as mock_cmd:
                mock_cmd.return_value = 0

                result = solo_rock_cli.main()

                assert result == 0
                mock_cmd.assert_called_once()

    def test_main_with_benchmark_command(self, mock_psutil):
        """Test main function dispatches to benchmark."""
        with patch('sys.argv', ['solo_rock_cli.py', 'benchmark']):
            with patch('solo_rock_cli.cmd_benchmark') as mock_cmd:
                mock_cmd.return_value = 0

                result = solo_rock_cli.main()

                assert result == 0
                mock_cmd.assert_called_once()

    def test_main_with_report_command(self, mock_psutil):
        """Test main function dispatches to report."""
        with patch('sys.argv', ['solo_rock_cli.py', 'report']):
            with patch('solo_rock_cli.cmd_report') as mock_cmd:
                mock_cmd.return_value = 0

                result = solo_rock_cli.main()

                assert result == 0
                mock_cmd.assert_called_once()

    def test_global_config_argument(self, temp_config_file, mock_psutil):
        """Test global --config argument."""
        with patch('sys.argv', ['solo_rock_cli.py', '--config', temp_config_file, 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.return_value = 0

                result = solo_rock_cli.main()

                # Should pass config to command
                call_args = mock_cmd.call_args[0][0]
                assert call_args.config == temp_config_file


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_config_error_handling(self, mock_psutil):
        """Test handling of configuration errors."""
        with patch('sys.argv', ['solo_rock_cli.py', '--config', '/invalid/path.yaml', 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.return_value = 2

                result = solo_rock_cli.main()

                # Should propagate error
                assert mock_cmd.called

    def test_command_exception_handling(self, mock_psutil):
        """Test handling of command exceptions."""
        with patch('sys.argv', ['solo_rock_cli.py', 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.side_effect = Exception("Test error")

                with pytest.raises(Exception):
                    solo_rock_cli.main()


class TestCLIExitCodes:
    """Test CLI exit codes."""

    def test_exit_code_0_on_success(self, mock_psutil):
        """Test exit code 0 on successful execution."""
        with patch('sys.argv', ['solo_rock_cli.py', 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.return_value = 0

                result = solo_rock_cli.main()
                assert result == 0

    def test_exit_code_1_on_issues(self, mock_psutil):
        """Test exit code 1 when issues detected."""
        with patch('sys.argv', ['solo_rock_cli.py', 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.return_value = 1

                result = solo_rock_cli.main()
                assert result == 1

    def test_exit_code_2_on_config_error(self, mock_psutil):
        """Test exit code 2 on configuration error."""
        with patch('sys.argv', ['solo_rock_cli.py', '--config', '/invalid.yaml', 'diagnose']):
            with patch('solo_rock_cli.cmd_diagnose') as mock_cmd:
                mock_cmd.return_value = 2

                result = solo_rock_cli.main()
                assert result == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
