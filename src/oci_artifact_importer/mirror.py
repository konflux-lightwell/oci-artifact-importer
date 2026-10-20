from __future__ import annotations

import logging
from pathlib import Path

from oci_artifact_importer.auth import home_docker_config, setup_ca_bundle
from oci_artifact_importer.tools import cosign

logger = logging.getLogger(__name__)


def run_mirror(source_image: str, dest_image: str, *, ca_bundle: Path | None = None) -> None:
    setup_ca_bundle(ca_bundle)
    docker_config = home_docker_config()

    cosign.copy(source_image, dest_image, docker_config=docker_config)
    logger.info("Mirrored %s -> %s", source_image, dest_image)
