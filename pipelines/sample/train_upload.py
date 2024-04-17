from typing import Optional

from google_cloud_pipeline_components._implementation.model import GetVertexModelOp
from google_cloud_pipeline_components.types import artifact_types
from google_cloud_pipeline_components.v1.custom_job import utils
from kfp import dsl

from components.sample.train_model_by_train_upload import train_model
from components.support.upload_model import model_upload
from settings.settings import get_settings

settings = get_settings()

# Create a custom training job component from the pipeline component
custom_training_op = utils.create_custom_training_job_from_component(
    train_model,
    machine_type="n1-standard-4",
    replica_count=1,
)


@dsl.pipeline(
    name="sample-train-upload",
    description="Sample train & upload pipeline.",
    pipeline_root=f"{settings.vertex_bucket}/pipelines",
)
def sample_train_upload(
    project: str,
    location: str,
    parent_model: Optional[str],
    model_dir: str,
):
    custom_producer_task = custom_training_op(
        project=project,
        location=location,
        model_dir=model_dir,
    )

    unmanaged_model_importer = dsl.importer(
        artifact_uri=model_dir,
        artifact_class=artifact_types.UnmanagedContainerModel,
        metadata={
            "containerSpec": {
                # https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
                # TODO: Choose a prediction base image from the above link
                "imageUri": "us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-11:latest"
            }
        },
    )

    get_parent_model = GetVertexModelOp(model_name=parent_model)

    # The pipeline does not fail even if the parent model does not exist because ignore_upstream_failure() is called.
    model_upload_op = model_upload(
        project=project,
        display_name="sample model",
        location=location,
        parent_model=get_parent_model.outputs["model"],
        unmanaged_container_model=unmanaged_model_importer.outputs["artifact"],
        is_default_version=False,
    ).ignore_upstream_failure()

    model_upload_op.after(custom_producer_task)
