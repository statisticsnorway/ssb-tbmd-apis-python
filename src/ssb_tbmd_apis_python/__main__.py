"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Tbmd Apis Python."""


if __name__ == "__main__":
    main(prog_name="ssb-tbmd-apis-python")  # pragma: no cover
