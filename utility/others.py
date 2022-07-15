"""othersは汎用の関数が格納されたモジュールです. / This is a module that stores general-purpose modules.


Available functions
-------------------
beep
    ビープ音を鳴らす. / Make a beep.

transpose_list
    2次元配列を転置する. / Transpose a two-dimensional array.

make_str_int
    小数または整数を任意の桁数で丸め, 文字列で返す. / Round a decimal or integer by any number of digits and return a string.

get_time
    時刻を取得し, 文字列に直す. / Get the time and convert it to a string.

get_variable_name
    変数名を取得する. / Get the name of a variable.

check_variable
    変数名を表示する. / Print the name of the variable.

get_args_of_current_function
    関数の引数とその値を取得する. / Get function arguments and their values.

get_directory_path
    引数のパスを絶対パスにし, 親ディレクトリのパスを返す. / Make the path of the argument an absolute path and return the path of the parent directory.

get_program_name
    引数のパスのファイル名を取得する. / Get the file name of the argument path.

select_file
    処理ファイルをGUIから選択し, その絶対パスを返す. / Select a processing file from the GUI and return its absolute path.

select_folder
    処理フォルダーをGUIから選択し, その絶対パスを返す. / Select a processing folder from the GUI and return its absolute path.

get_yes_or_no
    YesかNoが入力するまで質問を繰り返す. / Repeat the question until you enter Yes or No.

series
    級数を計算し, 結果を返す. / Calculates a series and returns the result.

significant digits
    引数valueを有効数字が引数digitになるように丸めて返す． / Rounds the argument value so that the significant digits become the argument digit and returns it.

sort_based_on_a_list
    あるリストを基準にソートする / sort based on a list

generate_a_random_string
    任意の長さのランダムな文字列を生成する / generate a random string of arbitrary length
"""


import itertools
import os
import platform
import random
import string
import time
from tkinter import filedialog, Tk
from datetime import datetime
from inspect import currentframe, getargvalues
from utility import CURRENT_PATH
from utility.constants import EXTENSION_DICT


