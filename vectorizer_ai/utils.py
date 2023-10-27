import functools
import re
from inspect import signature
from typing import List, Tuple, Union


def enforce_types(method):
    """
    A decorator that enforces type annotations on the arguments of a method.

    Args:
        method: The method to be decorated.

    Returns:
        The decorated method.

    Raises:
        TypeError: If an argument is not of the expected type.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        sig = signature(method)
        bound = sig.bind(self, *args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            if name == "self":
                continue  # skip self argument
            expected_type = sig.parameters[name].annotation
            if expected_type is not sig.empty and not isinstance(value, expected_type):
                raise TypeError(f"Argument {name} must be of type {expected_type}")

        return method(self, *args, **kwargs)

    return wrapper


def param_exists(names: list, params: list):
    """
    Check if any of the given parameters exist.

    Args:
        names (list): A list of parameter names to check.
        params (list): A list of parameters to check.

    Raises:
        ValueError: If none of the parameters exist.
    """
    if not any(params):
        raise ValueError(f"Either {', '.join(names)} must be provided")


def validate_param(
    name: str,
    param: Union[bool, int, float, str],
    options: Union[
        List[Union[bool, int, float, str]], Tuple[Union[int, float], Union[int, float]]
    ],
):
    """
    Validates that a given parameter is one of the valid options or falls
    within a specified range.

    Args:
        name (str): The name of the parameter to validate.
        param (Union[bool, int, float, str]): The parameter to validate.
        options (Union[List[Union[bool, int, float, str]], Tuple[Union[int, float], Union[int, float]]]):
            A list of valid options or a tuple representing a range of valid integers/floats.

    Raises:
        ValueError:
            If the parameter is not one of the valid options or does not fall
            within the specified range.
    """
    if isinstance(options, tuple) and len(options) == 2:
        # Assume options is a range if it's a tuple of length 2
        start, end = options
        if param and not (start <= param <= end):
            raise ValueError(f"Invalid value: {name}. Valid range is: {start} to {end}")
    elif isinstance(options, list):
        if param not in options:
            raise ValueError(
                f"Invalid value: {name}. Valid options are: {', '.join(map(str, options))}"
            )
    else:
        raise ValueError(f"Invalid value and options provided for {name}")


def validate_hex(name: str, color: str) -> None:
    """
    Validates a hexadecimal color code.

    Args:
        name (str): The name of the parameter.
        color (str): The color code to validate.

    Raises:
        ValueError: If the color code is not a valid hexadecimal color code.
    """
    pattern = re.compile(r"^#[0-9a-fA-F]{6}$")
    if not pattern.match(color):
        raise ValueError(f"Invalid value: {name}. Hex color code provided: {color}")
