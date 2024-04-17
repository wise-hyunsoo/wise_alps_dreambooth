import subprocess

import fire

from create import create_component, create_pipeline


class Configure(object):
    @staticmethod
    def wipr(repo: str):
        """
        Add the repository to a workload identity pool to access Google Cloud resources.
        :param repo: repository name
        :return:
        """
        subprocess.call(
            ["bash", "./scripts/support/workload-identity-pool-resource.sh", repo]
        )


class Create(object):
    @staticmethod
    def component(name: str):
        """
        Create component
        :param name: component name
        :return:
        """
        create_component(name)

    @staticmethod
    def pipeline(name: str):
        """
        Create pipeline
        :param name: pipeline name
        :return:
        """
        create_pipeline(name)


class Build(object):
    @staticmethod
    def components():
        """
        Build containerized components. (If you have components that need to be containerized.)
        :return:
        """
        subprocess.call(["bash", "./scripts/support/build.sh"])


class Compile(object):
    @staticmethod
    def pipelines():
        """
        Compile pipelines.
        :return:
        """
        subprocess.call(["bash", "./scripts/support/compile.sh"])


class Upload(object):
    @staticmethod
    def pipelines():
        """
        Upload pipelines to the Vertex AI Pipelines.
        :return:
        """
        subprocess.call(["bash", "./scripts/support/upload-pipelines.sh"])

    @staticmethod
    def components():
        """
        Upload containerized components to the Artifact Registry.
        :return:
        """
        subprocess.call(["bash", "./scripts/support/upload-components.sh"])


class Commands(object):
    def __init__(self):
        self.configure = Configure()
        self.create = Create()
        self.build = Build()
        self.compile = Compile()
        self.upload = Upload()


if __name__ == "__main__":
    fire.Fire(component=Commands(), name="alps")
