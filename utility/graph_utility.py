"""GraphUtilityはmatplotlibを使用してグラフを作成するためのモジュールです.
(matplotlib ⇒ https://matplotlib.org/)
使用する際, GraphUtilityと同じディレクトリに存在するfontsディレクトリにTrueTypeフォ
ントファイルを置いてください.
"GraphUtility" is a module that creats graphs by using matplotlib.
(matplotlib ⇒ https://matplotlib.org/)
When you use this module, please place the TrueType font file in the "fonts" 
directory that exists in the same directory as "GraphUtility".


Available classes
-------------------
class: GraphUtility
    Class wrapping matplotlib

    variables:
        logger : logging.Logger
           ロガー
        fig : matplotlib.figure.Figure
            matplotlibのfigureインスタンス / The figure instance of matplotlib
        ax : matplotlib.axes._subplots.AxesSubplot
            subplotのaxesインスタンス / The axes of the subplot.
        x_axis_min : float
            X軸の最小値 / X-axis minimum
        x_axis_max : float
            X軸の最大値 / X-axis maximum
        y_axis_min : float
            Y軸の最小値 / Y-axis minimum
        y_axis_max : float
            Y軸の最大値 / Y-axis maximum
        legend_exist : bool
            凡例が存在するかどうか / Whether legends exists

    methods:
        __init__
            パラメータの設定. 変数fig及びaxの準備. / Parameter setting. 
            Preparation of variables fig and ax.
        __del__
            pyplot.figureの全消去及びメモリを解放する. / Erase pyplot.figure and 
            release memory.
        plot
            X軸及びY軸のデータをプロットする. / Plot the X-axis and Y-axis data.
        single_plot
            X軸のデータを自動生成し, Y軸のデータをプロットする. / Automatically 
            generate data on the x-axis and plot data on the y-axis.
        make_color_map
            カラーマップを作成する. / Create a color map.
        line
            補助線を引く. / Draw auxiliary lines.
        save
            図を保存する. / Save the figure.
        show
            図を画面に出力する. / Output the figure to the screen.
"""


import os
import gc
import random
from matplotlib import rc, font_manager, pyplot
from utility import CURRENT_PATH
from utility.logging_utility import get_normal_logger
from utility.others import get_directory_path, get_args_of_current_function, get_time


