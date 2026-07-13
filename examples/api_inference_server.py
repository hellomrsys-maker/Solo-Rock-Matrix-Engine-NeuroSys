"""
Integration Example: API Inference Server with SOLO ROCK

Shows how to use SOLO ROCK to detect server load and adapt request handling:
- FULL_RATE: serve immediately
- BATCH: queue requests for batched inference (lower latency variance)
- THROTTLE: queue requests, serve less frequently
- EMERGENCY: reject requests, return 503 Service Unavailable

This prevents retry storms from clients retrying on timeout.
Adapt the Flask code to your inference framework (FastAPI, Django, etc.)
"""

import time
import sys
import os
from collections import deque
from threading import Thread, Event

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from central_command.central_ai import CentralAI
from central_command.decision_engine import FULL_RATE, BATCH, THROTTLE, EMERGENCY


class InferenceServer:
    """API inference server that adapts to hardware load via SOLO ROCK."""

    def __init__(self, model, max_batch_size=32):
        self.model = model
        self.max_batch_size = max_batch_size
        self.ceo = CentralAI()
        self.request_queue = deque()
        self.running = True
        self.batch_thread = Thread(target=self._batch_processor, daemon=True)
        self.batch_thread.start()
        self.stats = {
            "requests_served": 0,
            "requests_queued": 0,
            "requests_rejected": 0,
            "decisions": {FULL_RATE: 0, BATCH: 0, THROTTLE: 0, EMERGENCY: 0}
        }

    def _batch_processor(self):
        """Background thread that processes queued requests in batches."""
        while self.running:
            if self.request_queue:
                # Process batches based on accumulated requests
                batch_size = min(len(self.request_queue), self.max_batch_size)
                batch = [self.request_queue.popleft() for _ in range(batch_size)]

                # Run inference on batch
                for req in batch:
                    try:
                        result = self._run_inference(req["data"])
                        req["result"] = result
                        req["status"] = "complete"
                    except Exception as e:
                        req["error"] = str(e)
                        req["status"] = "error"

            time.sleep(0.01)  # Small sleep to prevent busy-waiting

    def handle_inference_request(self, request_data):
        """Handle incoming inference request.

        Args:
            request_data: Input data for inference

        Returns:
            dict with {"result": output, "latency_ms": ms, "status": "served" | "queued" | "rejected"}
        """
        start_time = time.time()

        # **KEY:** Get SOLO ROCK recommendation
        action, reason, snapshot = self.ceo.tick()
        self.stats["decisions"][action] += 1

        cpu_temp = snapshot.get('cpu_temp', 0.0)
        cpu_load = snapshot.get('cpu_load', 0.0)

        # **DECISION TREE:** Adapt request handling based on hardware state
        if action == FULL_RATE:
            # Server has headroom: serve immediately
            try:
                result = self._run_inference(request_data)
                latency = (time.time() - start_time) * 1000
                self.stats["requests_served"] += 1

                return {
                    "status": "served",
                    "result": result,
                    "latency_ms": latency,
                    "decision": action,
                    "reason": reason,
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e),
                    "decision": action,
                }

        elif action == BATCH:
            # Moderate load: queue for batched inference (4-8 requests per batch)
            req_entry = {
                "data": request_data,
                "status": "queued",
                "result": None,
                "submitted_at": time.time(),
            }
            self.request_queue.append(req_entry)
            self.stats["requests_queued"] += 1

            # Wait for processing (with timeout)
            max_wait = 0.5  # 500ms max wait for batch
            deadline = time.time() + max_wait
            while req_entry["status"] == "queued" and time.time() < deadline:
                time.sleep(0.01)

            latency = (time.time() - start_time) * 1000

            if req_entry["status"] == "complete":
                return {
                    "status": "served",
                    "result": req_entry["result"],
                    "latency_ms": latency,
                    "decision": action,
                    "reason": f"Batched (queue_depth={len(self.request_queue)})",
                }
            else:
                return {
                    "status": "timeout",
                    "message": f"Request queued but not processed within {max_wait}s",
                    "decision": action,
                }

        elif action == THROTTLE:
            # High load: queue but serve less frequently (only large batches)
            req_entry = {
                "data": request_data,
                "status": "queued",
                "result": None,
                "submitted_at": time.time(),
            }
            self.request_queue.append(req_entry)
            self.stats["requests_queued"] += 1

            # Wait longer for batch to fill
            max_wait = 1.0  # 1000ms max wait
            deadline = time.time() + max_wait
            while req_entry["status"] == "queued" and time.time() < deadline:
                time.sleep(0.02)

            latency = (time.time() - start_time) * 1000

            if req_entry["status"] == "complete":
                return {
                    "status": "served",
                    "result": req_entry["result"],
                    "latency_ms": latency,
                    "decision": action,
                    "reason": f"Throttled, batched (temp={cpu_temp:.1f}C)",
                }
            else:
                return {
                    "status": "timeout",
                    "message": f"Server throttled, request timed out",
                    "retry_after": 2,
                    "decision": action,
                }

        elif action == EMERGENCY:
            # Critical thermal/power: reject with backoff signal
            self.stats["requests_rejected"] += 1

            return {
                "status": "service_unavailable",
                "error": "Server in emergency thermal state",
                "retry_after": 5,
                "decision": action,
                "reason": reason,
            }

    def _run_inference(self, request_data):
        """Run inference on request. Placeholder."""
        # In real code: output = self.model(request_data)
        import random
        time.sleep(0.01)  # Simulate compute time
        return {"prediction": random.random(), "confidence": random.random()}

    def get_stats(self):
        """Return server statistics."""
        return {
            "requests_served": self.stats["requests_served"],
            "requests_queued": self.stats["requests_queued"],
            "requests_rejected": self.stats["requests_rejected"],
            "decisions": self.stats["decisions"],
            "current_queue_depth": len(self.request_queue),
        }

    def shutdown(self):
        """Gracefully shutdown server."""
        self.running = False
        self.batch_thread.join()


