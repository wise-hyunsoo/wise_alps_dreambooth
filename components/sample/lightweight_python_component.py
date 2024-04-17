from kfp import dsl


@dsl.component
def gatekeeper(visitor: str) -> str:
    """
    Example of a lightweight python component
    """
    assert visitor != "stranger", "You are not allowed to enter!"

    return visitor
