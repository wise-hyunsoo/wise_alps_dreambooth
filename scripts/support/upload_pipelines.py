from pipelines.support.pipelines import Pipelines

for pipeline in Pipelines:
    if pipeline.do_upload:
        pipeline.upload()