# Example usage with Flask
if __name__ == "__main__":
    # This example simulates the server behavior without actually running Flask

    class DummyModel:
        def __call__(self, data):
            return {"output": 0.5}

    # Initialize server
    model = DummyModel()
    server = InferenceServer(model, max_batch_size=8)

    print("=" * 80)
    print("API INFERENCE SERVER WITH SOLO ROCK BACKPRESSURE")
    print("=" * 80)
    print()

    # Simulate incoming requests
    print("Simulating 50 inference requests...")
    print()

    request_results = []
    for i in range(50):
        response = server.handle_inference_request({"input": i})
        request_results.append(response)

        if (i + 1) % 10 == 0:
            stats = server.get_stats()
            print(f"[Request {i+1:>2}] Status: {response['status']:<15} "
                  f"Decision: {response.get('decision', 'N/A'):<10} "
                  f"Latency: {response.get('latency_ms', 'N/A'):>6.1f}ms")
            print(f"  Server: served={stats['requests_served']}, "
                  f"queued={stats['requests_queued']}, "
                  f"rejected={stats['requests_rejected']}, "
                  f"queue_depth={stats['current_queue_depth']}")

    print()
    print("=" * 80)
    print("FINAL STATISTICS")
    print("=" * 80)

    stats = server.get_stats()
    print(f"Requests Served Immediately: {stats['requests_served']}")
    print(f"Requests Queued/Batched:    {stats['requests_queued']}")
    print(f"Requests Rejected:          {stats['requests_rejected']}")
    print()
    print("Decision Breakdown:")
    for decision, count in stats['decisions'].items():
        pct = (count / 50 * 100)
        print(f"  {decision:<10}: {count:>2} ({pct:>5.1f}%)")
    print()
    print("What SOLO ROCK did:")
    print(f"  - Served {stats['requests_served']}/{50} requests immediately (no queue)")
    print(f"  - Batched {stats['requests_queued']}/{50} requests to reduce latency variance")
    print(f"  - Rejected {stats['requests_rejected']}/{50} requests to protect server")
    print(f"  - This prevents clients from retrying and overloading the server further")
    print()

    server.shutdown()
