from __future__ import annotations

import argparse
import logging
import sys

from oci_artifact_importer import OciVerifyError
from oci_artifact_importer.commands import mirror, results, verify


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oci-artifact-importer", description="Verify, mirror, and process OCI artifacts"
    )
    subparsers = parser.add_subparsers(dest="command")

    verify.register(subparsers)
    mirror.register(subparsers)
    results.register(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    parser = make_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help(sys.stderr)
        return 2

    try:
        return args.func(args)
    except OciVerifyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
