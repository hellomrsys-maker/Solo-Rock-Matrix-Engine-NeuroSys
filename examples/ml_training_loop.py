"""
Integration Example: ML Training Loop with SOLO ROCK

Shows how to use SOLO ROCK to detect hardware busyness and adapt submission rate
in a machine learning training loop, reducing retry storms and thermal spikes.

This is a conceptual example — adapt it to your specific ML framework (PyTorch, TensorFlow, etc.)
"""

import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from central_command.central_ai import CentralAI
from central_command.decision_engine import FULL_RATE, BATCH, THROTTLE, EMERGENCY


class TrainingLoop:
    """ML training loop that respects SOLO ROCK backpressure."""

    def __init__(self, model, train_loader, num_epochs=10, log_interval=10):
        self.model = model
        self.train_loader = train_loader
        self.num_epochs = num_epochs
        self.log_interval = log_interval
        self.ceo = CentralAI()
        self.batch_queue = []
        self.stats = {
            "batches_processed": 0,
            "batches_queued": 0,
            "thermal_events": 0,
            "decisions": {FULL_RATE: 0, BATCH: 0, THROTTLE: 0, EMERGENCY: 0}
        }

    def train_epoch(self, epoch):
        """Train for one epoch, respecting SOLO ROCK decisions."""
        epoch_loss = 0.0
        batch_num = 0

        for batch_data in self.train_loader:
            # **KEY:** Ask SOLO ROCK what hardware state is
            action, reason, snapshot = self.ceo.tick()
            self.stats["decisions"][action] += 1

            # Log telemetry
            cpu_temp = snapshot.get('cpu_temp', 0.0)
            cpu_load = snapshot.get('cpu_load', 0.0)
            ram_usage = snapshot.get('ram_usage', 0.0)

            batch_num += 1

            # **DECISION TREE:** Adapt submission strategy based on hardware state
            if action == FULL_RATE:
                # Hardware has headroom: submit immediately
                loss = self._compute_batch(batch_data)
                epoch_loss += loss
                self.stats["batches_processed"] += 1

                if batch_num % self.log_interval == 0:
                    print(f"[Epoch {epoch}, Batch {batch_num:>4}] "
                          f"Loss: {loss:.4f} | "
                          f"{action} (temp={cpu_temp:.1f}C, load={cpu_load:.1f}%) | "
                          f"Reason: {reason}")

            elif action == BATCH:
                # Moderate load: queue submissions for coalescing
                # When 4 batches queued, submit them as a single batch operation
                self.batch_queue.append(batch_data)
                self.stats["batches_queued"] += 1

                if len(self.batch_queue) >= 4:
                    # Process queued batches together
                    loss = self._compute_batch_group(self.batch_queue)
                    epoch_loss += loss
                    self.stats["batches_processed"] += len(self.batch_queue)
                    self.batch_queue = []

                    if batch_num % self.log_interval == 0:
                        print(f"[Epoch {epoch}, Batch {batch_num:>4}] "
                              f"Loss: {loss:.4f} (batched 4 items) | "
                              f"{action} (temp={cpu_temp:.1f}C, load={cpu_load:.1f}%)")

            elif action == THROTTLE:
                # High load: pace submissions, back off
                self.batch_queue.append(batch_data)
                self.stats["batches_queued"] += 1

                # Only process when queue reaches 2 (instead of 4)
                if len(self.batch_queue) >= 2:
                    loss = self._compute_batch_group(self.batch_queue)
                    epoch_loss += loss
                    self.stats["batches_processed"] += len(self.batch_queue)
                    self.batch_queue = []

                    # Back off to give hardware time to cool/clear queues
                    time.sleep(0.05)

                    if batch_num % self.log_interval == 0:
                        print(f"[Epoch {epoch}, Batch {batch_num:>4}] "
                              f"Loss: {loss:.4f} (batched, paced) | "
                              f"{action} (temp={cpu_temp:.1f}C, load={cpu_load:.1f}%) | "
                              f"BACKING OFF — {reason}")

            elif action == EMERGENCY:
                # Critical thermal/power state: hold everything
                self.batch_queue.append(batch_data)
                self.stats["batches_queued"] += 1
                self.stats["thermal_events"] += 1

                # Wait for conditions to normalize before processing
                if len(self.batch_queue) >= 1:
                    # Only process if queue is blocking
                    time.sleep(0.1)
                    loss = self._compute_batch_group(self.batch_queue)
                    epoch_loss += loss
                    self.stats["batches_processed"] += len(self.batch_queue)
                    self.batch_queue = []

                if batch_num % self.log_interval == 0:
                    print(f"[Epoch {epoch}, Batch {batch_num:>4}] "
                          f"Loss: {loss:.4f} | "
                          f"{action} (temp={cpu_temp:.1f}C, load={cpu_load:.1f}%) | "
                          f"⚠ EMERGENCY: {reason}")

        # Flush any remaining queued batches at end of epoch
        if self.batch_queue:
            loss = self._compute_batch_group(self.batch_queue)
            epoch_loss += loss
            self.stats["batches_processed"] += len(self.batch_queue)
            self.batch_queue = []

        avg_loss = epoch_loss / max(batch_num, 1)
        return avg_loss

    def _compute_batch(self, batch_data):
        """Compute forward/backward pass on single batch. Placeholder."""
        # In real code: loss = self.model(batch_data); loss.backward()
        # For this example, we simulate with random loss
        import random
        return random.uniform(0.5, 2.5)

    def _compute_batch_group(self, batch_group):
        """Compute forward/backward pass on group of batches. Placeholder."""
        # In real code: concatenate batches, process together, backward
        import random
        return random.uniform(0.5, 2.5)

    def train(self):
        """Run full training loop."""
        print("=" * 80)
        print("ML TRAINING WITH SOLO ROCK BACKPRESSURE")
        print("=" * 80)
        print()

        for epoch in range(self.num_epochs):
            print(f"\nEpoch {epoch + 1}/{self.num_epochs}")
            print("-" * 80)

            avg_loss = self.train_epoch(epoch)

            print(f"\nEpoch {epoch + 1} Summary:")
            print(f"  Average Loss: {avg_loss:.4f}")
            print(f"  Batches processed: {self.stats['batches_processed']}")
            print(f"  Batches queued: {self.stats['batches_queued']}")
            print(f"  Thermal events: {self.stats['thermal_events']}")
            print(f"  Decision breakdown: {self.stats['decisions']}")

        print("\n" + "=" * 80)
        print("TRAINING COMPLETE")
        print("=" * 80)
        print()
        print("What SOLO ROCK did:")
        print(f"  - Reduced submission rate during high load via BATCH coalescing")
        print(f"  - Paced submissions during thermal stress via THROTTLE")
        print(f"  - Held submissions during emergency via EMERGENCY mode")
        print(f"  - Total thermal events: {self.stats['thermal_events']}")
        print(f"  - This prevents retry storms and reduces wasted power")
        print()


# Example usage
if __name__ == "__main__":
    # Dummy model and data loader (replace with real ones)
    class DummyModel:
        def __call__(self, batch):
            return None

    class DummyDataLoader:
        def __init__(self, num_batches=50):
            self.num_batches = num_batches

        def __iter__(self):
            for i in range(self.num_batches):
                yield f"batch_{i}"

    model = DummyModel()
    train_loader = DummyDataLoader(num_batches=50)

    trainer = TrainingLoop(model, train_loader, num_epochs=3, log_interval=10)
    trainer.train()
