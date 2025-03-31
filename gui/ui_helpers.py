from typing import Any, Callable, ParamSpec
from PySide6.QtWidgets import QMessageBox

P = ParamSpec('P')


def run_and_raise(func: Callable[P, None]) -> Callable:
    def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    return wrapper