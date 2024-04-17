from pipelines.sample.evaluate import sample_evaluate
from pipelines.sample.train_upload import sample_train_upload
from pipelines.support.pipeline_enum import PipelineEnum


class Pipelines(PipelineEnum):
    # SAMPLE_SIMPLE = (sample_simple, "sample-simple.yaml", False, False)
    SAMPLE_TRAIN_UPLOAD = (
        sample_train_upload,
        "sample-train-upload.yaml",
        False,
        False,
    )
    SAMPLE_EVALUATE = (sample_evaluate, "sample-evaluate.yaml", False, False)
