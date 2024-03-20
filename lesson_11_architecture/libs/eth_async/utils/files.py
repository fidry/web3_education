import os
import json


def join_path(path: str | tuple | list) -> str:
    if isinstance(path, str):
        return path
    return str(os.path.join(*path))


def read_json(path: str | tuple | list, encoding: str | None = None) -> list | dict:
    path = join_path(path)
    return json.load(open(path, encoding=encoding))


def touch(path: str | tuple | list, file: bool = False) -> bool:
    """
    Create an object (file or directory) if it doesn't exist.

    :param Union[str, tuple, list] path: path to the object
    :param bool file: is it a file?
    :return bool: True if the object was created
    """
    path = join_path(path)
    if file:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('')

            return True

        return False

    if not os.path.isdir(path):
        os.mkdir(path)
        return True

    return False


def write_json(path: str | tuple | list, obj: list | dict, indent: int | None = None,
               encoding: str | None = None) -> None:
    """
    Write Python list or dictionary to a JSON file.

    :param Union[str, tuple, list] path: path to the JSON file
    :param Union[list, dict] obj: the Python list or dictionary
    :param Optional[int] indent: the indent level
    :param Optional[str] encoding: the name of the encoding used to decode or encode the file
    """
    path = join_path(path)
    with open(path, mode='w', encoding=encoding) as f:
        json.dump(obj, f, indent=indent)
