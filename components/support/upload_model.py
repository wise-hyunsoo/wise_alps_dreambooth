from google_cloud_pipeline_components.types.artifact_types import (
    UnmanagedContainerModel,
)
from google_cloud_pipeline_components.types.artifact_types import VertexModel
from kfp import dsl
from kfp.dsl import Input
from kfp.dsl import Output


@dsl.component(
    packages_to_install=["google-cloud-pipeline-components>=2.0.0"],
)
def model_upload(
    project: str,
    location: str,
    display_name: str,
    model: Output[VertexModel],
    parent_model: Input[VertexModel] = None,
    unmanaged_container_model: Input[UnmanagedContainerModel] = None,
    is_default_version: bool = False,
):
    """
    Custom component for model upload to Vertex AI model registry.

    Official ModelUploadOp (from google_cloud_pipeline_components.v1.model) component has some bugs.
    - One of them is that it uploads a model with parent_model, but the new version of the model is not set as default.
    - Another one is that it returns model URI without the version, which is required for the next step of the pipeline.

    This component fixes this bugs.
    """
    from google.cloud import aiplatform

    artifact_uri = unmanaged_container_model.uri
    serving_container_image_uri = unmanaged_container_model.metadata.get(
        "containerSpec"
    ).get("imageUri")

    uploaded_model = aiplatform.Model.upload(
        display_name=display_name,
        parent_model=parent_model.metadata["resourceName"] if parent_model else None,
        project=project,
        location=location,
        artifact_uri=artifact_uri,
        serving_container_image_uri=serving_container_image_uri,
        is_default_version=is_default_version,
    )

    api_endpoint = location + "-aiplatform.googleapis.com"
    model.uri = f"https://{api_endpoint}/v1/{uploaded_model.versioned_resource_name}"
    model.metadata["resourceName"] = uploaded_model.versioned_resource_name
