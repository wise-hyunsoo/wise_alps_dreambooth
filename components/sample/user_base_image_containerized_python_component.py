import os

from kfp import dsl

from helpers.say import say

# NOTE: Containerized python component must define the target image
#   using the CONTAINER_REPOSITORY environment variable.
CONTAINER_REPOSITORY = os.getenv("CONTAINER_REPOSITORY")
PROJECT_NAME = os.getenv("PROJECT_NAME")


@dsl.component(
    base_image=f"{CONTAINER_REPOSITORY}/containerized-python-component-base:latest",
    target_image=f"{CONTAINER_REPOSITORY}/{PROJECT_NAME}-sample-shepherd:latest",
)
def shepherd(visitor: str) -> str:
    """
    Example of a containerized python component that uses the outer module.
    """
    say(visitor)

    return visitor