__all__ = [
    "GraphUtility",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


# パス / paths
DIRECTORY_PATH = get_directory_path(
    __file__
)  # ディレクトリパス / path in where this file is placed
FONT_PATH = (
    DIRECTORY_PATH + "/fonts/ipaexg.ttf"
)  # フォントディレクトリパス / path in where a font file is placed


# デフォルトのパラメータ設定 / default parameter
FONT_SIZE = 25.0  # フォントの大きさ
FIGURE_SIZE = (16.0, 9.0)  # 図のサイズ(横, 縦) / figure size(horizontal, vertical)
AXES_LINE_WIDTH = 3.0  # 軸の線幅
MAJOR_WIDTH = 3.0  # メモリ線の線幅
TICK_LENGTH = 10  # メモリの長さ
TICK_WIDTH = 2  # メモリの幅
COLOR = "k"  # グラフの色 / color of glaph
# (参考 /  ⇒ https://matplotlib.org/api/colors_api.html#module-matplotlib.colors, 
# https://pythondatascience.plavox.info/matplotlib/%E8%89%B2%E3%81%AE%E5%90%8D%E5%89%8D)
LINE = "line"  # グラフの種類 / type of glaph("line", "scatter")
LINE_WIDTH = 2  # 折れ線グラフの線の太さ
POINT_SIZE = 20  # 散布図のポイントの大きさ
DPI = None  # DPI
FONT_NAME = "IPAexGothic"  # フォント名


class GraphUtility:
    """Class wrapping matplotlib

    Parameters
    ----------
    font_size : float or int, default: FONT_SIZE
        フォントの大きさ / font size
    figure_size : tuple or list, default: FIGURE_SIZE
        グラフの大きさ / figure size
    x_axis_min : float or int, default: None
        X軸の最小値 / minimum value of vertical axis
        Noneのとき, 可変になります. / When None, it is variable.
    x_axis_max : float or int, default: None
        X軸の最大値 / max value of vertical axis
        Noneのとき, 可変になります. / When None, it is variable.
    y_axis_min : float or int, default: None
        Y軸の最小値 / minimum value of horizontal axis
        Noneのとき, 可変になります. / When None, it is variable.
    y_axis_max : float or int, default: None
        Y軸の最大値 / max value of horizontal axis
        Noneのとき, 可変になります. / When None, it is variable.
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """

    def __init__(
        self,
        font_size=FONT_SIZE,
        figure_size=FIGURE_SIZE,
        x_axis_min=None,
        x_axis_max=None,
        y_axis_min=None,
        y_axis_max=None,
        logger=get_normal_logger(logger_name="GraphUtility", level="info"),
    ):
        self.logger = logger
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        font_manager.fontManager.addfont(FONT_PATH)
        rc("font", family=FONT_NAME)
        pyplot.rcParams["font.size"] = font_size
        pyplot.rcParams["xtick.major.width"] = MAJOR_WIDTH
        pyplot.rcParams["ytick.major.width"] = MAJOR_WIDTH
        pyplot.rcParams["axes.linewidth"] = AXES_LINE_WIDTH
        self.fig = pyplot.figure(figsize=figure_size)
        self.ax = self.fig.add_subplot(111)
        self.ax.tick_params(
            bottom=True,
            top=True,
            left=True,
            right=True,
            direction="in",
            length=TICK_LENGTH,
            width=TICK_WIDTH,
            colors=COLOR,
        )
        self.x_axis_min = x_axis_min
        self.x_axis_max = x_axis_max
        self.y_axis_min = y_axis_min
        self.y_axis_max = y_axis_max
        self.legend_exist = False

    def __del__(self):
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        pyplot.close()
        del self.fig
        del self.ax
        gc.collect()

    def plot(
        self,
        x_array,
        y_array,
        label=None,
        color=COLOR,
        line=LINE,
        point_size=POINT_SIZE,
        line_width=LINE_WIDTH,
    ):
        """X軸及びY軸のデータをプロットする. / Plot the X-axis and Y-axis data.

        Parameters
        ----------
        x_array : np.ndarray or list
            X軸のデータ / data of X-axis
        y_array : np.ndarray or list
            Y軸のデータ / data of Y-axis
        label : str, default: None
            凡例に表示されるプロットのラベル. / label of the plot displayed in the legend
        color : str, default: COLOR
            グラフの色 / color of graph
            (参考 ⇒ https://matplotlib.org/api/colors_api.html#module-matplotlib.colors, 
            https://pythondatascience.plavox.info/matplotlib/%E8%89%B2%E3%81%AE%E5%90%8D%E5%89%8D)
        line : str, default: LINE
            "line":折れ線グラフ, "scatter":散布図 / "line":polygonal line graph, 
            "scatter":scatter diagram
        point_size : float or int, default: POINT_SIZE
            散布図のポイントの大きさ / size of the points on the scatter plot
        line_width : float or int, default: LINE_WIDTH
            折れ線グラフの線の太さ / line thickness of line graph
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if color == "random":
            random_num = lambda: random.randint(0, 255)
            color = "#%02X%02X%02X" % (random_num(), random_num(), random_num())
        if label == None:
            if line == "scatter":
                self.ax.scatter(x_array, y_array, color=color, s=point_size)
            elif line == "line":
                self.ax.plot(x_array, y_array, color=color, linewidth=line_width)
        else:
            if line == "scatter":
                self.ax.scatter(
                    x_array, y_array, label=label, color=color, s=point_size
                )
            elif line == "line":
                self.ax.plot(
                    x_array, y_array, label=label, color=color, linewidth=line_width
                )

    def single_plot(
        self,
        y_array,
        label=None,
        color=COLOR,
        line=LINE,
        point_size=POINT_SIZE,
        line_width=LINE_WIDTH,
    ):
        """X軸のデータを自動生成し, Y軸のデータをプロットする. / Automatically 
        generate data on the x-axis and plot data on the y-axis.

        Parameters
        ----------
        y_array : np.ndarray or list
            Y軸のデータ / data of Y-axis
        label : str, default: None
            凡例に表示されるプロットのラベル. / label of the plot displayed in the legend
        color : str, default: COLOR
            グラフの色 / color of graph
            (参考 ⇒ https://matplotlib.org/api/colors_api.html#module-matplotlib.colors, 
            https://pythondatascience.plavox.info/matplotlib/%E8%89%B2%E3%81%AE%E5%90%8D%E5%89%8D)
        line : str, default: LINE
            "line":折れ線グラフ, "scatter":散布図 / "line":polygonal line graph, 
            "scatter":scatter diagram
        point_size : float or int, default: POINT_SIZE
            散布図のポイントの大きさ / size of the points on the scatter plot
        line_width : float or int, default: LINE_WIDTH
            折れ線グラフの線の太さ / line thickness of line graph
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        x_array = range(len(y_array))
        self.plot(
            x_array,
            y_array,
            label=label,
            color=color,
            line=line,
            point_size=point_size,
            line_width=line_width,
        )

    def make_color_map(self, z_array, x_axis_min, x_axis_max, y_axis_min, y_axis_max):
        """カラーマップを作成する. / Create a color map.

        Parameters
        ----------
        z_array : np.ndarray or list
            Z軸のデータ / data of Z-axis
        x_axis_min : float
            X軸の最小値 / minimum value of X-axis
        x_axis_max : float
            X軸の最大値 / maximum value of X-axis
        y_axis_min : float
            Y軸の最小値 / minimum value of Y-axis
        y_axis_max : float
            Y軸の最大値 / maximum value of Y-axis
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        image = self.ax.imshow(
            z_array,
            cmap="Reds",
            origin="lower",
            interpolation="gaussian",
            extent=[x_axis_min, x_axis_max, y_axis_min, y_axis_max],
        )
        self.ax.grid(False)
        pyplot.colorbar(image)

    def line(self, value, direction, color="k", line_width=LINE_WIDTH, linestyle="--"):
        """補助線を引く. / Draw auxiliary lines.

        Parameters
        ----------
        value : float or int
            線を引く値 / value of line
        direction : str
            線の方向 / direction of line(縦:("v", "vertical"), 横:("h", "horizontal"))
        color : str, default: "k"
            線の色 / color of line
            (参考 ⇒ https://matplotlib.org/api/colors_api.html#module-matplotlib.colors, 
            https://pythondatascience.plavox.info/matplotlib/%E8%89%B2%E3%81%AE%E5%90%8D%E5%89%8D)
        line_width : float or int, default: LINE_WIDTH
            線の太さ / line thickness
        linestyle : str, default: "--"
            Linestyleの設定
            ----------------------------------------
            Linestyle            -  Description
            "-" or "solid"       -  solid line
            "--" or "dashed"     -  dashed line
            "-." or "dashdot"    -  dash-dotted line
            ":" or "dotted"      -  dotted line
            "None" or " " or ""  -  draw nothin
            ----------------------------------------
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if direction in ("v", "vertical",):
            self.ax.axvline(
                x=value, color=color, linewidth=line_width, linestyle=linestyle
            )
        elif direction in ("h", "horizontal",):
            self.ax.axhline(
                y=value, color=color, linewidth=line_width, linestyle=linestyle
            )

    def save(
        self,
        figure_path=CURRENT_PATH,
        figure_name=get_time(),
        extension=".png",
        x_axis_label=None,
        y_axis_label=None,
        legend=False,
    ):
        """図を保存する. / Save the figure.

        Parameters
        ----------
        figure_path : str, default: None
            図の保存先 / where to save the figure
        figure_name : str, default: utility.others.get_time()
            保存する図の名前 / name of the figure to save
        extension : str, default: ".png"
            図の拡張子 / extension of figure
        x_axis_label : str, default: None
            X軸の名前 / name of X-axis
        y_axis_label : str, default: None
            Y軸の名前 / name of Y-axis
        legend : bool, default: True
            Trueのとき, 凡例を出力する. / If true, print a legend.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.ax.set_xlim(left=self.x_axis_min, right=self.x_axis_max)
        self.ax.set_ylim(bottom=self.y_axis_min, top=self.y_axis_max)
        if x_axis_label != None:
            self.ax.set_xlabel(x_axis_label)
        if y_axis_label != None:
            self.ax.set_ylabel(y_axis_label)
        if legend:
            if self.legend_exist == False:
                self.fig.legend()
                self.legend_exist = True
        self.fig.tight_layout()
        os.makedirs(figure_path, exist_ok=True)
        self.fig.savefig(figure_path + "/" + figure_name + extension, dpi=DPI)

    def show(self, x_axis_label=None, y_axis_label=None, legend=False):
        """図を画面に出力する. / Output the figure to the screen.

        Parameters
        ----------
        x_axis_label : str, default: None
            X軸の名前 / name of X-axis
        y_axis_label : str, default: None
            Y軸の名前 / name of Y-axis
        legend : bool, default: True
            Trueのとき, 凡例を出力する. / If true, print a legend.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if x_axis_label != None:
            self.ax.set_xlabel(x_axis_label)
        if y_axis_label != None:
            self.ax.set_ylabel(y_axis_label)
        if legend:
            if self.legend_exist == False:
                self.fig.legend()
                self.legend_exist = True
        self.fig.tight_layout()
        pyplot.show()
