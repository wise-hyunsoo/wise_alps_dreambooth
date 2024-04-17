from kfp import dsl


@dsl.component(
    packages_to_install=[
        "google-cloud-logging~=3.6.0",
    ],
)
def log_struct(
    project: str,
):
    from google.cloud import logging

    # Make sure to pass the project ID explicitly.
    # The pipeline job runs in on-demand project (different project from the pipeline project).
    # If project ID not given, will be inferred from the environment. But the environment is the on-demand project.
    logging_client = logging.Client(project=project)

    # This logger logs with different resource than the pipeline job.
    # You cannot see the logs in the pipeline job.
    logger = logging_client.logger("sample-logger")

    # Make a simple text log
    logger.log_text("Hello, world!")

    # Simple text log with severity.
    logger.log_text("Goodbye, world!", severity="ERROR")

    # Struct log. The struct can be any JSON-serializable dictionary.
    logger.log_struct(
        {
            "severity": "NOTICE",
            "message": "Struct log. The struct can be any JSON-serializable dictionary.",
        },
        labels={
            "name": "King Arthur",
            "quest": "Find the Holy Grail",
            "favorite_color": "Blue",
        },
    )
    # You can see the logs by querying the labels of the logs.
    # For example, you can see the logs by running the following command:
    #   gcloud logging read "labels.favorite_color=Blue"
