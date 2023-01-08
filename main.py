from typing import Optional

import click

from commands.init import Init
from commands.update import Update
from utils.initializeConsole import InitializeConsole

console = InitializeConsole()


@click.group()
def cli():
    pass


@cli.group()
def automuteus():
    pass


@automuteus.command("init")
@click.option("--input", type=click.Path(dir_okay=False, exists=True))
@click.option("--output", type=click.Path(dir_okay=False, exists=False), required=True)
@click.option("--force", is_flag=True, default=False)
@click.argument("destination", type=click.Path(file_okay=False, exists=False))
@click.argument(
    "upstream-url", type=str, default="https://github.com/automuteus/automuteus"
)
def automuteus_init(
    input: Optional[str],
    output: str,
    force: bool,
    destination: str,
    upstream_url: str,
):
    Init(destination, input, output, upstream_url, force)


@automuteus.command("update")
@click.option("--input", type=click.Path(dir_okay=False, exists=True), required=True)
@click.option("--output", type=click.Path(dir_okay=False, exists=False))
@click.option("--force", is_flag=True, default=False)
@click.argument("destination", type=click.Path(file_okay=False, exists=False))
@click.argument(
    "upstream-url", type=str, default="https://github.com/automuteus/automuteus"
)
def automuteus_update(
    input: str,
    output: Optional[str],
    force: bool,
    destination: str,
    upstream_url: str,
):
    Update(
        destination, input, output if output is not None else input, upstream_url, force
    )


def main():
    try:
        cli()
    except:
        console.print_exception()


if __name__ == "__main__":
    main()
