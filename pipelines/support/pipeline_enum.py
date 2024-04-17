from enum import Enum
from functools import cached_property

import google.auth
from kfp import compiler
from kfp.registry import RegistryClient

from settings.settings import get_settings


class PipelineEnum(Enum):
    def __init__(self, func, compiled_filename, do_compile=True, do_upload=True):
        self.func = func
        self.compiled_filename = compiled_filename
        self.do_compile = do_compile
        self.do_upload = do_upload

    @cached_property
    def settings(self):
        return get_settings()

    @cached_property
    def registry_client(self):
        auth, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        return RegistryClient(
            host=self.settings.pipeline_registry_host,
            auth=auth,
        )

    def compile(self):
        compiler.Compiler().compile(
            pipeline_func=self.func,
            package_path=f"pipelines/compiled/{self.compiled_filename}",
        )

    def upload(self):
        template_name, version_name = self.registry_client.upload_pipeline(
            file_name=f"pipelines/compiled/{self.compiled_filename}",
            tags=[self.settings.pipelines_shared_tag, "latest"],
        )

        print(
            f"Upload completed! Template name: {template_name} / Version name: {version_name}"
        )
