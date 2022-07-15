"""utilityは汎用のモジュールが格納されたパッケージです. / This is a package that st
ores general-purpose modules.


Available modules
-----------------
constants
    様々な定数を格納したモジュール / a module that contains various constants

file_manager
    ディレクトリの情報を取得, 操作するモジュール / a module for retrieving and 
    manipulating directory information

graph_utility
    matplotlibを使用してグラフを作成するためのモジュール / a module for creating 
    graphs using matplotlib

logging_utility
    loggerを作成するモジュール / a module to create loggers

others
    その他の関数が格納されたモジュール / a module containing other functions

pulse
    パルスシーケンスを作成するためのモジュール / a module for creating a pulse 
    sequence

read_write
    テキストファイル, CSVファイル, バイナリファイルを読み書きするためのモジュール / a 
    module to read and write text files, CSV files and binary files

waveform_processing
    numpyを使用してデータの処理を行うためのモジュール / a module for processing 
    data using numpy
"""


import os
import sys


__all__ = [
    "COMMAND_LINE_ARGUMENTS",
    "MAIN_FILE_DIRECTORY_PATH",
    "CURRENT_PATH",
    "PROGRAM_NAME",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


COMMAND_LINE_ARGUMENTS = sys.argv
CURRENT_PATH = os.getcwd()
MAIN_FILE_DIRECTORY_PATH = os.path.dirname(
    os.path.abspath(COMMAND_LINE_ARGUMENTS[0])
)
PROGRAM_NAME, _ = os.path.splitext(
    os.path.basename(os.path.abspath(COMMAND_LINE_ARGUMENTS[0]))
)
