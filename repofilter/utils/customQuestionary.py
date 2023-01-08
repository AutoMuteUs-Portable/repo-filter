from typing import Any, Callable

from prompt_toolkit.layout import VSplit, Window, to_container, to_dimension
from questionary import Question

from .temporarilyStopLive import TemporarilyStopLive


def CustomQuestionary(indent: int, func: Callable[..., Any], *args, **kwargs) -> Any:
    with TemporarilyStopLive():
        question: Question = func(*args, **kwargs)
        layout = question.application.layout

        # Configure width
        # Set weight to 2 to give first priority to the original container
        layout.container.width = to_dimension(layout.container.width)
        layout.container.width.weight = 2

        layout.container = to_container(
            VSplit([Window(width=indent, char=" "), layout.container])
        )

        return question.ask()
