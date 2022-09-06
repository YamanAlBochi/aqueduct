from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from aqueduct.artifacts import utils as artifact_utils
from aqueduct.artifacts.base_artifact import BaseArtifact
from aqueduct.dag import DAG
from aqueduct.enums import ArtifactType


class GenericArtifact(BaseArtifact):
    """This class represents a generic artifact within the flow's DAG.

    Currently, a generic artifact can be any artifact other than table, numeric, bool, or parameter
    generated from eager execution, or an artifact of unknown type generated from lazy execution.
    """

    def __init__(
        self,
        dag: DAG,
        artifact_id: uuid.UUID,
        artifact_type: ArtifactType = ArtifactType.UNTYPED,
        content: Optional[Any] = None,
        from_flow_run: bool = False,
    ):
        # Cannot initialize a generic artifact's content without also setting its type.
        if content is not None:
            assert artifact_type != ArtifactType.UNTYPED

        self._dag = dag
        self._artifact_id = artifact_id
        # This parameter indicates whether the artifact is fetched from flow-run or not.
        self._from_flow_run = from_flow_run
        self._set_content(content)

        if self._from_flow_run:
            # If the artifact is initialized from a flow run, then it should not contain any content.
            assert self._get_content() is None

    def get(self, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Materializes the artifact.

        Returns:
            The materialized value.

        Raises:
            InvalidRequestError:
                An error occurred because of an issue with the user's code or inputs.
            InternalServerError:
                An unexpected error occurred in the server.
        """
        self._dag.must_get_artifact(self._artifact_id)

        if parameters is None and self._get_content() is not None:
            return self._get_content()

        previewed_artifact = artifact_utils.preview_artifact(
            self._dag, self._artifact_id, parameters
        )
        content = previewed_artifact._get_content()

        # If the artifact was previously generated lazily, materialize the contents.
        if parameters is None and self._get_content() is None:
            self._set_content(content)

        return content

    def describe(self) -> None:
        """Prints out a human-readable description of the bool artifact."""
        # TODO: make this more informative.
        print("This is a %s artifact." % self._get_type())
