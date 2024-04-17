import time

from google.cloud import aiplatform

from settings.settings import get_settings

settings = get_settings()

# Before initializing, make sure to set the GOOGLE_APPLICATION_CREDENTIALS
# environment variable to the file path of your service account.
# For example:
#   export GOOGLE_APPLICATION_CREDENTIALS="~/key.json"
aiplatform.init(
    project=settings.project_id,
    location=settings.default_location,
)

PARENT_MODEL_NUMBER = "1342785172491206656"
MODEL_DISPLAY_NAME = "tf-decision-forests-sample"
PIPELINE_PACKAGE_PATH = "tfdf_sample_pipeline.json"
PIPELINE_DISPLAY_NAME = "tensorflow_decision_forests_sample_pipeline"
PREDICTION_INPUT_DATASET_ID = "penguins_prediction"
TEST_DATA_TABLE_ID = "penguins_test_data"
TRAIN_DATA_PARQUET_FILENAME = "penguins_train.parquet"
TRAIN_DATA_BUCKET_NAME = "us-west1-dev-ai-lab-vertex"
COLUMNS = (
    "species",
    "island",
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "sex",
    "year",
)
TARGET = "species"
BATCH_SAMPLE_SIZE = 3000
CLASS_LABELS = ["Adelie", "Gentoo", "Chinstrap"]
TRAIN_DATA_OBJECT = "train_data/{}-{}".format(
    TRAIN_DATA_PARQUET_FILENAME, "1689663617018021692"
)

# Prepare the pipeline job
job = aiplatform.PipelineJob(
    display_name="sample-evaluation",
    template_path=f"{settings.pipeline_registry_host}/sample-evaluation/latest",
    pipeline_root=f"{settings.vertex_bucket}/pipelines",
    parameter_values={
        "project": settings.project_id,
        "location": settings.default_location,
        "parent_model": f"projects/{settings.project_number}/locations/{settings.default_location}/models/{PARENT_MODEL_NUMBER}",
        "model_dir": f"{settings.vertex_bucket}/model/{time.time_ns()}",
        "model_display_name": MODEL_DISPLAY_NAME,
        "target_field_name": TARGET,
        "train_bucket_name": TRAIN_DATA_BUCKET_NAME,
        "train_bucket_object": TRAIN_DATA_OBJECT,
        "bigquery_test_data_uri": f"bq://{settings.project_id}.{PREDICTION_INPUT_DATASET_ID}.{TEST_DATA_TABLE_ID}",
        "bigquery_destination_output_uri": f"bq://{settings.project_id}.{PREDICTION_INPUT_DATASET_ID}",
        "batch_predict_instances_format": "bigquery",
        "batch_predict_predictions_format": "bigquery",
        "evaluation_class_names": CLASS_LABELS,
        "batch_predict_data_sample_size": BATCH_SAMPLE_SIZE,
    },
)

job.submit()
