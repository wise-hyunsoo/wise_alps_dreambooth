from kfp import dsl


@dsl.component(
    # https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
    # TODO: Choose a training base image from the above link
    base_image="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13.py310:latest",
    packages_to_install=[
        # Required packages are not installed in the base image
    ],
)
def train_model(
    model_dir: str,
):
    # Add your training code here
    pass
