from typing import Optional

from google_cloud_pipeline_components._implementation.model import GetVertexModelOp
from google_cloud_pipeline_components._implementation.model_evaluation import (
    EvaluationDataSamplerOp,
)
from google_cloud_pipeline_components._implementation.model_evaluation import (
    ModelImportEvaluationOp,
)
from google_cloud_pipeline_components._implementation.model_evaluation import (
    TargetFieldDataRemoverOp,
)
from google_cloud_pipeline_components.types import artifact_types
from google_cloud_pipeline_components.v1.batch_predict_job import ModelBatchPredictOp
from google_cloud_pipeline_components.v1.custom_job import utils
from google_cloud_pipeline_components.v1.model_evaluation import (
    ModelEvaluationClassificationOp,
)
from kfp import dsl

from components.sample.train_model_for_evaluate import train_model
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
    name="sample-evaluation",
    description="Sample evaluation pipeline.",
    pipeline_root=f"{settings.vertex_bucket}/pipelines",
)
def sample_evaluate(
    project: str,
    location: str,
    parent_model: Optional[str],
    model_dir: str,
    model_display_name: str,
    target_field_name: str,
    train_bucket_name: str,
    train_bucket_object: str,
    bigquery_test_data_uri: str,
    bigquery_destination_output_uri: str,
    batch_predict_instances_format: str,
    evaluation_class_names: list,
    batch_predict_predictions_format: str = "bigquery",
    evaluation_prediction_label_column: str = "",
    evaluation_prediction_score_column: str = "prediction",
    batch_predict_machine_type: str = "n1-standard-4",
    batch_predict_starting_replica_count: int = 5,
    batch_predict_max_replica_count: int = 10,
    batch_predict_data_sample_size: int = 10000,
):
    custom_producer_task = custom_training_op(
        project=project,
        location="asia-northeast3",
        model_dir=model_dir,
        label_column=target_field_name,
        train_bucket_name=train_bucket_name,
        train_bucket_object=train_bucket_object,
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
        display_name=model_display_name,
        location=location,
        parent_model=get_parent_model.outputs["model"],
        unmanaged_container_model=unmanaged_model_importer.outputs["artifact"],
        is_default_version=False,
    ).ignore_upstream_failure()

    model_upload_op.after(custom_producer_task)

    # Run the data sampling task
    data_sampler_task = EvaluationDataSamplerOp(
        project=project,
        location=location,
        bigquery_source_uri=bigquery_test_data_uri,
        instances_format=batch_predict_instances_format,
        sample_size=batch_predict_data_sample_size,
    )

    # Run the task to remove the target field from data for batch prediction
    data_splitter_task = TargetFieldDataRemoverOp(
        project=project,
        location=location,
        bigquery_source_uri=data_sampler_task.outputs["bigquery_output_table"],
        instances_format=batch_predict_instances_format,
        target_field_name=target_field_name,
    )

    batch_predict_task = ModelBatchPredictOp(
        project=project,
        location=location,
        model=model_upload_op.outputs["model"],
        job_display_name="model-registry-batch-prediction",
        bigquery_source_input_uri=data_splitter_task.outputs["bigquery_output_table"],
        instances_format=batch_predict_instances_format,
        instance_type="object",
        predictions_format=batch_predict_predictions_format,
        bigquery_destination_output_uri=bigquery_destination_output_uri,
        machine_type=batch_predict_machine_type,
        starting_replica_count=batch_predict_starting_replica_count,
        max_replica_count=batch_predict_max_replica_count,
    )

    # Run the evaluation based on prediction type
    eval_task = ModelEvaluationClassificationOp(
        project=project,
        location=location,
        class_labels=evaluation_class_names,
        prediction_label_column=evaluation_prediction_label_column,
        prediction_score_column=evaluation_prediction_score_column,
        target_field_name=target_field_name,
        ground_truth_format=batch_predict_instances_format,
        ground_truth_bigquery_source=data_sampler_task.outputs["bigquery_output_table"],
        predictions_format=batch_predict_predictions_format,
        predictions_bigquery_source=batch_predict_task.outputs["bigquery_output_table"],
    )

    # Import the model evaluations to the Vertex AI model
    ModelImportEvaluationOp(
        classification_metrics=eval_task.outputs["evaluation_metrics"],
        model=model_upload_op.outputs["model"],
        dataset_type=batch_predict_instances_format,
    )
