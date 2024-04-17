from google.cloud import aiplatform

from settings.settings import get_settings

settings = get_settings()

aiplatform.init(
    project=settings.project_id,
    location=settings.default_location,
    staging_bucket=f"{settings.vertex_bucket}/custom-job-artifacts",
)

job = aiplatform.CustomJob.from_local_script(
    display_name="my-custom-job",
    script_path="./components/train_model/custom_job_script.py",
    # https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
    # TODO: Choose a training base image from the above link
    container_uri="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12.py310:latest",
    replica_count=1,
    requirements=[
        "python-json-logger==2.0.7",
    ],
    machine_type="n1-standard-4",
)

job.run()
