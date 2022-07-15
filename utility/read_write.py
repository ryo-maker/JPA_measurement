"""read_writeはテキストファイル, CSVファイル, バイナリファイルを読み書きするためのモ
ジュールです. / This is a module that reads and writes text files, CSV files, 
and other binary files.


Available functions
-------------------
read_binary_file
    バイナリファイルを読み込む. / Load the binary file.

write_binary_file
    バイナリファイルを書き込む. / Write binary files.

read_text
    テキストファイルを読み込む. / Load text files.

write_text
    テキストファイルに書き込む. / Write text files.

read_csv
    CSVファイルを読み込む. / Load CSV files.

write_csv
    CSVファイルを書き込む. / Read CSV file.

read_json
    JSONファイルを読み込む. / Load JSON files.

write_json
    JSONファイルを書き込む. / Read JSON file.

read_pickle
    PICKLEファイルを読み込む. / Load PICKLE files.

write_pickle
    PICKLEファイルを書き込む. / Read PICKLE file.
"""


import csv
import codecs
import json
import os
import pickle
import struct
import numpy as np
from utility import CURRENT_PATH
from utility.logging_utility import get_normal_logger
from utility.others import get_args_of_current_function, get_time, transpose_list


__all__ = [
    "read_text",
    "write_text",
    "read_csv",
    "write_csv",
    "read_binary_file",
    "write_binary_file",
    "read_json",
    "write_json",
    "read_pickle",
    "write_pickle",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


def read_binary_file(
    binary_path,
    format_character="B",
    logger=None,
):
    """バイナリファイルを読み込む. / Load the binary file.

    Parameters
    ----------
    binary_path : str
        バイナリファイルのパス
    format_character : str, default: "B"
        フォーマット指定 / specification of the format
    logger : logging.Logger, default: None
        任意のロガー / any logger

    Returns
    -------
    tuple
        バイナリファイルの中身 / contents of the binary file
    """
    if logger == None:
        logger = get_normal_logger(logger_name="read_binary_file", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    with open(
        binary_path,
        mode="rb",
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ) as binary_file:
        binary_data = binary_file.read()
    binary_data_length = len(binary_data)
    format_character_size = struct.calcsize(format_character)
    if binary_data_length % format_character_size == 0:
        return struct.unpack(
            str(binary_data_length // format_character_size) + format_character,
            binary_data,
        )
    else:
        raise ValueError(
            "バイナリデータのサイズがフォーマット指定のサイズで割り切れません. / The size of binary data is not divisible by the size specified in the format."
        )


def write_binary_file(
    binary_data,
    binary_path=CURRENT_PATH,
    binary_name=None,
    addition=False,
    extension="",
    format_character="B",
    logger=None,
):
    """バイナリファイルを書き込む. / Write binary files.

    Parameters
    ----------
    binary_data : list or tuple
        バイナリファイルに書き込むデータ / data to be written to a binary file
    binary_path : str, default: CURRENT_PATH
        バイナリファイルのパス / path of binary file
    binary_name : str, default: None
        バイナリファイルの名前 / name of binary file
    addition : bool, default: False
        Trueのとき, ファイルが存在する場合は末尾に追記する. / If True, if the file 
        exists, it is appended to the end.
    extension : str, default: ""
        作成したファイルの拡張子 / extension of the created file
    format_character : str, default: "B"
        フォーマット指定 / specification of the format
        ------------------------------
        x - パティングバイト    -   - 値なし
        c - char               - 1 - 長さ1のバイト列
        b - signed char        - 1 - 整数
        B - unsigned char      - 1 - 整数
        ? - _Bool              - 1 - 真偽値型(bool)
        h - short              - 2 - 整数
        H - unsigned short     - 2 - 整数
        i - int                - 4 - 整数
        I - unsigned int       - 4 - 整数
        l - long               - 4 - 整数
        L - unsigned long      - 4 - 整数
        q - long long          - 8 - 整数
        Q - unsigned long long - 8 - 整数
        n - ssize_t            -   - 整数
        N - size_t             -   - 整数
        e -                    - 2 - 浮動小数点
        f - float              - 4 - 浮動小数点
        d - double             - 8 - 浮動小数点
        s - char[]             -   - bytes
        p - char[]             -   - bytes
        P - void *             -   - 整数
    logger : logging.Logger, default: None
        任意のロガー / any logger
    """
    if binary_name == None:
        binary_name = get_time()
    if logger == None:
        logger = get_normal_logger(logger_name="write_binary_file", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    if binary_path is None:
        folder_name = ("".join(extension.split("."))).upper()
        if folder_name == "":
            folder_name = "FILE"
        binary_path = CURRENT_PATH + "/DATA/" + folder_name
    os.makedirs(binary_path, exist_ok=True)
    if addition:
        with open(
            binary_path + "/" + binary_name + extension,
            mode="ab",
            buffering=-1,
            encoding=None,
            errors=None,
            newline=None,
            closefd=True,
            opener=None,
        ) as binary_file:
            if type(binary_data) == bytes:
                binary_file.write(binary_data)
            else:
                binary_file.write(
                    struct.pack(
                        "{0}{1}".format(len(binary_data), format_character),
                        *binary_data
                    )
                )
    else:
        with open(
            binary_path + "/" + binary_name + extension,
            mode="wb",
            buffering=-1,
            encoding=None,
            errors=None,
            newline=None,
            closefd=True,
            opener=None,
        ) as binary_file:
            if type(binary_data) == bytes:
                binary_file.write(binary_data)
            else:
                binary_file.write(
                    struct.pack(
                        "{0}{1}".format(len(binary_data), format_character),
                        *binary_data
                    )
                )


def read_text(
    text_path,
    encoding="utf-8",
    logger=None,
):
    """テキストファイルを読み込む. / Load text files.

    Parameters
    ----------
    text_path : str
        テキストファイルのパス / path of text file
    encoding : str, default: "utf-8"
        エンコーディング指定 / encoding of text file
    logger : logging.Logger, default: None
        任意のロガー / any logger

    Returns
    -------
    list
        テキストファイルの中身 / contents of the binary file
    """
    if logger == None:
        logger = get_normal_logger(logger_name="read_text", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    with open(
        text_path,
        mode="rt",
        buffering=-1,
        encoding=encoding,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ) as textfile:
        text = textfile.readlines()
    return [textline[:-1] if textline[-1:] == "\n" else textline for textline in text]


def write_text(
    text_data,
    text_path=CURRENT_PATH,
    text_name=None,
    addition=False,
    extension=".txt",
    encoding="utf-8",
    logger=None,
):
    """テキストファイルに書き込む. / Write text files.

    Parameters
    ----------
    text_data : list
        テキストファイルに書き込む文章 / text to be written to a text file
    text_path : str, default: CURRENT_PATH
        テキストファイルのパス / path of text file
    text_name : str, default: None
        テキストの名前 / name of text file
    addition : bool, default: False
        Trueのとき, ファイルが存在する場合は末尾に追記する. / If True, if the file 
        exists, it is appended to the end.
    extension : str, default: ".txt"
        テキストファイルの拡張子 / extension of text file
    encoding : str, default: "utf-8"
        エンコーディング指定 / encoding of text file
    logger : logging.Logger, default: None
        任意のロガー / any logger
    """
    if text_name == None:
        text_name = get_time()
    if logger == None:
        logger = get_normal_logger(logger_name="write_text", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    os.makedirs(text_path, exist_ok=True)
    if addition:
        print(
            *text_data,
            sep="\n",
            end="\n",
            file=codecs.open(text_path + "/" + text_name + extension, "a", encoding)
        )
    else:
        print(
            *text_data,
            sep="\n",
            end="\n",
            file=codecs.open(text_path + "/" + text_name + extension, "w", encoding)
        )


def read_csv(
    csv_path,
    header=(0, 0),
    transpose=True,
    dtype=None,
    encoding="utf-8",
    logger=None,
):
    """CSVファイルを読み込む. / Load CSV files.

    Parameters
    ----------
    csv_path : str
        CSVファイルのパス / path of CSV file
    header : tuple, default: (0, 0)
        headerとして読み飛ばす行数, 列数 / number of rows and columns to skip as header
    transpose : bool, default: True
        Trueのとき, 返値を転置する. / If True, transpose the return value.
    dtype : np.dtype
            numpy arrayのデータ型 / data type of array
    encoding : str, default: "utf-8"
        エンコーディング指定 / encoding of CSV file
    logger : logging.Logger, default: None
        任意のロガー / any logger

    Returns
    -------
    list
        CSVファイルの中身 / contents of CSV file
    """
    if logger == None:
        logger = get_normal_logger(logger_name="read_csv", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    with open(
        csv_path,
        mode="rt",
        buffering=-1,
        encoding=encoding,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ) as csvfile:
        reader = csv.reader(csvfile)
        return_data = [row[header[1] :] for row in reader][header[0] :]
    if dtype == None:
        if transpose:
            return_data = transpose_list(return_data)
        return return_data
    else:
        if transpose:
            return np.array(return_data, dtype=dtype).T
        else:
            return np.array(return_data, dtype=dtype)


def write_csv(
    csv_data,
    header=None,
    csv_path=CURRENT_PATH,
    csv_name=None,
    addition=False,
    transpose=True,
    encoding="utf-8",
    logger=None,
):
    """CSVファイルを書き込む. / Read CSV file.

    Parameters
    ----------
    data : np.ndarray or list
        CSVファイルに書き込むデータ / data to be written to the CSV file
    header : list, default: None
        1行目にheaderとして書き込む内容 / what to write in the first line as a header
    csv_path : str, default: CURRENT_PATH
        CSVファイルのパス / path of CSV file
    csv_name : str, default: None
        CSVファイルの名前 / name of CSV file
    addition : bool, default: False
        Trueのとき, ファイルが存在する場合は末尾に追記する. / If True, if the file 
        exists, it is appended to the end.
    transpose : bool, default: True
        Trueのとき, データを転置してから書き込む. / If True, transpose the written value.
    encoding : str, default: "utf-8"
        エンコーディング指定 / encoding of CSV file
    logger : logging.Logger, default: None
        任意のロガー / any logger
    """
    if csv_name == None:
        csv_name = get_time()
    if logger == None:
        logger = get_normal_logger(logger_name="write_csv", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    os.makedirs(csv_path, exist_ok=True)
    if transpose:
        csv_data = transpose_list(csv_data)
    else:
        csv_data = csv_data
    csv = []
    if header != None:
        csv.append(",".join([str(i) for i in header]))
    for row in csv_data:
        csv.append(",".join([str(i) for i in row]))
    if addition:
        print(
            *csv,
            sep="\n",
            end="\n",
            file=codecs.open(csv_path + "/" + csv_name + ".csv", "a", encoding)
        )
    else:
        print(
            *csv,
            sep="\n",
            end="\n",
            file=codecs.open(csv_path + "/" + csv_name + ".csv", "w", encoding)
        )


def read_json(
    json_path,
    encoding="utf-8",
    logger=None,
):
    """JSONファイルを読み込む. / Load JSON files.

    Parameters
    ----------
    json_path : str
        JSONファイルのパス / path of JSON file
    encoding : str, default: "utf-8"
        エンコーディング指定 / encoding of JSON file
    logger : logging.Logger, default: None
        任意のロガー / any logger

    Returns
    -------
    list
        JSONファイルの中身 / contents of JSON file
    """
    if logger == None:
        logger = get_normal_logger(logger_name="read_json", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    with open(
        json_path,
        mode="r",
        buffering=-1,
        encoding=encoding,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ) as json_file:
        return json.load(json_file)


def write_json(
    json_data,
    json_path=CURRENT_PATH,
    json_name=None,
    addition=False,
    encoding="utf-8",
    logger=None,
):
    """JSONファイルを書き込む. / Read JSON file.

    Parameters
    ----------
    json_data : np.ndarray or list
        JSONファイルに書き込むデータ / data to be written to the JSON file
    json_path : str, default: CURRENT_PATH
        JSONファイルのパス / path of JSON file
    json_name : str, default: None
        JSONファイルの名前 / name of JSON file
    addition : bool, default: False
        Trueのとき, ファイルが存在する場合は末尾に追記する. / If True, if the file 
        exists, it is appended to the end.
    encoding : str, default: "utf-8"
        エンコーディング指定 / encoding of JSON file
    logger : logging.Logger, default: None
        任意のロガー / any logger
    """
    if json_name == None:
        json_name = get_time()
    if logger == None:
        logger = get_normal_logger(logger_name="write_json", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    os.makedirs(json_path, exist_ok=True)
    if addition:
        if os.path.exists(json_path + "/" + json_name + ".json"):
            try:
                written_data = read_json(
                    json_path + "/" + json_name + ".json", encoding=encoding
                )
                written_data.update(json_data)
                json_data.update(written_data)
            except json.decoder.JSONDecodeError:
                pass
        with open(
            json_path + "/" + json_name + ".json",
            mode="w",
            buffering=-1,
            encoding=encoding,
            errors=None,
            newline=None,
            closefd=True,
            opener=None,
        ) as json_file:
            json.dump(json_data, json_file, indent=4)
    else:
        with open(
            json_path + "/" + json_name + ".json",
            mode="w",
            buffering=-1,
            encoding=encoding,
            errors=None,
            newline=None,
            closefd=True,
            opener=None,
        ) as json_file:
            json.dump(json_data, json_file, indent=4)


def read_pickle(
    pickle_path, logger=None
):
    """PICKLEファイルを読み込む. / Load PICKLE files.

    Parameters
    ----------
    pickle_path : str
        PICKLEファイルのパス / path of PICKLE file
    logger : logging.Logger, default: None
        任意のロガー / any logger

    Returns
    -------
    object
        PICKLEファイルの中身 / contents of PICKLE file
    """
    if logger == None:
        logger = get_normal_logger(logger_name="read_pickle", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    with open(pickle_path, mode="rb") as pickle_file:
        return pickle.load(pickle_file)


def write_pickle(
    pickle_data,
    pickle_path=CURRENT_PATH,
    pickle_name=None,
    logger=None,
):
    """PICKLEファイルを書き込む. / Read PICKLE file.

    Parameters
    ----------
    pickle_data : np.ndarray or list
        PICKLEファイルに書き込むデータ / data to be written to the PICKLE file
    pickle_path : str, default: CURRENT_PATH
        PICKLEファイルのパス / path of PICKLE file
    pickle_name : str, default: None
        PICKLEファイルの名前 / name of PICKLE file
    logger : logging.Logger, default: None
        任意のロガー / any logger
    """
    if pickle_name == None:
        pickle_name = get_time()
    if logger == None:
        logger = get_normal_logger(logger_name="write_pickle", level="info")
    logger.debug("Parameter:{}".format(get_args_of_current_function()))
    os.makedirs(pickle_path, exist_ok=True)
    with open(
        "{0}/{1}.pickle".format(pickle_path, pickle_name), mode="wb"
    ) as pickle_file:
        pickle.dump(pickle_data, pickle_file)
