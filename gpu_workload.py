"""
GPU/CPU Compute Harness — Auto-detects available hardware and runs repeatable workload.

Supports:
- NVIDIA CUDA (via CuPy)
- AMD ROCm (via PyTorch/TensorFlow)
- CPU fallback (via NumPy)

Returns consistent result type regardless of backend.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import cupy as cp
    HAS_CUDA = True
except ImportError:
    HAS_CUDA = False

try:
    import torch
    HAS_ROCM = torch.cuda.is_available() and torch.version.hip is not None
except ImportError:
    HAS_ROCM = False

import numpy as np


class GPUWorkload:
    """Compute harness with auto-detection and graceful fallback."""

    def __init__(self, matrix_size=512):
        self.matrix_size = matrix_size
        self.backend = self._detect_backend()

    def _detect_backend(self):
        """Detect available GPU/CPU backend."""
        if HAS_CUDA:
            return "cuda"
        elif HAS_ROCM:
            return "rocm"
        else:
            return "cpu"

    def run(self):
        """Execute matrix multiply workload, return result magnitude."""
        if self.backend == "cuda":
            return self._run_cuda()
        elif self.backend == "rocm":
            return self._run_rocm()
        else:
            return self._run_cpu()

    def _run_cuda(self):
        """NVIDIA CUDA compute via CuPy."""
        try:
            A = cp.random.randn(self.matrix_size, self.matrix_size, dtype=cp.float32)
            B = cp.random.randn(self.matrix_size, self.matrix_size, dtype=cp.float32)
            C = cp.matmul(A, B)
            result = float(cp.sum(cp.abs(C)))
            return result
        except Exception as e:
            # Graceful fallback to CPU
            return self._run_cpu()

    def _run_rocm(self):
        """AMD ROCm compute via PyTorch."""
        try:
            device = torch.device("cuda")  # ROCm uses CUDA APIs
            A = torch.randn(self.matrix_size, self.matrix_size, device=device, dtype=torch.float32)
            B = torch.randn(self.matrix_size, self.matrix_size, device=device, dtype=torch.float32)
            C = torch.matmul(A, B)
            result = float(torch.sum(torch.abs(C)))
            return result
        except Exception as e:
            # Graceful fallback to CPU
            return self._run_cpu()

    def _run_cpu(self):
        """CPU compute via NumPy."""
        A = np.random.randn(self.matrix_size, self.matrix_size).astype(np.float32)
        B = np.random.randn(self.matrix_size, self.matrix_size).astype(np.float32)
        C = np.matmul(A, B)
        result = float(np.sum(np.abs(C)))
        return result

    def get_backend_name(self):
        """Return human-readable backend name."""
        if self.backend == "cuda":
            return "NVIDIA CUDA (CuPy)"
        elif self.backend == "rocm":
            return "AMD ROCm (PyTorch)"
        else:
            return "CPU (NumPy)"


if __name__ == "__main__":
    # Quick test
    workload = GPUWorkload(matrix_size=256)
    print(f"Backend: {workload.get_backend_name()}")
    result = workload.run()
    print(f"Compute result: {result:.2e}")
