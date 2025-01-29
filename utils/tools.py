from yaml import safe_load
import os


def load_yml(filepath: str) -> dict:
    """
    Load a YAML file and return its contents as a dictionary.

    Args:
        filepath (str): The path to the YAML file to be loaded.

    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        with open(filepath, "r") as file:
            data = safe_load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file '{filepath}' was not found. Please check the path and try again."
        )


def filename_from_path(path: str) -> str:
    """
    Extract the filename from a given file path.

    Args:
        path (str): The full path to the file.

    Returns:
        str: The filename extracted from the given path.
    """
    return os.path.basename(path)
