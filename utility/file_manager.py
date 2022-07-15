"""file_managerはディレクトリの情報を取得, 操作するモジュールです. / This is a 
module that acquires and operates information of directory.


Available functions
-------------------
class: JsonFileManager
    Class wrapping JSON file

    variables:
        json_file_path
            JSONファイルのパス / path of JSON file

    methods:
        __init__
            JSONファイルを読み込む / load JSON file
        load_json_file
            JSONファイルを読み込む / load JSON file
        save_setting
            JSONファイルにデータを書き込む / load JSON file

get_file_folder_path_list
    ファイルとフォルダのパスのリストを返す. / Returns a list of paths for files 
    and folders.

get_all_file_folder_path_list
    ファイルとフォルダのパスのリストを返す.(フォルダの中身も含む) / Returns a list 
    of paths for files and folders. (Including folder contents)

get_folder_path_list
    フォルダのパスのリストを返す. / Returns a list of paths for folders.

get_all_folder_path_list
    フォルダのパスのリストを返す.(フォルダの中身も含む) / Returns a list of paths 
    for folders. (Including folder contents)

get_file_path_list
    ファイルのパスのリストを返す. / Returns a list of paths for files.

get_all_file_path_list
    ファイルのパスのリストを返す.(フォルダの中身も含む) / Returns a list of paths 
    for files. (Including folder contents)

move_file
    ファイルを移動させる. / Move a file.

copy_file
    ファイルをコピーする. / Copy a file.

move_folder
   フォルダをコピーする. / Copy a folder.

copy_folder
    フォルダをコピーする. / Copy a folder.

arrange_folder
    フォルダの中身を整理する. / Arrange the contents of the folder.

delete_all_empty_folder
    空のフォルダーをすべて削除する. / Delete all empty folders.

delete_same_files
    フォルダ内の同じデータのファイルを削除する. / Delete the files with the same 
    data in the folder.

arrange_file_name
    フォルダ内のファイル名を調整する. / Adjust the file name in the folder.

get_new_file_name
    新しいファイル名を取得する / get new file name
"""


import gc
import os
import pathlib
import shutil
from utility.constants import EXTENSION_DICT
from utility.logging_utility import get_normal_logger
from utility.others import (
    get_args_of_current_function,
    get_directory_path,
    get_program_name,
    sort_based_on_a_list,
    generate_a_random_string,
)
from utility.read_write import read_json, write_json


