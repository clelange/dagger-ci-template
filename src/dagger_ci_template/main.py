import os
from typing import Annotated

import dagger
from dagger import DefaultPath, Doc, dag, function, object_type


@object_type
class DaggerCiTemplate:

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
        registry_image_path: Annotated[
            str,
            Doc("registry image path"),
        ] = "ttl.sh/dagger-ci-template",
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
        # build using Dockerfile and publish to registry
        ref = (
            dag.container()
            .build(context=context, dockerfile=dockerfile)
            .publish(registry_image_path)
        )
        # if publish:
        #     ref = ref.publish("ttl.sh/hello-dagger")
        return await ref
