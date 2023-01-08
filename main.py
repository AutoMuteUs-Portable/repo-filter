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
@click.option(
    "--input",
    type=click.Path(dir_okay=False, exists=True),
    help="Path to dill file to be inputted",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, exists=False),
    required=True,
    help="Path to dill file to be outputted",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Run git-filter-repo with --force option",
)
@click.argument(
    "destination",
    type=click.Path(file_okay=False, exists=False),
)
@click.argument(
    "upstream-url",
    type=str,
    default="https://github.com/automuteus/automuteus",
)
def automuteus_init(
    input: Optional[str],
    output: str,
    force: bool,
    destination: str,
    upstream_url: str,
):
    """
    \b
    Initialize automuteus repository for AutoMuteUs-Portable.

    \b
    Applying filter is necessary because the upstream repository is not designed to be built for Windows.
    It makes possible to build Windows executable using Github Actions.

    \b
    After initializing repository, push to your own remote repository and push tags to run Github Actions.
    If upstream reposiory is updated, run update command to apply filter to the new commits.

    \b
    Arguments:
        destination: Path to destination(local repository) directory
        upstream_url: URL to upstream repository
    """
    Init(destination, input, output, upstream_url, force)


@automuteus.command("update")
@click.option(
    "--input",
    type=click.Path(dir_okay=False, exists=True),
    required=True,
    help="Path to dill file to be inputted",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, exists=False),
    help="Path to dill file to be outputted",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Run git-filter-repo with --force option",
)
@click.argument(
    "destination",
    type=click.Path(file_okay=False, exists=False),
)
@click.argument(
    "upstream-url",
    type=str,
    default="https://github.com/automuteus/automuteus",
)
def automuteus_update(
    input: str,
    output: Optional[str],
    force: bool,
    destination: str,
    upstream_url: str,
):
    """
    \b
    Update automuteus repository that is filtered previously.

    \b
    Arguments:
        destination: Path to destination(local repository) directory
        upstream_url: URL to upstream repository
    """
    Update(
        destination, input, output if output is not None else input, upstream_url, force
    )


def main():
    try:
        cli()
    except SystemExit as e:
        if e.code == 0:
            return
    except:
        console.print_exception()


if __name__ == "__main__":
    main()
