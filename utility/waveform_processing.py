"""WaveformProcessingはnumpyを使用してデータの処理を行うためのモジュールです.
(numpy ⇒ https://np.org/) / "WaveformProcessing" is a module for processing 
data by using np.


Available classes
-------------------
class: WaveformProcessing
    Class for processing data

    variables:
        minimum_value : float
            電力の最小値 / minimum power
        sampling_rate : float
            サンプリングレート / sampling rate
        waveform_array : np.ndarray
            波形データの配列 / data array of waveform
        characteristic_impedance : float
            特性インピーダンス / characteristic_impedance
        dtype : np.dtype
            データ型 / data type
        logger : logging.Logger
            ロガー / logger
        length : int
            波形データの配列の個数 / length of data array of waveform
        length_roll : int
            データをずらす個数 / number of data to shift
        time_length : float
            データの時間的な長さ / time length of data
        time_array : np.ndarray
            時間配列 / time array
        frequency_array : np.ndarray
            周波数配列 / frequency array
        positive_frequency_array : np.ndarray
            正の周波数配列 / positive frequency array

    methods:
        __init__
            パラメータの設定. 配列データの読み込み. フーリエ変換. / Parameter 
            setting. Array data reading. Fourier transform.
        __del__
            メモリを解放する. / Release memory.
        get_dc_voltage:
            DC成分の大きさを返す. / Return DC voltage.
        get_voltage
            電圧の大きさを返す. / Return voltage.
        get_spectrum
            スペクトルの値を返す. / Return value of spectrum.
        get_power
            電力の大きさを返す. / Return power.
        fourier_transform
            waveformをフーリエ変換する. / Fourier transform the waveform.
        inverse_fourier_transform
            spectrumを逆フーリエ変換する. / Inverse Fourier transform of the spectrum.
        hanning
            waveformにハニング窓をかける. / Arrange waveform by using hanning window
        hamming
            waveformにハミング窓をかける. / Arrange waveform by using hamming window
        zerofill
            波形データに対してゼロフィル処理を行う. / Zero-fill processing of waveform data.
        rectifire
            波形データから正もしくは負のデータを0にする. / Set positive or negative 
            data from the waveform data to zero.
        through
            low_frequencyからhigh_frequencyの間以外の周波数成分を0にする. / Set the 
            frequency component to 0 except between low_frequency and high_frequency.
        block
            low_frequencyからhigh_frequencyの間の周波数成分を0にする.
        lpf
            LPFをかける. / Arrange waveform by using low pass filter.
        hpf
            HPFをかける. / Arrange waveform by using high pass filter.
        bpf
            BPFをかける. / Arrange waveform by using band pass filter.
        bsf
            BSFをかける. / Arrange waveform by using band stop filter.
        fir_lpf
            LPFをかける. / Arrange waveform by using low pass filter.
        fir_hpf
            HPFをかける. / Arrange waveform by using high pass filter.
        fir_bpf
            BPFをかける. / Arrange waveform by using band pass filter.
        fir_bsf
            BSFをかける. / Arrange waveform by using band stop filter.
        dc_block
            DC成分を0にする. / Make dc offset zero.
        zoom
            一部をズームする. / Zoom in on part of waveform.
        save
            PNGファイル及びCSVファイルを作成, 保存する. / Create and save PNG and 
            CSV files.
        show
            グラフを画面に出力する． / Output the graph to the screen.
"""


import gc
import numpy as np
from scipy.signal import firwin, lfilter
from utility import CURRENT_PATH
from utility.constants import METRIC_PREFIX
from utility.graph_utility import GraphUtility
from utility.logging_utility import get_normal_logger
from utility.others import get_args_of_current_function, get_time
from utility.read_write import write_csv


