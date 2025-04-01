import os
from typing import Annotated

import dagger
from dagger import DefaultPath, Doc, dag, function, object_type


@object_type
class DaggerCiTemplate:

    def __init__(self):
        self._dag = dag
        self.registry_image_path = os.getenv("REGISTRY_IMAGE_PATH", "ttl.sh/dagger-ci-template")

    @function
    async def build(
        self,
        context: Annotated[
            dagger.Directory,
            Doc("location of source/context directory"),
            DefaultPath(".")
        ],
        dockerfile: Annotated[
            str,
            Doc("location of Dockerfile"),
        ] = "Dockerfile",
        publish: Annotated[
            bool,
            Doc("publish to registry"),
        ] = False,
    ) -> str:
        """
        Build and publish image from Dockerfile

        This example uses a build context directory in a different location
        than the current working directory.
        """
        # get build context with dockerfile added
        # workspace = (
        #     dag.container()
        #     .with_directory("/src", contextdir)
        #     .with_workdir("/src")
        #     .with_file("/src/Dockerfile", dockerfile)
        #     .directory("/src")
        # )

        # build using Dockerfile and publish to registry
        ref = (
            dag.container()
            .build(context=context, dockerfile=dockerfile)
            .publish(f"{self.ci_registry_image}:{self.ci_commit_short_sha}")
        )
        # if publish:
        #     ref = ref.publish("ttl.sh/hello-dagger")
        return await ref
