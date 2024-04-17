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

PARENT_MODEL_NUMBER = "123456789"
PIPELINE_NAME = ""

parent_model = f"projects/{settings.project_number}/locations/{settings.default_location}/models/{PARENT_MODEL_NUMBER}"

# Prepare the pipeline job
job = aiplatform.PipelineJob(
    display_name=PIPELINE_NAME,
    template_path=f"{settings.pipeline_registry_host}/{PIPELINE_NAME}/latest",
    pipeline_root=f"{settings.vertex_bucket}/pipelines",
    parameter_values={
        "project": settings.project_id,
        "location": settings.default_location,
        "parent_model": parent_model,
        "model_dir": f"{settings.vertex_bucket}/model/{time.time_ns()}",
    },
)

job.submit()