__all__ = [
    "beep",
    "transpose_list",
    "make_str_int",
    "get_time",
    "get_variable_name",
    "check_variable",
    "get_args_of_current_function",
    "get_directory_path",
    "get_program_name",
    "select_file",
    "select_folder",
    "get_yes_or_no",
    "series",
    "significant_digits",
    "sort_based_on_a_list",
    "generate_a_random_string",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


def beep(frequency=1000, length=0.25, interval=0.5, times=1):
    """ビープ音を鳴らす. / Make a beep.

    Parameters
    ----------
    frequency : float or int, default: 1000
        ビープ音の周波数(単位:Hz) / frequency of beep(unit:Hz)
    length : float or int, default: 0.25
        ビープ音の長さ(単位:s) / length of beep(unit:s)
    interval : float or int, default: 0.5
        ビープ音の間隔(単位:s) / interval of beep(unit:s)
    times : int, default: 1
        ビープ音を鳴らす回数(単位:回) / number of times to make a beep
    """
    for _ in range(times):
        if platform.system() == "Windows":
            import winsound

            winsound.Beep(frequency, round(length * 1000.0))
        else:
            import os

            os.system("play -n synth %s sin %s" % (length, frequency))
        time.sleep(interval)


def transpose_list(data):
    """2次元配列を転置する. / Transpose a two-dimensional array.

    Parameters
    ----------
    data : np.ndarray or list
        元の2次元配列 / original two-dimensional array

    Returns
    -------
    np.ndarray or list
        転置された配列 / transposed two-dimensional array
    """
    len_list = [len(row) for row in data]
    max_index = len_list.index(max(len_list))
    return [
        [row[line] if len(row) > line else "" for row in data]
        for line in range(len(data[max_index]))
    ]


def make_str_int(value, digit, column=5):
    """小数または整数を任意の桁数で丸め, 文字列で返す. / Round a decimal or integer 
    by any number of digits and return a string.

    Parameters
    ----------
    value : float or int
        小数若しくは整数 / decimal or whole number
    digit : int
        文字数 / number of characters
    column : int, default: 5
        丸めの桁数 / number of rounding digits

    Returns
    -------
    str
        任意の桁数で丸められた数字の文字列 / decimal or integer by any number of 
        digits and return a string
    """
    res = str(int(round(value, column)))
    while True:
        if len(res) < digit:
            res = "0" + res
        else:
            break
    return res


def get_time():
    """時刻を取得し, 文字列に直す. / Get the time and convert it to a string.

    Returns
    -------
    str
        時刻 / time
    """
    time_now = datetime.now()
    return (
        make_str_int(time_now.year, 4)
        + "_"
        + make_str_int(time_now.month, 2)
        + "_"
        + make_str_int(time_now.day, 2)
        + "_"
        + make_str_int(time_now.hour, 2)
        + "_"
        + make_str_int(time_now.minute, 2)
        + "_"
        + make_str_int(time_now.second, 2)
        + "_"
        + make_str_int(time_now.microsecond, 6)
    )


def get_variable_name(variable):
    """変数名を取得する. / Get the name of a variable.

    Parameters
    ----------
    variable : any type variable of Python
        変数

    Returns
    -------
    str
        変数名
    """
    names = {id(v): k for k, v in currentframe().f_back.f_locals.items()}
    return names.get(id(variable), "???")


def check_variable(variable, logger=None):
    """変数名を表示する. / Print the name of the variable.

    Parameters
    ----------
    variable : any type variable of Python
        変数
    logger : logging.Logger, default: None
        任意のロガー / any logger
    """
    if logger == None:
        print(
            "name:{0}, type:{1}, value:{2}".format(
                " or ".join(
                    [
                        key
                        for key, value in currentframe().f_back.f_locals.items()
                        if id(value) == id(variable)
                    ]
                ),
                type(variable),
                variable,
            )
        )
    else:
        logger.debug(
            "name:{0}, type:{1}, value:{2}".format(
                " or ".join(
                    [
                        key
                        for key, value in currentframe().f_back.f_locals.items()
                        if id(value) == id(variable)
                    ]
                ),
                type(variable),
                variable,
            )
        )


def get_args_of_current_function():
    """関数の引数とその値を取得する. / Get function arguments and their values.

    Returns
    -------
    dict
        関数の引数と値 / function arguments and values
    """
    arguments_information = getargvalues(currentframe().f_back)
    arguments_dict = {
        argument_name: arguments_information.locals[argument_name]
        for argument_name in arguments_information.args
    }
    return_dict = {}
    for argument_key in arguments_dict.keys():
        if argument_key == "self":
            pass
        elif isinstance(
            arguments_dict[argument_key], (bool, int, float, str, type(None))
        ):
            return_dict[argument_key] = arguments_dict[argument_key]
        else:
            return_dict[argument_key] = type(arguments_dict[argument_key])
    return return_dict


def get_directory_path(path):
    """引数のパスを絶対パスにし, 親ディレクトリのパスを返す. / Make the path of the 
    argument an absolute path and return the path of the parent directory.

    Parameters
    ----------
    path : str
        パス / path

    Returns
    -------
    str - パス / path
    """
    return os.path.dirname(os.path.abspath(path))


def get_program_name(path):
    """引数のパスのファイル名を取得する. / Get the file name of the argument path.

    Parameters
    ----------
    path : str
        パス / path

    Returns
    -------
    str
        ファイルの名前 / name of file
    """
    return os.path.splitext(os.path.basename(os.path.abspath(path)))[0]


def select_file(initial_directory=CURRENT_PATH, extension=None):
    """処理ファイルをGUIから選択し, その絶対パスを返す. / Select a processing file 
    from the GUI and return its absolute path.

    Parameters
    ----------
    initial_directory : str, default: CURRENT_PATH
        最初に開くディレクトリ / first directory to open
    extension : str or list, default: None
        抽出するファイルの拡張子 / file extension to extract

    Returns
    -------
    str
        パス / path
    """
    root_window = Tk()
    root_window.attributes("-topmost", True)
    root_window.withdraw()
    if extension is None:
        file_types = [
            ("すべてのファイル", "*"),
        ]
    else:
        if isinstance(extension, str):
            if extension in EXTENSION_DICT.keys():
                file_types = [
                    (EXTENSION_DICT[extension], "*{}".format(extension)),
                    ("すべてのファイル", "*"),
                ]
            else:
                file_types = [
                    (extension[1:].upper(), "*{}".format(extension)),
                    ("すべてのファイル", "*"),
                ]
        else:
            file_types = []
            for element in extension:
                if element in EXTENSION_DICT.keys():
                    file_types.append((EXTENSION_DICT[element], "*{}".format(element)))
                else:
                    file_types.append((extension[1:].upper(), "*{}".format(extension)))
            file_types.append(("すべてのファイル", "*"))
    file_path = filedialog.askopenfilename(
        filetypes=file_types, initialdir=initial_directory
    )
    if file_path == "":
        file_path = None
    return file_path


def select_folder(initial_directory=CURRENT_PATH):
    """処理フォルダーをGUIから選択し, その絶対パスを返す. / Select a processing 
    folder from the GUI and return its absolute path.

    Parameters
    ----------
    initial_directory : str, default: CURRENT_PATH
        最初に開くディレクトリ / first directory to open

    Returns
    -------
    str
        パス / path
    """
    root_window = Tk()
    root_window.attributes("-topmost", True)
    root_window.withdraw()
    folder_path = filedialog.askdirectory(initialdir=initial_directory)
    if folder_path == "":
        folder_path = None
    return folder_path


def get_yes_or_no(word):
    """YesかNoが入力するまで質問を繰り返す. / Repeat the question until you enter 
    Yes or No.

    Parameters
    ----------
    word : str
        質問内容 / Contents of question

    Returns
    -------
    str
        "yes" or "no"
    """
    while True:
        input_word = input(word)
        if input_word.lower() in ("y", "yes",):
            return "yes"
        elif input_word.lower() in ("n", "no",):
            return "no"


def series(function, N, k=None):
    """級数を計算し, 結果を返す. / Calculates a series and returns the result.

    Parameters
    ----------
    function : any type variable of Python
        数列の関数 / function of numerical sequence
    N : int or tuple
        数列の個数 / number of numerical sequence
    k : int or tuple, default: None
        開始番号 / starting number of summing up
    """
    if type(N) == int and (type(k) == int or k == None):
        k = 1 if k == None else k
        return sum(function(i) for i in range(k, N + 1))
    elif type(N) == tuple and (type(k) == tuple or k == None):
        k = tuple(1 for index in range(len(N))) if k == None else k
        return sum(
            function(*i)
            for i in tuple(
                itertools.product(
                    *tuple(
                        tuple(i for i in range(k[index], N[index] + 1))
                        for index in range(len(N))
                    )
                )
            )
        )


def significant_digits(value, digit):
    """引数valueを有効数字が引数digitになるように丸めて返す． / Rounds the 
    argument value so that the significant digits become the argument digit 
    and teturns it.

    Parameters
    ----------
    value : float
        値 / value
    digit : int
        有効数字 / significant digits
    """
    return round(value, digit - int((("{:e}".format(value)).split("e"))[1]) - 1)


def sort_based_on_a_list(sorted_list, standard_list):
    """あるリストを基準にソートする / sort based on a list
    
    Parameters
    ----------
    sorted_list : list
        ソートされるリスト / sorted list
    standard_list : list
        基準となるリスト / standard list
    """
    sorted_list = list(sorted_list)
    standard_list = list(standard_list)
    index_list = []
    for element in sorted(standard_list):
        index = standard_list.index(element)
        index_list.append(index)
        standard_list.pop(index)
        standard_list.insert(index, None)
    new_list = []
    for index in index_list:
        element = sorted_list.pop(index)
        sorted_list.insert(index, None)
        new_list.append(element)
    return new_list


def generate_a_random_string(length_of_string):
    """任意の長さのランダムな文字列を生成する / generate a random string of 
    arbitrary length

    Parameters
    ----------
    length_of_string : int
        取得する文字列の長さ / length of the string to retrieve
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length_of_string)
    )
