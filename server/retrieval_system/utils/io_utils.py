# YAML utility functions (`yaml_save`, `yaml_load`) were took from ultralytics with modification
# Link: https://github.com/ultralytics/ultralytics/blob/c3c27b019a9516a9b2c78c291b61ef7cf97ff7f3/ultralytics/utils/__init__.py#L285

import json
import os
import re
from collections import OrderedDict
from pathlib import Path

import yaml


def __yaml_save(file="data.yaml", data=None):
    """
    Save YAML data to a file.

    Args:
        file (str, optional): File name. Default is 'data.yaml'.
        data (dict): Data to save in YAML format.

    Returns:
        (None): Data is saved to the specified file.
    """
    if data is None:
        data = {}
    file = Path(file)
    if not file.parent.exists():
        # Create parent directories if they don't exist
        file.parent.mkdir(parents=True, exist_ok=True)

    # Convert Path objects to strings
    for k, v in data.items():
        if isinstance(v, Path):
            data[k] = str(v)

    # Dump data to file in YAML format
    with open(file, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def __yaml_load(file="data.yaml", append_filename=False):
    """
    Load YAML data from a file.

    Args:
        file (str, optional): File name. Default is 'data.yaml'.
        append_filename (bool): Add the YAML filename to the YAML dictionary. Default is False.

    Returns:
        (dict): YAML data and file name.
    """
    with open(file, errors="ignore", encoding="utf-8") as f:
        s = f.read()  # string

        # Remove special characters
        if not s.isprintable():
            s = re.sub(
                r"[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+",
                "",
                s,
            )

        # Add YAML filename to dict and return
        return (
            {**yaml.safe_load(s), "yaml_file": str(file)}
            if append_filename
            else yaml.safe_load(s)
        )


def load_yaml_to_dict(filename: str) -> dict:
    return __yaml_load(filename)


def load_json_to_dict(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f)


def load_json_to_ordered_dict(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def save_dict_to_yaml(filename: str, data: dict) -> None:
    __yaml_save(file=filename, data=data)


def save_dict_to_json(filename: str, data: dict) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)


def get_filename(filename: str) -> str:
    return os.path.basename(filename)


def get_filename_without_ext(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]
