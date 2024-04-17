from kfp import dsl

from components.sample.containerized_python_component import reception
from components.sample.lightweight_python_component import gatekeeper
from settings.settings import get_settings

settings = get_settings()


@dsl.pipeline(
    name="sample-simple",
    description="Sample simple pipeline.",
    pipeline_root=f"{settings.vertex_bucket}/pipelines",
)
def sample_simple(
    project: str,
    location: str,
):
    visitor = gatekeeper(visitor="guest")
    reception(visitor=visitor.output)

    # visitor = (
    #     gatekeeper(visitor="guest")
    #     .set_cpu_request("16")
    #     .set_memory_request("32Gi")
    #     .set_accelerator_type("NVIDIA_TESLA_T4")
    #     .set_gpu_limit("1")
    # )
