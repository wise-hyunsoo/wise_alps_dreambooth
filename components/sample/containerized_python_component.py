import os

from kfp import dsl

from helpers.hello import say_hello

# NOTE: Containerized python component must define the target image
#   using the CONTAINER_REPOSITORY environment variable.
CONTAINER_REPOSITORY = os.getenv("CONTAINER_REPOSITORY")
PROJECT_NAME = os.getenv("PROJECT_NAME")


@dsl.component(
    base_image="python:3.10",
    target_image=f"{CONTAINER_REPOSITORY}/{PROJECT_NAME}-sample-reception:latest",
)
def reception(visitor: str) -> str:
    """
    Example of a containerized python component that uses the outer module.
    """
    say_hello(visitor)
    return visitor
