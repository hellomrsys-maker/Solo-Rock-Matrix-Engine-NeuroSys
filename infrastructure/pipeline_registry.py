class PipelineRegistry:
    def __init__(self):
        self._nerves_by_pipeline = {
            "input_comm": [],
            "timing_comm": [],
            "performance": [],
            "runtime": [],
            "output": []
        }

    def register(self, nerve):
        if nerve.PIPELINE in self._nerves_by_pipeline:
            self._nerves_by_pipeline[nerve.PIPELINE].append(nerve)
            
    def get_nerves(self, pipeline_id):
        return self._nerves_by_pipeline.get(pipeline_id, [])

# Global registry
pipeline_registry = PipelineRegistry()
