import os

from kfp import dsl

CONTAINER_REPOSITORY = os.getenv("CONTAINER_REPOSITORY")


@dsl.component(
    base_image=f"{CONTAINER_REPOSITORY}/lightweight-python-component-base:latest",
    install_kfp_package=False,
)
def sheepdog(visitor: str) -> str:
    """
    Example of a lightweight python component
    """
    import cowsay

    assert visitor != "stranger", cowsay.cow("You are not allowed to enter!")

    return visitor
