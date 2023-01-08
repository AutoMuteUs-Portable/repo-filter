from typing import Optional

import click

from commands.init import Init
from utils.initializeConsole import InitializeConsole
from utils.remote import Remote

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
@click.argument("destination", type=click.Path(file_okay=False, exists=False))
@click.argument(
    "upstream-url", type=str, default="https://github.com/automuteus/automuteus"
)
@click.argument("upstream-branch", type=str, default="master")
def automuteus_init(
    input: Optional[str],
    output: str,
    destination: str,
    upstream_url: str,
    upstream_branch: str,
):
    Init(destination, input, output, Remote(url=upstream_url, branch=upstream_branch))


if __name__ == "__main__":
    try:
        cli()
    except SystemExit as e:
        pass
    except click.Abort:
        console.print("Aborted", style="bold red")
    except:
        console.print_exception()