__all__ = [
    "JsonFileManager",
    "get_file_folder_path_list",
    "get_all_file_folder_path_list",
    "get_folder_path_list",
    "get_all_folder_path_list",
    "get_file_path_list",
    "get_all_file_path_list",
    "move_file",
    "copy_file",
    "move_folder",
    "copy_folder",
    "arrange_folder",
    "delete_all_empty_folder",
    "delete_same_files",
    "arrange_file_name",
    "get_new_file_name",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


class JsonFileManager:
    def __init__(self, json_file_path):
        """JSONファイルを読み込む / load JSON file
        
        Parameters
        ----------
        json_file_path : str
            読み込むJSONファイルのパス / path of JSON file to load
        """
        self.json_file_path = json_file_path
        self.load_json_file(self.json_file_path)

    def load_json_file(self, json_file_path):
        """JSONファイルを読み込む / load JSON file
        
        Parameters
        ----------
        json_file_path : str
            読み込むJSONファイルのパス / path of JSON file to load
        """
        self.json_file_path = json_file_path or self.json_file_path
        if os.path.exists(self.json_file_path):
            self.json_data = read_json(json_path=self.json_file_path)
        else:
            self.json_data = {}

    def save_setting(self, key, value):
        """JSONファイルにデータを書き込む / write data to JSON file"""
        json_folder_path = get_directory_path(self.json_file_path)
        json_name = get_program_name(self.json_file_path)
        write_json(
            json_data={key: value,},
            json_path=json_folder_path,
            json_name=json_name,
            addition=True,
        )


def get_file_folder_path_list(
    path,
    logger=get_normal_logger(logger_name="get_file_folder_path_list", level="info"),
):
    """ファイルとフォルダのパスのリストを返す. / Returns a list of paths for files 
    and folders.

    Parameters
    ----------
    path : str
        リストを取得するパス / path to get the list
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger

    Returns
    -------
    list
        ファイルとフォルダのパスのリスト / list of file and folder paths
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    return [
        file_folder_path.absolute()
        for file_folder_path in list(pathlib.Path(path).glob("*"))
    ]


def get_all_file_folder_path_list(
    path,
    logger=get_normal_logger(logger_name="get_all_file_folder_path_list", level="info"),
):
    """ファイルとフォルダのパスのリストを返す.(フォルダの中身も含む) / Returns a 
    list of paths for files and folders. (Including folder contents)

    Parameters
    ----------
    path : str
        リストを取得するパス / path to get the list
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger

    Returns
    -------
    list
        ファイルとフォルダのパスのリスト / list of file and folder paths
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    return [
        file_folder_path.absolute()
        for file_folder_path in list(pathlib.Path(path).glob("**/*"))
    ]


def get_folder_path_list(
    path, logger=get_normal_logger(logger_name="get_folder_path_list", level="info")
):
    """フォルダのパスのリストを返す. / Returns a list of paths for folders.

    Parameters
    ----------
    path : str
        リストを取得するパス / path to get the list
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger

    Returns
    -------
    list
        フォルダのパスのリスト / list of folder paths
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    return [
        folder_path.absolute()
        for folder_path in list(pathlib.Path(path).glob("*"))
        if folder_path.is_dir()
    ]


def get_all_folder_path_list(
    path, logger=get_normal_logger(logger_name="get_all_folder_path_list", level="info")
):
    """フォルダのパスのリストを返す.(フォルダの中身も含む) / Returns a list of 
    paths for folders. (Including folder contents)

    Parameters
    ----------
    path : str
        リストを取得するパス / path to get the list
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger

    Reterns
    -------
    list
        フォルダのパスのリスト / list of folder paths
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    return [
        folder_path.absolute()
        for folder_path in list(pathlib.Path(path).glob("**/*"))
        if folder_path.is_dir()
    ]


def get_file_path_list(
    path,
    extension=None,
    logger=get_normal_logger(logger_name="get_file_path_list", level="info"),
):
    """ファイルのパスのリストを返す. / Returns a list of paths for files.

    Parameters
    ----------
    path : str
        リストを取得するパス / path to get the list
    extension : str, default: None
        指定の拡張子 / specified extension
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger

    Returns
    -------
        ファイルのパスのリスト / list of file paths
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    if extension == None:
        return [
            file_path.absolute()
            for file_path in list(pathlib.Path(path).glob("*"))
            if file_path.is_file()
        ]
    else:
        return [
            file_path.absolute()
            for file_path in list(pathlib.Path(path).glob("*"))
            if file_path.is_file() and file_path.suffix == extension
        ]


def get_all_file_path_list(
    path,
    extension=None,
    logger=get_normal_logger(logger_name="get_all_file_path_list", level="info"),
):
    """ファイルのパスのリストを返す.(フォルダの中身も含む) / Returns a list of 
    paths for files. (Including folder contents)

    Parameters
    ----------
    path : str
        リストを取得するパス / path to get the list
    extension : str, default: None
        指定の拡張子 / specified extension
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger

    Reterns
    -------
        ファイルのパスのリスト / list of file paths
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    if extension == None:
        return [
            file_path.absolute()
            for file_path in list(pathlib.Path(path).glob("**/*"))
            if file_path.is_file()
        ]
    else:
        return [
            file_path.absolute()
            for file_path in list(pathlib.Path(path).glob("**/*"))
            if file_path.is_file() and file_path.suffix == extension
        ]


def move_file(
    path1,
    path2,
    overwrite=False,
    logger=get_normal_logger(logger_name="move_file", level="info"),
):
    """ファイルを移動させる. / Move a file.

    Parameters
    ----------
    path1 : str
        コピー元 / copy source
    path2 : str
        コピー先 / copy destination
    overwrite : bool, default: False
        Trueのときファイルを上書きする. / If true, overwrite the file.
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path1 == None or path2 == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    path1 = pathlib.Path(path1)
    path2 = pathlib.Path(path2)
    path2.mkdir(exist_ok=True)
    path2 = path2 / path1.name
    if str(path1) != str(path2):
        if overwrite:
            if path2.exists():
                path2.unlink()
                logger.info("{}を削除しました.".format(path2))
            shutil.move(path1, path2)
            logger.info("{0}を{1}に移動させました. / Moved {0} to {1}.".format(path1, path2))
        else:
            continuation = True
            counter = 1
            while continuation:
                if path2.exists():
                    try:
                        f = open(path1, mode="rb")
                        binary_data1 = f.read()
                        f.close()
                        f = open(path2, mode="rb")
                        binary_data2 = f.read()
                        f.close()
                    except MemoryError:
                        binary_data1 = path1.stat().st_mtime
                        binary_data2 = path2.stat().st_mtime
                    if binary_data1 != binary_data2:
                        path2 = path2.parent / pathlib.Path(
                            path1.stem + "({})".format(counter) + path1.suffix
                        )
                        counter += 1
                    else:
                        path1.unlink()
                        logger.info("{}を削除しました.".format(path1))
                        continuation = False
                else:
                    shutil.move(path1, path2)
                    logger.info(
                        "{0}を{1}に移動させました. / Moved {0} to {1}.".format(path1, path2)
                    )
                    continuation = False


def copy_file(
    path1,
    path2,
    overwrite=False,
    logger=get_normal_logger(logger_name="copy_file", level="info"),
):
    """ファイルをコピーする. / Copy a file.

    Parameters
    ----------
    path1 : str
        コピー元 / copy source
    path2 : str
        コピー先 / copy destination
    overwrite : bool, default: False
        Trueのときファイルを上書きする. / If true, overwrite the file.
    excepted_extension : list, default: []
        除外する拡張子 / excluded extensions
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path1 == None or path2 == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    path1 = pathlib.Path(path1)
    path2 = pathlib.Path(path2)
    path2.mkdir(exist_ok=True)
    path2 = path2 / path1.name
    if str(path1) != str(path2):
        if overwrite:
            if path2.exists():
                path2.unlink()
                logger.info("{}を削除しました.".format(path2))
            shutil.copy2(path1, path2)
            logger.info("{0}を{1}にコピーしました. / Moved {0} to {1}.".format(path1, path2))
        else:
            continuation = True
            counter = 1
            while continuation:
                if path2.exists():
                    try:
                        f = open(path1, mode="rb")
                        binary_data1 = f.read()
                        f.close()
                        f = open(path2, mode="rb")
                        binary_data2 = f.read()
                        f.close()
                    except MemoryError:
                        binary_data1 = path1.stat().st_mtime
                        binary_data2 = path2.stat().st_mtime
                    if binary_data1 != binary_data2:
                        path2 = path2.parent / pathlib.Path(
                            path1.stem + "({})".format(counter) + path1.suffix
                        )
                        counter += 1
                    else:
                        continuation = False
                    del binary_data1
                    del binary_data2
                    gc.collect()
                else:
                    shutil.copy2(path1, path2)
                    logger.info(
                        "{0}を{1}にコピーしました. / Copy {0} to {1}.".format(path1, path2)
                    )
                    continuation = False


def move_folder(
    path1,
    path2,
    overwrite=False,
    excepted_extension=[],
    logger=get_normal_logger(logger_name="copy_folder", level="info"),
):
    """フォルダをコピーする. / Copy a folder.

    Parameters
    ----------
    path1 : str
        コピー元 / copy source
    path2 : str
        コピー先 / copy destination
    overwrite : bool, default: False
        Trueのときファイルを上書きする. / If true, overwrite the file.
    excepted_extension : list, default: []
        除外する拡張子 / excluded extensions
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path1 == None or path2 == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    path1 = pathlib.Path(path1)
    path2 = pathlib.Path(path2)
    path2.mkdir(exist_ok=True)
    for file_path in get_file_path_list(str(path1), logger=logger):
        if str(file_path.suffix) not in excepted_extension:
            move_file(
                str(file_path),
                str(path2 / path1.name),
                overwrite=overwrite,
                logger=logger,
            )
    for folder_path in get_folder_path_list(str(path1)):
        move_folder(
            str(folder_path),
            str(path2 / path1.name),
            overwrite=overwrite,
            excepted_extension=excepted_extension,
            logger=logger,
        )


def copy_folder(
    path1,
    path2,
    overwrite=False,
    excepted_extension=[],
    logger=get_normal_logger(logger_name="copy_folder", level="info"),
):
    """フォルダをコピーする. / Copy a folder.

    Parameters
    ----------
    path1 : str
        コピー元 / copy source
    path2 : str
        コピー先 / copy destination
    overwrite : bool, default: False
        Trueのときファイルを上書きする. / If true, overwrite the file.
    excepted_extension : list, default: []
        除外する拡張子 / excluded extensions
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path1 == None or path2 == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    path1 = pathlib.Path(path1)
    path2 = pathlib.Path(path2)
    path2.mkdir(exist_ok=True)
    for file_path in get_file_path_list(str(path1), logger=logger):
        if str(file_path.suffix) not in excepted_extension:
            copy_file(
                str(file_path),
                str(path2 / path1.name),
                overwrite=overwrite,
                logger=logger,
            )
    for folder_path in get_folder_path_list(str(path1)):
        copy_folder(
            str(folder_path),
            str(path2 / path1.name),
            overwrite=overwrite,
            excepted_extension=excepted_extension,
            logger=logger,
        )


def arrange_folder(
    path,
    excepted_extension=[],
    logger=get_normal_logger(logger_name="arrange_folder", level="info"),
):
    """フォルダの中身を整理する. / Arrange the contents of the folder.

    Parameters
    ----------
    path : str
        パス / path where the function is executed
    excepted_extension : list, default: []
        除外する拡張子 / excluded extensions
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    for file_path in get_all_file_path_list(str(path), logger=logger):
        if file_path.suffix not in excepted_extension:
            if file_path.suffix in EXTENSION_DICT.keys():
                move_file(
                    str(file_path),
                    str(path) + "/" + EXTENSION_DICT[file_path.suffix],
                    logger=logger,
                )
            else:
                move_file(
                    str(file_path),
                    str(path) + "/" + file_path.suffix[1:].upper(),
                    logger=logger,
                )


def delete_all_empty_folder(
    path, logger=get_normal_logger(logger_name="delete_all_empty_folder", level="info")
):
    """空のフォルダーをすべて削除する. / Delete all empty folders.

    Parameters
    ----------
    path : str
        パス / path where the function is executed
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    continuation = True
    while continuation:
        continuation = False
        for folder_path in get_all_folder_path_list(str(path), logger=logger):
            if get_file_folder_path_list(str(folder_path), logger=logger) == []:
                continuation = True
                logger.info("{}を削除しました.".format(folder_path))
                folder_path.rmdir()


def delete_same_files(
    path, logger=get_normal_logger(logger_name="delete_same_files", level="info")
):
    """フォルダ内の同じデータのファイルを削除する. / Delete the files with the same data in the folder.

    Parameters
    ----------
    path : str
        パス / path where the function is executed
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    folder_path_list = get_all_folder_path_list(str(path), logger=logger)
    folder_path_list.append(pathlib.Path(path))
    for folder_path in folder_path_list:
        file_path_list = get_file_path_list(str(folder_path), logger=logger)
        file_size_dict = {}
        for file_path in file_path_list:
            if file_path.stat().st_size not in file_size_dict.keys():
                file_size_dict[file_path.stat().st_size] = []
            file_size_dict[file_path.stat().st_size].append(file_path)
        for file_path_list in file_size_dict.values():
            checked_file_path_list = []
            larged_file_path_list = []
            for file_path1 in file_path_list:
                if (
                    file_path1.exists()
                    and (file_path1 not in checked_file_path_list)
                    and (file_path1 not in larged_file_path_list)
                ):
                    binary_data1_size = file_path1.stat().st_size
                    for file_path2 in file_path_list:
                        if (
                            file_path2.exists()
                            and (file_path2 not in checked_file_path_list)
                            and (file_path2 not in larged_file_path_list)
                            and (file_path1 != file_path2)
                        ):
                            binary_data2_size = file_path2.stat().st_size
                            if binary_data2_size == binary_data1_size:
                                try:
                                    f = open(file_path1, mode="rb")
                                    binary_data1 = f.read()
                                    f.close()
                                    try:
                                        f = open(file_path2, mode="rb")
                                        binary_data2 = f.read()
                                        f.close()
                                    except MemoryError:
                                        logger.warning(
                                            "{0}は大きいファイルのため, 読み込むことができません. / Unable to read because {0} is a large file.".format(
                                                file_path2
                                            )
                                        )
                                        larged_file_path_list.append(file_path2)
                                        gc.collect()
                                    else:
                                        if binary_data1 == binary_data2:
                                            file_path2.unlink()
                                            logger.info("{}を削除しました.".format(file_path2))
                                        del binary_data1
                                        del binary_data2
                                        gc.collect()
                                except MemoryError:
                                    logger.warning(
                                        "{0}は大きいファイルのため, 読み込むことができません. / Unable to read because {0} is a large file.".format(
                                            file_path1
                                        )
                                    )
                                    larged_file_path_list.append(file_path1)
                                    gc.collect()
                    checked_file_path_list.append(file_path1)
                    gc.collect()


def arrange_file_name(
    path, logger=get_normal_logger(logger_name="arrange_file_name", level="info")
):
    """フォルダ内のファイル名を調整する. / Adjust the file name in the folder.

    Parameters
    ----------
    path : str
        パス / path where the function is executed
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if path == None:
        raise ValueError("NoneTypeはパスとして使用できません. / NoneType cannot be used as a path.")
    folder_path_list = get_all_folder_path_list(path)
    folder_path_list.append(pathlib.Path(path))
    for folder_path in folder_path_list:
        file_path_dict = {}
        file_path_list = get_file_path_list(folder_path)
        for file_path in file_path_list:
            file_path_ = get_new_file_name(file_path)
            if file_path_ not in file_path_dict.keys():
                file_path_dict[file_path_] = []
            file_path_dict[file_path_].append(file_path)
        for file_path in file_path_dict.keys():
            file_path_list = file_path_dict[file_path]
            file_path_list = sort_based_on_a_list(
                file_path_list,
                (file_path.stat().st_mtime for file_path in file_path_list),
            )
            for index in range(len(file_path_list)):
                if index == 0:
                    new_file_path = file_path
                    if new_file_path.is_file():
                        if file_path_list[index] != new_file_path:
                            new_file_name = generate_a_random_string(16)
                            file_path_list[file_path_list.index(new_file_path)] = (
                                new_file_path.parent / new_file_name
                            )
                            new_file_path.rename(
                                "{0}\\{1}".format(new_file_path.parent, new_file_name)
                            )
                            logger.info(
                                "ファイル名{0}を{1}に変更しました.".format(
                                    new_file_path,
                                    "{0}\\{1}".format(
                                        new_file_path.parent, new_file_name
                                    ),
                                )
                            )

                            file_path_list[index].rename(new_file_path)
                            logger.info(
                                "ファイル名{0}を{1}に変更しました.".format(
                                    file_path_list[index], new_file_path
                                )
                            )
                    else:
                        file_path_list[index].rename(new_file_path)
                        logger.info(
                            "ファイル名{0}を{1}に変更しました.".format(
                                file_path_list[index], new_file_path
                            )
                        )
                else:
                    new_file_path = pathlib.Path(
                        "{0}\\{1}{2}{3}".format(
                            file_path.parent,
                            file_path.stem,
                            "({})".format(index - 1),
                            file_path.suffix,
                        )
                    )
                    if new_file_path.is_file():
                        if file_path_list[index] != new_file_path:
                            new_file_name = generate_a_random_string(16)
                            file_path_list[file_path_list.index(new_file_path)] = (
                                new_file_path.parent / new_file_name
                            )
                            new_file_path.rename(
                                "{0}\\{1}".format(new_file_path.parent, new_file_name)
                            )
                            logger.info(
                                "ファイル名{0}を{1}に変更しました.".format(
                                    new_file_path,
                                    "{0}\\{1}".format(
                                        new_file_path.parent, new_file_name
                                    ),
                                )
                            )

                            file_path_list[index].rename(new_file_path)
                            logger.info(
                                "ファイル名{0}を{1}に変更しました.".format(
                                    file_path_list[index], new_file_path
                                )
                            )
                    else:
                        file_path_list[index].rename(new_file_path)
                        logger.info(
                            "ファイル名{0}を{1}に変更しました.".format(
                                file_path_list[index], new_file_path
                            )
                        )


def get_new_file_name(file_path):
    """新しいファイル名を取得する / get new file name
    
    Parameters
    ----------
    file_path : str
        ファイルパス
    """
    file_path = pathlib.Path(file_path)
    flag0 = True
    index = -1
    while flag0:
        carry_out_flag1 = False
        carry_out_flag2 = False
        try:
            if file_path.stem[index] == ")":
                flag1 = True
                index -= 1
                while flag1:
                    if file_path.stem[index] in "0123456789":
                        carry_out_flag1 = True
                        index -= 1
                    else:
                        flag1 = False
                if file_path.stem[index] == "(":
                    carry_out_flag2 = True
                    flag2 = True
                    index -= 1
                    while flag2:
                        if file_path.stem[index] == " ":
                            index -= 1
                        else:
                            flag2 = False
                else:
                    flag0 = False
            else:
                flag0 = False
        except IndexError:
            flag0 = False
        if carry_out_flag1 and carry_out_flag2:
            file_path = pathlib.Path(
                "{0}/{1}{2}".format(
                    file_path.parent, file_path.stem[: index + 1], file_path.suffix
                )
            )
    return file_path
