import math
import time
import matplotlib.pyplot as plt
import numpy
from tkinter import filedialog

# ['1', '7', '42.7', '0', '0.0', 'N', '0', '0.0', 'W', '0.0', '1', '0', '7', '99.99', '0.0', '\n']

filepath = '/Users/jaeuklee/Downloads/7월16일/' \
           'CLBX-4A-21_1.2_0_1626401668_0/CLBX-4A-21_1.2_0_1626401668_0_filtered.txt'

GT_filepath = '/Users/jaeuklee/Downloads/7월16일/rtk_test_7_16/Testlog_Rover_RTK_F9P_2021-07-16_filtered.txt'


def gps_to_ecef_custom(lat, lon, alt):
    rad_lat = lat * (math.pi / 180.0)
    rad_lon = lon * (math.pi / 180.0)

    a = 6378137.0
    finv = 298.257223563
    f = 1 / finv
    e2 = 1 - (1 - f) * (1 - f)
    v = a / math.sqrt(1 - e2 * math.sin(rad_lat) * math.sin(rad_lat))

    x = (v + alt) * math.cos(rad_lat) * math.cos(rad_lon)
    y = (v + alt) * math.cos(rad_lat) * math.sin(rad_lon)
    z = (v * (1 - e2) + alt) * math.sin(rad_lat)

    return x, y, z


def ECEF_2D_data_extract(filepath):
    with open(filepath, 'rb') as f:
        barr = f.readlines()
        str_nmea_data = [x.decode('utf-8') for x in barr]

    print("?????", len(str_nmea_data), str_nmea_data[0], str_nmea_data[1], str_nmea_data[2])
    nmea_data_split_list = str_nmea_data[0].split(' ')
    # print(nmea_data_split_list)

    return str_nmea_data


def make_lla_list(str_nmea_data):
    lat = []
    lon = []
    alt = []

    lla_coords = []

    for buf in str_nmea_data:
        nmea_data_split_list = buf.split(' ')
        lat_buf = float(nmea_data_split_list[3] + "." + nmea_data_split_list[4].replace(".", ""))
        lon_buf = float(nmea_data_split_list[6] + "." + nmea_data_split_list[7].replace(".", ""))
        alt_buf = float(nmea_data_split_list[9])

        lla_coords.append((lat_buf, lon_buf, alt_buf))

        # print(nmea_data_split_list[4], nmea_data_split_list[7])
        # print("lat", lat)
        # print("lon", lon)
        # print("alt", alt)
        print("jaeuk3", len(lla_coords))

    return lla_coords


def lla_to_ecef_list(lla_list):
    x_list = []
    y_list = []
    z_list = []

    for buf in lla_list:
        # print(buf)
        x, y, z = gps_to_ecef_custom(buf[0], buf[1], buf[2])
        x_list.append(x)
        y_list.append(y)

    # print(x_list, y_list)

    return x_list, y_list


def ECEF_2D_plotting(GT_X, GT_Y, X, Y, cell_path):
    plt.rcParams["figure.figsize"] = (18, 12)
    plt.title("ECEF 2D graph")
    print("Cell length =", len(X))
    print("GT length = ", len(GT_X))
    plt.plot(X, Y, label='CELL', color='red')
    plt.plot(GT_X, GT_Y, label='GT', color='blue')
    plt.savefig(cell_path[:-3] + '_2d_position' + '.png', dpi=300)
    print("2D position graph DONE!")
    # plt.show()


def ECEF_2D_save_only_cell_3min(x, y, cell_path):
    sum_error_distance = 0
    print("asd", cell_path)
    plt.rcParams["figure.figsize"] = (18, 12)
    plt.title("ECEF 2D graph")
    plt.plot(x, y, label='CELL', color='red')
    x_mean = numpy.mean(x)
    y_mean = numpy.mean(y)
    # 평균점을 원점으로 삼고 다른 점과의 거리를 오차로 생각하여 비교
    print(x_mean, y_mean)
    for i, j in zip(x, y):
        x_delta = x_mean - i
        y_delta = y_mean - j
        error_distance = math.sqrt(math.pow(x_delta, 2) + math.pow(y_delta, 2))
        sum_error_distance += error_distance
    mae = sum_error_distance/len(x)

    standard_dev_file_name = open( cell_path[:-14] +"Position mean absolute error(MAE)=" + str(round(mae, 4)) + '.txt', 'w')
    standard_dev_file_name.close()

    plt.savefig(cell_path[:-3] + '_2d_3_min_position' + '.png', dpi=300)
    print("ECEF_2D_save_only_cell_3min DONE!")


def NMEA_2d_plot_main(gt_path, cell_path):
    print(gt_path)
    print(cell_path)
    # ----------- cell data---------------
    str_nmea_data = ECEF_2D_data_extract(cell_path)
    lla_list = make_lla_list(str_nmea_data)
    print(len(lla_list))
    x_list, y_list = lla_to_ecef_list(lla_list)
    print("0000", len(x_list), len(y_list))

    # ECEF_2D_save_only_cell_3min(x_list, y_list, cell_path)

    # ----------- RTK(GT) data--------------
    print("=============================================")

    GT_nmea_data = ECEF_2D_data_extract(gt_path)
    GT_lla_list = make_lla_list(GT_nmea_data)
    print(len(GT_lla_list))
    GT_x_list, GT_y_list = lla_to_ecef_list(GT_lla_list)

    print("1111", len(GT_x_list), len(GT_y_list))

    ECEF_2D_plotting(x_list, y_list, GT_x_list, GT_y_list, cell_path)

# gt_txt_file_path = filedialog.askopenfilename()
# cell_txt_filepath = filedialog.askopenfilename()
# NMEA_2d_plot_main(gt_txt_file_path, cell_txt_filepath)
