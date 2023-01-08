from typing import Optional

from rich.console import Console
from rich.progress import GetTimeCallable, Progress, SpinnerColumn, TimeElapsedColumn


def CustomProgress(
    console: Optional[Console] = None,
    auto_refresh: bool = True,
    refresh_per_second: float = 10,
    speed_estimate_period: float = 30.0,
    transient: bool = False,
    redirect_stdout: bool = True,
    redirect_stderr: bool = True,
    get_time: Optional[GetTimeCallable] = None,
    disable: bool = False,
    expand: bool = False,
):
    CustomizedProgressColumns = [
        SpinnerColumn(),
        *Progress.get_default_columns(),
        "Elapsed:",
        TimeElapsedColumn(),
    ]

    return Progress(
        *CustomizedProgressColumns,
        console=console,
        auto_refresh=auto_refresh,
        refresh_per_second=refresh_per_second,
        speed_estimate_period=speed_estimate_period,
        transient=transient,
        redirect_stdout=redirect_stdout,
        redirect_stderr=redirect_stderr,
        get_time=get_time,
        disable=disable,
        expand=expand,
    )