__all__ = [
    "WaveformProcessing",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


# デフォルトのパラメータ設定 / default parameter
MINIMUM_VALUE = 1e-20


class WaveformProcessing:
    """Class for processing data.

    Parameters
    ----------
    sampling_rate : float
        サンプリングレート / sampling rate
    waveform_array : np.ndarray or list
        波形データ / data array of waveform
    characteristic_impedance : float or int, default: 50.
        特性インピーダンス / characteristic impedance
    dtype : np.dtype, default: complex
        numpy arrayのデータ型 / data type of array
    logger : logging.Logger, default: utility.logging_utility.get_normal_logger()
        任意のロガー / any logger
    """

    def __init__(
        self,
        sampling_rate,
        waveform_array,
        fourier_transform=True,
        characteristic_impedance=50.0,
        dtype=complex,
        logger=get_normal_logger(logger_name="WaveformProcessing", level="info"),
    ):
        self.minimum_value = MINIMUM_VALUE
        self.sampling_rate = float(sampling_rate)
        self.waveform_array = np.array(waveform_array, dtype=dtype)
        self.characteristic_impedance = float(characteristic_impedance)
        self.dtype = dtype
        self.logger = logger
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.length = len(self.waveform_array)
        self.length_roll = (
            self.length - 1
        ) // 2  # FFTをかけるときに配列をシフトする量 / Amount to shift the array when performing FFT operations
        self.time_length = float(self.length) / self.sampling_rate
        self.time_array = np.linspace(
            -self.time_length / 2.0, self.time_length / 2.0, self.length, endpoint=False
        )
        self.frequency_array = (
            np.linspace(
                -float(self.length_roll),
                float(self.length_roll) + (self.length + 1) % 2,
                self.length,
            )
            * self.sampling_rate
            / float(self.length)
        )
        self.positive_frequency_array = (
            np.linspace(0.0, float(self.length_roll), self.length_roll + 1)
            * self.sampling_rate
            / float(self.length)
        )
        if fourier_transform:
            self.fourier_transform()

    def __del__(self):
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        del self.time_array
        del self.frequency_array
        del self.positive_frequency_array
        del self.spectrum_array
        del self.power_array_W
        del self.power_array_dBm
        gc.collect()

    def _set_power(self):
        """インスタンス変数spectrumを元にインスタンス変数powerに値を代入する. / 
        Assign a value to the instance variable power based on the instance 
        variable spectrum.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.power_array_W = (
            np.abs(self.spectrum_array ** 2.0, dtype=float)
            / self.characteristic_impedance
        )
        self.power_array_W = np.hstack(
            (
                self.power_array_W[self.length_roll],
                np.flip(self.power_array_W[: self.length_roll])
                + self.power_array_W[
                    self.length_roll + 1 : self.length - (self.length + 1) % 2
                ],
            )
        )
        self.power_array_dBm = 10.0 * np.log10(
            np.clip(self.power_array_W * 1e3, self.minimum_value, None)
        )

    def _get_time_array_index(self, time, over):
        """指定した時間のインデックスを返す. / Returns the index for the specified time.

        Parameters
        ----------
        time : float
            インデックスを返す時間 / time to return the index
        over : bool
            指定した時間より大きいインデックスを返すかどうか / Whether to return an 
            index greater than the specified time

        Returns
        -------
        int
            指定した時間のインデックス / index at a specified time
        """
        if over:
            return np.where(self.time_array >= time)[0][0]
        else:
            return np.where(self.time_array <= time)[0][-1]

    def _get_frequency_array_index(self, frequency, over):
        """指定した周波数のインデックスを返す. / Returns the index for the specified frequency.

        Parameters
        ----------
        frequency : float
            インデックスを返す周波数 / frequency to return the index
        over : bool
            指定した時間より大きいインデックスを返すかどうか / Whether to return an 
            index greater than the specified time

        Returns
        -------
        int
            指定した周波数のインデックス / index at a specified frequency
        """
        if over:
            return np.where(self.frequency_array >= frequency)[0][0]
        else:
            return np.where(self.frequency_array <= frequency)[0][-1]

    def _get_positive_frequency_array_index(self, frequency, over):
        """指定した周波数のインデックスを返す. / Returns the index for the specified frequency.

        Parameters
        ----------
        frequency : float
            インデックスを返す周波数 / frequency to return the index
        over : bool
            指定した時間より大きいインデックスを返すかどうか / Whether to return an 
            index greater than the specified time

        Returns
        -------
        int
            指定した周波数のインデックス / index at a specified frequency
        """
        if over:
            return np.where(self.positive_frequency_array >= frequency)[0][0]
        else:
            return np.where(self.positive_frequency_array <= frequency)[0][-1]

    def _set_any_frequency_spectrum_zero(self, frequency, over):
        """任意の周波数のスペクトルをゼロにする. / Zero the spectrum of any frequency.

        Parameters
        ----------
        frequency : float
            任意の周波数 / any frequency
        over : bool
            Trueのとき, 指定の周波数よりも大きい周波数をゼロにする. / If True, zero 
            frequencies above the specified frequency.
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        """
        cut_point = self._get_frequency_array_index(frequency, over)
        if over:
            self.spectrum_array = np.hstack(
                (
                    self.spectrum_array[:cut_point],
                    np.zeros(self.length - cut_point, dtype=self.dtype),
                )
            )
        else:
            self.spectrum_array = np.hstack(
                (
                    np.zeros(self.length - cut_point, dtype=self.dtype),
                    self.spectrum_array[:cut_point],
                )
            )

    def get_dc_voltage(self):
        """DC成分の大きさを返す. / Return DC voltage.

        Returns
        -------
        complex
            DC成分の値 / value of DC voltage"""
        return self.spectrum_array[self.length_roll]

    def get_voltage(self, time):
        """電圧の大きさを返す. / Return voltage.

        Parameters
        ----------
        time : float
            電圧を返す時間 / time to return voltage

        Returns
        -------
        complex
            電圧の値 / value of voltage
        """
        point = self._get_time_array_index(time=time, over=False)
        return (
            self.sampling_rate
            * (self.waveform_array[point + 1] - self.waveform_array[point])
            * (time - self.time_array[point])
            + self.waveform_array[point]
        )

    def get_spectrum(self, frequency):
        """スペクトルの値を返す. / Return value of spectrum.

        Parameters
        ----------
        frequency : float
            スペクトルの値を返す周波数 / frequency to return value of spectrum

        Returns
        -------
        complex
            スペクトルの値 / value of spectrum
        """
        point = self._get_frequency_array_index(frequency=frequency, over=False)
        return (self.spectrum_array[point + 1] - self.spectrum_array[point]) * (
            frequency - self.frequency_array[point]
        ) / self.sampling_rate + self.spectrum_array[point]

    def get_power(self, frequency, unit=True):
        """電力の大きさを返す. / Return power.

        Parameters
        ----------
        frequency : float
            電圧を返す周波数 / time to return frequency
        unit : bool
            Trueのとき, 単位をdBmとして返す. Falseのとき, 単位をWとして返す. / When 
            True, the unit is returned as dBm. When False, the unit is returned as W.

        Returns
        -------
        float
            電力の値 / value of power
        """
        point = self._get_positive_frequency_array_index(
            frequency=frequency, over=False
        )
        power = (self.power_array_W[point + 1] - self.power_array_W[point]) * (
            frequency - self.positive_frequency_array[point]
        ) / self.sampling_rate + self.power_array_W[point]
        if unit:
            return 10.0 * np.log10(power * 1e3)
        else:
            return power

    def fourier_transform(self):
        """waveformをフーリエ変換する. / Fourier transform the waveform."""
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.spectrum_array = np.roll(
            np.fft.fft(self.waveform_array).astype(self.dtype), self.length_roll
        ) / float(self.length)
        self._set_power()

    def inverse_fourier_transform(self):
        """spectrumを逆フーリエ変換する. / Inverse Fourier transform of the spectrum."""
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.waveform_array = float(self.length) * np.fft.ifft(
            np.roll(self.spectrum_array, -self.length_roll)
        ).astype(self.dtype)

    def zerofill(self, length):
        """波形データに対してゼロフィル処理を行う. / Zero-fill processing of waveform data.

        Parameters
        ----------
        length : int
            ゼロフィルするデータのポイント数 / number of points used to zero-fill
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.waveform_array = np.hstack(
            (self.waveform_array, np.zeros(length, dtype=self.dtype))
        )
        self.length = len(self.waveform_array)
        self.length_roll = (self.length - 1) // 2
        self.time_length = float(self.length) / self.sampling_rate
        self.time_array = np.linspace(
            -self.time_length / 2.0, self.time_length / 2.0, self.length, endpoint=False
        )
        self.frequency_array = (
            np.linspace(
                -float(self.length_roll),
                float(self.length_roll) + (self.length + 1) % 2,
                self.length,
            )
            * self.sampling_rate
            / float(self.length)
        )
        self.positive_frequency_array = (
            np.linspace(0.0, float(self.length_roll), self.length_roll + 1)
            * self.sampling_rate
            / float(self.length)
        )
        self.fourier_transform()

    def hanning(self):
        """waveformにハニング窓をかける. / Arrange waveform by using hanning window"""
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.waveform_array = self.waveform_array * (
            0.5
            - 0.5
            * np.cos(
                2.0
                * np.pi
                * np.arange(self.length, dtype=self.dtype)
                / float(self.length)
            )
        )

    def hamming(self):
        """waveformにハミング窓をかける. / Arrange waveform by using hamming window"""
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.waveform_array = self.waveform_array * (
            0.54
            - 0.46
            * np.cos(
                2.0
                * np.pi
                * np.arange(self.length, dtype=self.dtype)
                / float(self.length)
            )
        )

    def rectifire(self, polarization=True, fourier_transform=True):
        """波形データから正もしくは負のデータを0にする. / Set positive or negative 
        data from the waveform data to zero.

        Parameters
        ----------
        polarization : bool, default: True
            Trueのとき, 負の部分をカット, Falseのとき, 正の部分をカット / If True, 
            set negative data to zero. If False, set positive data to zero.
        fourier_transform : bool, default: True
            Trueのとき, 最後にフーリエ変換する / If True, fourier transform at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if polarization:
            self.waveform_array = np.clip(self.waveform_array, 0.0, None)
        else:
            self.waveform_array = np.clip(self.waveform_array, None, 0.0)
        if fourier_transform:
            self.fourier_transform()

    def dc_block(self, inverse_fourier_transform=True, fourier_transform=False):
        """DC成分を0にする. / Make dc offset zero.

        Parameters
        ----------
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        fourier_transform : bool, default: False
            Trueのとき, 最後にフーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.spectrum_array[self.length_roll] = 0.0 + 0.0j
        self._set_power()
        if inverse_fourier_transform:
            self.inverse_fourier_transform()
        if fourier_transform:
            self.fourier_transform()

    def through(
        self,
        low_frequency,
        high_frequency,
        inverse_fourier_transform=True,
        fourier_transform=False,
    ):
        """low_frequencyからhigh_frequencyの間以外の周波数成分を0にする. / Set the 
        frequency component to 0 except between low_frequency and high_frequency.

        Parameters
        ----------
        low_frequency : float
            通す周波数の最低値(単位:Hz) / lowest value of frequency to pass(unit:Hz)
        high_frequency : float
            通す周波数の最高値(単位:Hz) / highest value of frequency to pass(unit:Hz)
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        fourier_transform : bool, default: False
            Trueのとき, 最後にフーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        low_cut_point = self._get_frequency_array_index(low_frequency, True)
        high_cut_point = self._get_frequency_array_index(high_frequency, False)
        self.spectrum_array = np.hstack(
            (
                np.zeros(low_cut_point, dtype=self.dtype),
                self.spectrum_array[low_cut_point : high_cut_point + 1],
                np.zeros(self.length - high_cut_point - 1, dtype=self.dtype),
            )
        )
        self._set_power()
        if inverse_fourier_transform:
            self.inverse_fourier_transform()
        if fourier_transform:
            self.fourier_transform()

    def block(
        self,
        low_frequency,
        high_frequency,
        inverse_fourier_transform=True,
        fourier_transform=False,
    ):
        """low_frequencyからhigh_frequencyの間の周波数成分を0にする.

        Parameters
        ----------
        low_frequency : float
            通さない周波数の最低値(単位:Hz) / lowest value of frequency to stop(unit:Hz)
        high_frequency : float
            通さない周波数の最高値(単位:Hz) / high value of frequency to stop(unit:Hz)
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        fourier_transform : bool, default: False
            Trueのとき, 最後にフーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        low_cut_point = self._get_frequency_array_index(low_frequency, True)
        high_cut_point = self._get_frequency_array_index(high_frequency, False)
        self.spectrum_array = np.hstack(
            (
                self.spectrum_array[:low_cut_point],
                np.zeros(high_cut_point - low_cut_point + 1, dtype=self.dtype),
                self.spectrum_array[high_cut_point + 1 :],
            )
        )
        self._set_power()
        if inverse_fourier_transform:
            self.inverse_fourier_transform()
        if fourier_transform:
            self.fourier_transform()

    def lpf(self, frequency, inverse_fourier_transform=True):
        """LPFをかける. / Arrange waveform by using low pass filter.

        Parameters
        ----------
        frequency : float
            LPFの周波数(単位:Hz) / frequency of LPF
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.through(-frequency, frequency, inverse_fourier_transform)

    def hpf(self, frequency, inverse_fourier_transform=True):
        """HPFをかける. / Arrange waveform by using high pass filter.

        Parameters
        ----------
        frequency : float
            周波数(単位:Hz) / frequency of HPF
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.block(
            -frequency + 0.25 * self.sampling_rate / float(self.length),
            frequency - 0.25 * self.sampling_rate / float(self.length),
            inverse_fourier_transform,
        )

    def bpf(
        self,
        low_frequency,
        high_frequency,
        inverse_fourier_transform=True,
        fourier_transform=False,
    ):
        """BPFをかける. / Arrange waveform by using band pass filter.

        Parameters
        ----------
        low_frequency : float
            通す周波数の最低値(単位:Hz) / lowest value of frequency to pass(unit:Hz)
        high_frequency : float
            通す周波数の最高値(単位:Hz) / highest value of frequency to pass(unit:Hz)
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        fourier_transform : bool, default: False
            Trueのとき, 最後にフーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.lpf(high_frequency, inverse_fourier_transform=False)
        self.hpf(low_frequency, inverse_fourier_transform=False)
        if inverse_fourier_transform:
            self.inverse_fourier_transform()
        if fourier_transform:
            self.fourier_transform()

    def bsf(
        self,
        low_frequency,
        high_frequency,
        inverse_fourier_transform=True,
        fourier_transform=False,
    ):
        """BSFをかける. / Arrange waveform by using band stop filter.

        low_frequency : float
            通さない周波数の最低値(単位:Hz) / lowest value of frequency to stop(unit:Hz)
        high_frequency : float
            通さない周波数の最高値(単位:Hz) / high value of frequency to stop(unit:Hz)
        inverse_fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        fourier_transform : bool, default: False
            Trueのとき, 最後にフーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        self.lpf(low_frequency, inverse_fourier_transform=False)
        self.hpf(high_frequency, inverse_fourier_transform=False)
        if inverse_fourier_transform:
            self.inverse_fourier_transform()
        if fourier_transform:
            self.fourier_transform()

    def fir_lpf(self, frequency, length_of_filter, fourier_transform=True):
        """LPFをかける. / Arrange waveform by using low pass filter.

        Parameters
        ----------
        frequency : float
            LPFの周波数(単位:Hz) / frequency of LPF
        length_of_filter : int
            FIRフィルタの長さ / length of FIR filter
        fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        fir_filter = firwin(
            numtaps=length_of_filter,
            cutoff=frequency,
            width=None,
            window="hamming",
            pass_zero=True,
            scale=True,
            nyq=None,
            fs=self.sampling_rate,
        )
        self.waveform_array = lfilter(fir_filter, 1, self.waveform_array)
        if fourier_transform:
            self.fourier_transform()

    def fir_hpf(self, frequency, length_of_filter, fourier_transform=True):
        """HPFをかける. / Arrange waveform by using high pass filter.

        Parameters
        ----------
        frequency : float
            HPFの周波数(単位:Hz) / frequency of HPF
        length_of_filter : int
            FIRフィルタの長さ / length of FIR filter
        fourier_transform : bool, default: True
            Trueのとき, 最後に逆フーリエ変換する. / If True, Inverse Fourier 
            Transform at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        fir_filter = firwin(
            numtaps=length_of_filter,
            cutoff=frequency,
            width=None,
            window="hamming",
            pass_zero=False,
            scale=True,
            nyq=None,
            fs=self.sampling_rate,
        )
        self.waveform_array = lfilter(fir_filter, 1, self.waveform_array)
        if fourier_transform:
            self.fourier_transform()

    def fir_bpf(
        self, low_frequency, high_frequency, length_of_filter, fourier_transform=True
    ):
        """BPFをかける. / Arrange waveform by using band pass filter.

        Parameters
        ----------
        low_frequency : float
            通す周波数の最低値(単位:Hz) / lowest value of frequency to pass(unit:Hz)
        high_frequency : float
            通す周波数の最高値(単位:Hz) / highest value of frequency to pass(unit:Hz)
        length_of_filter : int
            FIRフィルタの長さ / length of FIR filter
        fourier_transform : bool, default: True
            Trueのとき, 最後にフーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        fir_filter = firwin(
            numtaps=length_of_filter,
            cutoff=[low_frequency, high_frequency],
            width=None,
            window="hamming",
            pass_zero=False,
            scale=True,
            nyq=None,
            fs=self.sampling_rate,
        )
        self.waveform_array = lfilter(fir_filter, 1, self.waveform_array)
        if fourier_transform:
            self.fourier_transform()

    def fir_bsf(
        self, low_frequency, high_frequency, length_of_filter, fourier_transform=True
    ):
        """BSFをかける. / Arrange waveform by using band stop filter.

        Parameters
        ----------
        low_frequency : float
            通さない周波数の最低値(単位:Hz) / lowest value of frequency to stop(unit:Hz)
        high_frequency : float
            通さない周波数の最高値(単位:Hz) / high value of frequency to stop(unit:Hz)
        length_of_filter : int
            FIRフィルタの長さ / length of FIR filter
        fourier_transform : bool, default: True
            Trueのとき, 最後にフーリエ変換する. / If true, the Fourier transform 
            is performed at the end.
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        fir_filter = firwin(
            numtaps=length_of_filter,
            cutoff=[low_frequency, high_frequency],
            width=None,
            window="hamming",
            pass_zero=True,
            scale=True,
            nyq=None,
            fs=self.sampling_rate,
        )
        self.waveform_array = lfilter(fir_filter, 1, self.waveform_array)
        if fourier_transform:
            self.fourier_transform()

    def zoom(
        self, low_time=None, high_time=None, low_frequency=None, high_frequency=None
    ):
        """一部をズームする. / Zoom in on part of waveform.

        Parameters
        ----------
        low_time : float, default: None
            ズームされる時刻の最低値(単位:s) / lowest value of time to be zoomed(unit:s)
        high_time : float, default: None
            ズームされる時刻の最高値(単位:s) / highest value of time to be zoomed(unit:s)
        low_frequency : float, default: None
            ズームされる周波数の最低値(単位:Hz) / lowest value of frequency to be 
            zoomed(unit:Hz)
        high_frequency : float, default: None
            ズームされる周波数の最高値(単位:Hz) / high value of frequency to be 
            zoomed(unit:Hz)
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if low_time != None and high_time != None:
            low_cut_point = self._get_time_array_index(low_time, True)
            high_cut_point = self._get_time_array_index(high_time, False)
            self.t_zoom = self.time_array[low_cut_point : high_cut_point + 1]
            self.waveform_array_zoom = self.waveform_array[
                low_cut_point : high_cut_point + 1
            ]
        if low_frequency != None and high_frequency != None:
            low_cut_point = self._get_frequency_array_index(low_frequency, True)
            high_cut_point = self._get_frequency_array_index(high_frequency, False)
            self.f_zoom = self.frequency_array[low_cut_point : high_cut_point + 1]
            self.spectrum_array_zoom = self.spectrum_array[
                low_cut_point : high_cut_point + 1
            ]
            if low_frequency < 0.0 and high_frequency < 0.0:
                low_frequency, high_frequency = abs(high_frequency), abs(low_frequency)
            elif low_frequency < 0.0 and high_frequency > 0.0:
                low_frequency = 0.0
            low_cut_point = self._get_positive_frequency_array_index(
                low_frequency, True
            )
            high_cut_point = self._get_positive_frequency_array_index(
                high_frequency, False
            )
            self.r_zoom = self.positive_frequency_array[
                low_cut_point : high_cut_point + 1
            ]
            self.power_array_dBm_zoom = self.power_array_dBm[
                low_cut_point : high_cut_point + 1
            ]

    def save(
        self,
        csv_path=CURRENT_PATH,
        figure_path=CURRENT_PATH,
        file_name=get_time(),
        time_metric_prefix="",
        voltage_metric_prefix="",
        frequency_metric_prefix="",
        power_metric_prefix="",
        time_min=None,
        time_max=None,
        voltage_min=None,
        voltage_max=None,
        frequency_min=None,
        frequency_max=None,
        power_min=None,
        power_max=None,
        time_zoom_min=None,
        time_zoom_max=None,
        voltage_zoom_min=None,
        voltage_zoom_max=None,
        frequency_zoom_min=None,
        frequency_zoom_max=None,
        power_zoom_min=None,
        power_zoom_max=None,
        waveform_display="r",
        spectrum_display="ri",
    ):
        """PNGファイル及びCSVファイルを作成, 保存する. / Create and save PNG and CSV files.

        Parameters
        ----------
        csv_path : str, default: os.getcwd() + "/DATA/CSV"
            CSVファイルの保存先 / CSV file save destination
        figure_path : str, default: os.getcwd() + "/DATA/PNG"
            PNGファイルの保存先 / PNG file save destination
        file_name : str, default: get_time()
            PNGファイル及びCSVファイル名 / PNG file and CSV file name
        time_metric_prefix : str, default: ""
            時間のSI接頭辞 / SI prefix of time
        voltage_metric_prefix : str, default: ""
            電圧のSI接頭辞 / SI prefix of voltage
        frequency_metric_prefix : str, default: ""
            周波数のSI接頭辞 / SI prefix of frequency
        power_metric_prefix : str, default: ""
            dB表示のSI接頭辞 / SI prefix of power
        time_min : float, default: None
            時刻の最小値 / minimum value of time
        time_max : float, default: None
            時刻の最大値 / maximum value of time
        voltage_min : float, default: None
            電圧の最小値 / minimum value of voltage
        voltage_max : float, default: None
            電圧の最大値 / maximum value of voltage
        frequency_min : float, default: None
            周波数の最小値 / minimum value of frequency
        frequency_max : float, default: None
            周波数の最大値 / maximum value of frequency
        power_min : float, default: None
            dB表示の最小値 / minimum value of power
        power_max : float, default: None
            dB表示の最大値 / maximum value of power
        time_zoom_min : float, default: None
            ズームした状態の時刻の最小値 / minimum value of time when zoomed
        time_zoom_max : float, default: None
            ズームした状態の時刻の最大値 / maximum value of time when zoomed
        voltage_zoom_min : float, default: None
            ズームした状態の電圧の最小値 / minimum value of voltage when zoomed
        voltage_zoom_max : float, default: None
            ズームした状態の電圧の最大値 / maximum value of voltage when zoomed
        frequency_zoom_min : float, default: None
            ズームした状態の周波数の最小値 / minimum value of frequency when zoomed
        frequency_zoom_max : float, default: None
            ズームした状態の周波数の最大値 / maximum value of frequency when zoomed
        power_zoom_min : float, default: None
            ズームした状態のdB表示の最小値 / minimum value of power when zoomed
        power_zoom_max : float, default: None
            ズームした状態のdB表示の最大値 / maximum value of power when zoomed
        waveform_display : str, default: "r"
            waveformのグラフの'r':実数成分を表示, 'i':虚数成分を表示 / "r":show 
            real part of waveform, "i":show imag part of waveform
        spectrum_display : str, default: "ri"
            spectrumのグラフの'r':実数成分を表示, 'i':虚数成分を表示 / "r":show 
            
            real part of waveform, "i":show imag part of waveform
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if time_metric_prefix != None:
            time_unit = " ({}s)".format(time_metric_prefix)
        else:
            time_unit = ""
            time_metric_prefix = ""
        if voltage_metric_prefix != None:
            voltage_unit = " ({}V)".format(voltage_metric_prefix)
        else:
            voltage_unit = ""
            voltage_metric_prefix = ""
        if frequency_metric_prefix != None:
            frequency_unit = " ({}Hz)".format(frequency_metric_prefix)
        else:
            frequency_unit = ""
            frequency_metric_prefix = ""
        if power_metric_prefix != None:
            power_unit = " ({}dBm)".format(power_metric_prefix)
        else:
            power_unit = ""
            power_metric_prefix = ""
        write_csv(
            (
                self.time_array / METRIC_PREFIX[time_metric_prefix],
                self.waveform_array.real / METRIC_PREFIX[voltage_metric_prefix],
                self.waveform_array.imag / METRIC_PREFIX[voltage_metric_prefix],
            ),
            header=[
                "Time{}".format(time_unit),
                "Voltage{} (real)".format(voltage_unit),
                "Voltage{} (image)".format(voltage_unit),
            ],
            csv_path=csv_path,
            csv_name="waveform_" + file_name,
        )
        write_csv(
            (
                self.frequency_array / METRIC_PREFIX[frequency_metric_prefix],
                self.spectrum_array.real / METRIC_PREFIX[voltage_metric_prefix],
                self.spectrum_array.imag / METRIC_PREFIX[voltage_metric_prefix],
            ),
            header=[
                "Frequency{}".format(frequency_unit),
                "Voltage{} (real)".format(voltage_unit),
                "Voltage{} (image)".format(voltage_unit),
            ],
            csv_path=csv_path,
            csv_name="spectrum_" + file_name,
        )
        write_csv(
            (
                self.positive_frequency_array / METRIC_PREFIX[frequency_metric_prefix],
                self.power_array_dBm / METRIC_PREFIX[power_metric_prefix],
            ),
            header=["Frequency{}".format(frequency_unit), "Power{}".format(power_unit)],
            csv_path=csv_path,
            csv_name="power_" + file_name,
        )
        waveform_graph = GraphUtility(
            x_axis_min=time_min,
            x_axis_max=time_max,
            y_axis_min=voltage_min,
            y_axis_max=voltage_max,
            logger=self.logger,
        )
        if "r" in waveform_display:
            waveform_graph.plot(
                self.time_array / METRIC_PREFIX[time_metric_prefix],
                self.waveform_array.real / METRIC_PREFIX[voltage_metric_prefix],
                color="r",
            )
        if "i" in waveform_display:
            waveform_graph.plot(
                self.time_array / METRIC_PREFIX[time_metric_prefix],
                self.waveform_array.imag / METRIC_PREFIX[voltage_metric_prefix],
                color="b",
            )
        waveform_graph.save(
            figure_path=figure_path,
            figure_name="waveform_" + file_name,
            x_axis_label="Time{}".format(time_unit),
            y_axis_label="Voltage{}".format(voltage_unit),
        )
        del waveform_graph
        waveform_graph = GraphUtility(
            x_axis_min=frequency_min,
            x_axis_max=frequency_max,
            y_axis_min=voltage_min,
            y_axis_max=voltage_max,
            logger=self.logger,
        )
        if "r" in spectrum_display:
            waveform_graph.plot(
                self.frequency_array / METRIC_PREFIX[frequency_metric_prefix],
                self.spectrum_array.real / METRIC_PREFIX[voltage_metric_prefix],
                color="r",
            )
        if "i" in spectrum_display:
            waveform_graph.plot(
                self.frequency_array / METRIC_PREFIX[frequency_metric_prefix],
                self.spectrum_array.imag / METRIC_PREFIX[voltage_metric_prefix],
                color="b",
            )
        waveform_graph.save(
            figure_path=figure_path,
            figure_name="spectrum_" + file_name,
            x_axis_label="Frequency{}".format(frequency_unit),
            y_axis_label="Voltage{}".format(voltage_unit),
        )
        del waveform_graph
        waveform_graph = GraphUtility(
            x_axis_min=frequency_min,
            x_axis_max=frequency_max,
            y_axis_min=power_min,
            y_axis_max=power_max,
            logger=self.logger,
        )
        waveform_graph.plot(
            self.positive_frequency_array / METRIC_PREFIX[frequency_metric_prefix],
            self.power_array_dBm / METRIC_PREFIX[power_metric_prefix],
        )
        waveform_graph.save(
            figure_path=figure_path,
            figure_name="power_" + file_name,
            x_axis_label="Frequency{}".format(frequency_unit),
            y_axis_label="Power{}".format(power_unit),
        )
        del waveform_graph
        try:
            waveform_graph = GraphUtility(
                x_axis_min=time_zoom_min,
                x_axis_max=time_zoom_max,
                y_axis_min=voltage_zoom_min,
                y_axis_max=voltage_zoom_max,
                logger=self.logger,
            )
            if "r" in waveform_display:
                waveform_graph.plot(
                    self.t_zoom / METRIC_PREFIX[time_metric_prefix],
                    self.waveform_array_zoom.real
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="r",
                )
            if "i" in waveform_display:
                waveform_graph.plot(
                    self.t_zoom / METRIC_PREFIX[time_metric_prefix],
                    self.waveform_array_zoom.imag
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="b",
                )
            waveform_graph.save(
                figure_path=figure_path,
                figure_name="time_zoom_" + file_name,
                x_axis_label="Time{}".format(time_unit),
                y_axis_label="Voltage{}".format(voltage_unit),
            )
            del waveform_graph
        except AttributeError:
            pass
        try:
            waveform_graph = GraphUtility(
                x_axis_min=frequency_zoom_min,
                x_axis_max=frequency_zoom_max,
                y_axis_min=voltage_zoom_min,
                y_axis_max=voltage_zoom_max,
                logger=self.logger,
            )
            if "r" in spectrum_display:
                waveform_graph.plot(
                    self.f_zoom / METRIC_PREFIX[frequency_metric_prefix],
                    self.spectrum_array_zoom.real
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="r",
                )
            if "i" in spectrum_display:
                waveform_graph.plot(
                    self.f_zoom / METRIC_PREFIX[frequency_metric_prefix],
                    self.spectrum_array_zoom.imag
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="b",
                )
            waveform_graph.save(
                figure_path=figure_path,
                figure_name="spectrum_zoom_" + file_name,
                x_axis_label="Frequency{}".format(frequency_unit),
                y_axis_label="Voltage{}".format(voltage_unit),
            )
            del waveform_graph
            waveform_graph = GraphUtility(
                x_axis_min=frequency_zoom_min,
                x_axis_max=frequency_zoom_max,
                y_axis_min=power_zoom_min,
                y_axis_max=power_zoom_max,
                logger=self.logger,
            )
            waveform_graph.plot(
                self.r_zoom / METRIC_PREFIX[frequency_metric_prefix],
                self.power_array_dBm_zoom / METRIC_PREFIX[power_metric_prefix],
            )
            waveform_graph.save(
                figure_path=figure_path,
                figure_name="power_zoom_" + file_name,
                x_axis_label="Frequency{}".format(frequency_unit),
                y_axis_label="Power{}".format(power_unit),
            )
            del waveform_graph
        except AttributeError:
            pass

    def show(
        self,
        time_metric_prefix="",
        voltage_metric_prefix="",
        frequency_metric_prefix="",
        power_metric_prefix="",
        time_min=None,
        time_max=None,
        voltage_min=None,
        voltage_max=None,
        frequency_min=None,
        frequency_max=None,
        power_min=None,
        power_max=None,
        time_zoom_min=None,
        time_zoom_max=None,
        voltage_zoom_min=None,
        voltage_zoom_max=None,
        frequency_zoom_min=None,
        frequency_zoom_max=None,
        power_zoom_min=None,
        power_zoom_max=None,
        waveform_display="r",
        spectrum_display="ri",
    ):
        """グラフを画面に出力する． / Output the graph to the screen.

        Parameters
        ----------
        time_metric_prefix : str, default: ""
            時間のSI接頭辞 / SI prefix of time
        voltage_metric_prefix : str, default: ""
            電圧のSI接頭辞 / SI prefix of voltage
        frequency_metric_prefix : str, default: ""
            周波数のSI接頭辞 / SI prefix of frequency
        power_metric_prefix : str, default: ""
            dB表示のSI接頭辞 / SI prefix of power
        time_min : float, default: None
            時刻の最小値 / minimum value of time
        time_max : float, default: None
            時刻の最大値 / maximum value of time
        voltage_min : float, default: None
            電圧の最小値 / minimum value of voltage
        voltage_max : float, default: None
            電圧の最大値 / maximum value of voltage
        frequency_min : float, default: None
            周波数の最小値 / minimum value of frequency
        frequency_max : float, default: None
            周波数の最大値 / maximum value of frequency
        power_min : float, default: None
            dB表示の最小値 / minimum value of power
        power_max : float, default: None
            dB表示の最大値 / maximum value of power
        time_zoom_min : float, default: None
            ズームした状態の時刻の最小値 / minimum value of time when zoomed
        time_zoom_max : float, default: None
            ズームした状態の時刻の最大値 / maximum value of time when zoomed
        voltage_zoom_min : float, default: None
            ズームした状態の電圧の最小値 / minimum value of voltage when zoomed
        voltage_zoom_max : float, default: None
            ズームした状態の電圧の最大値 / maximum value of voltage when zoomed
        frequency_zoom_min : float, default: None
            ズームした状態の周波数の最小値 / minimum value of frequency when zoomed
        frequency_zoom_max : float, default: None
            ズームした状態の周波数の最大値 / maximum value of frequency when zoomed
        power_zoom_min : float, default: None
            ズームした状態のdB表示の最小値 / minimum value of power when zoomed
        power_zoom_max : float, default: None
            ズームした状態のdB表示の最大値 / maximum value of power when zoomed
        waveform_display : str, default: "r"
            waveformのグラフの'r':実数成分を表示, 'i':虚数成分を表示 / "r":show 
            real part of waveform, "i":show imag part of waveform
        spectrum_display : str, default: "ri"
            spectrumのグラフの'r':実数成分を表示, 'i':虚数成分を表示 / "r":show 
            real part of waveform, "i":show imag part of waveform
        """
        self.logger.debug("Parameter:{}".format(get_args_of_current_function()))
        if time_metric_prefix != None:
            time_unit = " ({}s)".format(time_metric_prefix)
        else:
            time_unit = ""
            time_metric_prefix = ""
        if voltage_metric_prefix != None:
            voltage_unit = " ({}V)".format(voltage_metric_prefix)
        else:
            voltage_unit = ""
            voltage_metric_prefix = ""
        if frequency_metric_prefix != None:
            frequency_unit = " ({}Hz)".format(frequency_metric_prefix)
        else:
            frequency_unit = ""
            frequency_metric_prefix = ""
        if power_metric_prefix != None:
            power_unit = " ({}dBm)".format(power_metric_prefix)
        else:
            power_unit = ""
            power_metric_prefix = ""
        waveform_graph = GraphUtility(
            x_axis_min=time_min,
            x_axis_max=time_max,
            y_axis_min=voltage_min,
            y_axis_max=voltage_max,
            logger=self.logger,
        )
        if "r" in waveform_display:
            waveform_graph.plot(
                self.time_array / METRIC_PREFIX[time_metric_prefix],
                self.waveform_array.real / METRIC_PREFIX[voltage_metric_prefix],
                color="r",
            )
        if "i" in waveform_display:
            waveform_graph.plot(
                self.time_array / METRIC_PREFIX[time_metric_prefix],
                self.waveform_array.imag / METRIC_PREFIX[voltage_metric_prefix],
                color="b",
            )
        waveform_graph.show(
            x_axis_label="Time{}".format(time_unit),
            y_axis_label="Voltage{}".format(voltage_unit),
        )
        del waveform_graph
        waveform_graph = GraphUtility(
            x_axis_min=frequency_min,
            x_axis_max=frequency_max,
            y_axis_min=voltage_min,
            y_axis_max=voltage_max,
            logger=self.logger,
        )
        if "r" in spectrum_display:
            waveform_graph.plot(
                self.frequency_array / METRIC_PREFIX[frequency_metric_prefix],
                self.spectrum_array.real / METRIC_PREFIX[voltage_metric_prefix],
                color="r",
            )
        if "i" in spectrum_display:
            waveform_graph.plot(
                self.frequency_array / METRIC_PREFIX[frequency_metric_prefix],
                self.spectrum_array.imag / METRIC_PREFIX[voltage_metric_prefix],
                color="b",
            )
        waveform_graph.show(
            x_axis_label="Frequency{}".format(frequency_unit),
            y_axis_label="Voltage{}".format(voltage_unit),
        )
        del waveform_graph
        waveform_graph = GraphUtility(
            x_axis_min=frequency_min,
            x_axis_max=frequency_max,
            y_axis_min=power_min,
            y_axis_max=power_max,
            logger=self.logger,
        )
        waveform_graph.plot(
            self.positive_frequency_array / METRIC_PREFIX[frequency_metric_prefix],
            self.power_array_dBm / METRIC_PREFIX[power_metric_prefix],
        )
        waveform_graph.show(
            x_axis_label="Frequency{}".format(frequency_unit),
            y_axis_label="Power{}".format(power_unit),
        )
        del waveform_graph
        try:
            waveform_graph = GraphUtility(
                x_axis_min=time_zoom_min,
                x_axis_max=time_zoom_max,
                y_axis_min=voltage_zoom_min,
                y_axis_max=voltage_zoom_max,
                logger=self.logger,
            )
            if "r" in waveform_display:
                waveform_graph.plot(
                    self.t_zoom / METRIC_PREFIX[time_metric_prefix],
                    self.waveform_array_zoom.real
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="r",
                )
            if "i" in waveform_display:
                waveform_graph.plot(
                    self.t_zoom / METRIC_PREFIX[time_metric_prefix],
                    self.waveform_array_zoom.imag
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="b",
                )
            waveform_graph.show(
                x_axis_label="Time{}".format(time_unit),
                y_axis_label="Voltage{}".format(voltage_unit),
            )
            del waveform_graph
        except AttributeError:
            pass
        try:
            waveform_graph = GraphUtility(
                x_axis_min=frequency_zoom_min,
                x_axis_max=frequency_zoom_max,
                y_axis_min=voltage_zoom_min,
                y_axis_max=voltage_zoom_max,
                logger=self.logger,
            )
            if "r" in spectrum_display:
                waveform_graph.plot(
                    self.f_zoom / METRIC_PREFIX[frequency_metric_prefix],
                    self.spectrum_array_zoom.real
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="r",
                )
            if "i" in spectrum_display:
                waveform_graph.plot(
                    self.f_zoom / METRIC_PREFIX[frequency_metric_prefix],
                    self.spectrum_array_zoom.imag
                    / METRIC_PREFIX[voltage_metric_prefix],
                    color="b",
                )
            waveform_graph.show(
                x_axis_label="Frequency{}".format(frequency_unit),
                y_axis_label="Voltage{}".format(voltage_unit),
            )
            del waveform_graph
            waveform_graph = GraphUtility(
                x_axis_min=frequency_zoom_min,
                x_axis_max=frequency_zoom_max,
                y_axis_min=power_zoom_min,
                y_axis_max=power_zoom_max,
                logger=self.logger,
            )
            waveform_graph.plot(
                self.r_zoom / METRIC_PREFIX[frequency_metric_prefix],
                self.power_array_dBm_zoom / METRIC_PREFIX[power_metric_prefix],
            )
            waveform_graph.show(
                x_axis_label="Frequency{}".format(frequency_unit),
                y_axis_label="Power{}".format(power_unit),
            )
            del waveform_graph
        except AttributeError:
            pass
