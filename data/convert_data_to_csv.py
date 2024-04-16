import csv as csv
import pmt
import sys
import numpy as np
from gnuradio.blocks import parse_file_metadata
from statistics import mean
from datetime import datetime
from heapq import nlargest

channels = [
    87.5,
    88.0,
    88.4,
    89.3,
    89.7,
    90.1,
    90.6,
    92.9,
    93.3,
    94.1,
    95.0,
    95.5,
]

dt = "24-04-16_17-39-35"
bin_files = []

for channel in channels:
    bin_files.append("fft_captures_" + dt + '_' + str(channel) + "MHz.bin")

# bin_files = [
#     "fft_captures_24-04-16_17-39-35_87.5MHz.bin",
#     "fft_captures_24-04-16_17-39-35_88.0MHz.bin",
#     "fft_captures_24-04-16_17-39-35_88.4MHz.bin",
#     "fft_captures_24-04-16_17-39-35_89.3MHz.bin",
#     "fft_captures_24-04-16_17-39-35_89.7MHz.bin",
#     "fft_captures_24-04-16_17-39-35_90.1MHz.bin",
#     "fft_captures_24-04-16_17-39-35_90.6MHz.bin",
#     "fft_captures_24-04-16_17-39-35_92.9MHz.bin",
#     "fft_captures_24-04-16_17-39-35_93.3MHz.bin",
#     "fft_captures_24-04-16_17-39-35_94.1MHz.bin",
#     "fft_captures_24-04-16_17-39-35_95.0MHz.bin",
#     "fft_captures_24-04-16_17-39-35_95.5MHz.bin",
# ]

csv_filename = "fft_captures_" + dt + ".csv"

delim = ","
max_data_segments_to_read = 100
print_output = False
np.set_printoptions(threshold=sys.maxsize)  # снимаем ограничение на вывод

# можно доставать все эти параметры из название файла
cutoff_freq = 50e3
fft_size = 1 << 10
samp_rate = 200e3
step = samp_rate / fft_size
start = int(cutoff_freq / step)
stop = start * 2

with open(csv_filename, "w") as target:
    writer = csv.writer(target, delimiter=delim)
    writer.writerow(["pwr_max", "pwr_avg3", "pwr_avg5", "pwr_avg", "freq", "dt", "utime"])  # запись заголовка

    channels_count = 0
    for filename in bin_files:
        channel_freq = int(channels[channels_count] * 1e6)
        channels_count += 1
        with open(filename, "rb") as source:
            ii = 0
            header_str = source.read(parse_file_metadata.HEADER_LENGTH)
            while header_str:
                # header_str = source.read(parse_file_metadata.HEADER_LENGTH)
                header = pmt.deserialize_str(header_str)

                if print_output:
                    print(f"\n===Data segment {ii} ===")

                header_info = parse_file_metadata.parse_header(header, print_output)
                if header_info["extra_len"] > 0:
                    extra_str = source.read(header_info["extra_len"])
                    if len(extra_str) != 0:
                        extra = pmt.deserialize_str(extra_str)
                        extra_info = parse_file_metadata.parse_extra_dict(extra, header_info, print_output)

                data = np.fromfile(file=source, dtype=np.float32, count=int(header_info['nitems']), sep='', offset=0)
                cutoff_data = data[start:stop:1]
                pwr_max = max(cutoff_data)
                pwr_avg3 = mean(nlargest(3, cutoff_data))
                pwr_avg5 = mean(nlargest(5, cutoff_data))
                pwr_avg = mean(cutoff_data)
                cutoff_data = data[start:stop:1]

                if 'ts_start' in header_info:
                    ts = pmt.to_double(header_info.get('ts_start')) + ii
                    format_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                    # timestamp записывается в .csv файл в миллисекундах
                    writer.writerow((pwr_max, pwr_avg3, pwr_avg5, pwr_avg, channel_freq, format_time, round(ts * 1e3)))

                if print_output:
                    print(f"Sliced data length: {len(cutoff_data)}; average value = {mean(cutoff_data)}")
                    print(f"{len(data)} data elements read; average value = {mean(data)}")

                ii += 1
                header_str = source.read(parse_file_metadata.HEADER_LENGTH)
        # channels_count += 1

print("Finish")
