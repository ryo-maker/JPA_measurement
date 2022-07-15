"""constantsは様々な定数を格納したモジュールです. / This is a module that stores 
various constants.


Available constants
-------------------
PI
    円周率 / ratio of the circumference of a circle to its diameter

PLANK_CONSTANT
    プランク定数 / Planck’s constant

LOGGING_LEVEL_DICT
    ログレベル / log level number of "logging" module

METRIC_PREFIX
    SI接頭辞 / SI metric prefix
"""


__all__ = [
    "PI",
    "PLANCK_CONSTANT",
    "LOGGING_LEVEL_DICT",
    "METRIC_PREFIX",
    "EXTENSION_DICT",
    "ps",
    "ns",
    "us",
    "ms",
    "kHz",
    "MHz",
    "GHz",
    "THz",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


# 円周率
PI = 3.141592653589793

# プランク定数
PLANCK_CONSTANT = 6.6267015e-34

# ログレベル
LOGGING_LEVEL_DICT = {
    "debug": 10,
    "info": 20,
    "warning": 30,
    "error": 40,
    "critical": 50,
}

# SI接頭辞
METRIC_PREFIX = {
    "Y": 1e24,
    "Z": 1e21,
    "E": 1e18,
    "P": 1e15,
    "T": 1e12,
    "G": 1e9,
    "M": 1e6,
    "k": 1e3,
    "h": 1e2,
    "da": 1e1,
    "": 1e0,
    "d": 1e-1,
    "c": 1e-2,
    "m": 1e-3,
    "u": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
    "a": 1e-18,
    "z": 1e-21,
    "y": 1e-24,
}

# 拡張子とファイルの種類の対応付け
EXTENSION_DICT = {
    "": "ファイル",
    ".db": "Data Base File",
    ".cat": "セキュリティ カタログ",
    ".txt": "テキスト",
    ".bat": "Windows バッチ ファイル",
    ".ps1": "Windows PowerShell スクリプト",
    ".py": "Python Scripts",
    ".aux": "AUXファイル",
    ".icm": "ICC プロファイル",
    ".doc": "Microsoft Word",
    ".wbk": "Microsoft Word",
    ".docx": "Microsoft Word",
    ".xls": "Microsoft Excel",
    ".xlsm": "Microsoft Excel",
    ".xlsx": "Microsoft Excel",
    ".ppt": "Microsoft PowerPoint",
    ".pptx": "Microsoft PowerPoint",
    ".pptm": "Microsoft PowerPoint",
    ".prn": "PRNファイル",
    ".ipynb": "Jupyter Notebooks",
}

# 単位
ps = 1e-12
ns = 1e-9
us = 1e-6
ms = 1e-3
kHz = 1e3
MHz = 1e6
GHz = 1e9
THz = 1e12
