import math
import time
import matplotlib.pyplot as plt
import numpy
from tkinter import filedialog
import utm
from pyproj import Proj, transform
import numpy as np
import pandas as pd


plotting_offset = 30
myProj = Proj(init='epsg:5178', proj='utm', zone=52, datum='WGS84')
# ['1', '7', '42.7', '0', '0.0', 'N', '0', '0.0', 'W', '0.0', '1', '0', '7', '99.99', '0.0', '\n']

filepath = '/Users/jaeuklee/Downloads/7월16일/' \
           'CLBX-4A-21_1.2_0_1626401668_0/CLBX-4A-21_1.2_0_1626401668_0_filtered.txt'

GT_filepath = '/Users/jaeuklee/Downloads/7월16일/rtk_test_7_16/Testlog_Rover_RTK_F9P_2021-07-16_filtered.txt'


def gps_to_lat_lon_conv(gps_x, gps_y):
    print(gps_x, gps_y)
    gps_x = float(gps_x * 100)
    gps_y = float(gps_y * 100)

    d_x = int(gps_x/100)
    m_x = (gps_x - (d_x * 100)) / 60

    lat = d_x + m_x

    d_y = int(gps_y/100)
    m_y = (gps_y - (d_y * 100)) / 60

    lon = d_y + m_y
    print("12314", lat, lon)

    return lat, lon


def WGS84_to_UTM_K(lat, lon):
    UTMx, UTMy = myProj(lon, lat)
    # print(x2, y2)

    return UTMx, UTMy


def lat_log_posx_posy(lat, lon):
    # px, py = [], []
    # for i in range(len(coords.lat)):
    dx = utm.from_latlon(lat, lon)
        # px.append(dx[0])
        # py.append(dx[1])
    return dx[0], dx[1]


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
        # TODO: change projection way
        # TODO: Need GPS coor to lat, lon convert
        lat, lon = gps_to_lat_lon_conv(buf[0], buf[1])
        x, y = WGS84_to_UTM_K(lat, lon)
        x_list.append(x)
        y_list.append(y)

    # new_x_list = [x - x_list[0] for x in x_list]
    # new_y_list = [y - y_list[0] for y in y_list]

    # print(x_list, y_list)

    return x_list, y_list


def ECEF_2D_plotting(GT_X, GT_Y, X, Y, cell_path):
    plt.rcParams["figure.figsize"] = (18, 12)
    plt.title("ECEF 2D graph")
    print("Cell length =", len(X))
    print("GT length = ", len(GT_X))

    plt.plot(X[50:-50], Y[50:-50], 'r-o', label='GT')
    plt.plot(GT_X[100:-100], GT_Y[100:-100], 'b-o', label='CELL')
    print(int(min(X)) - 1, int(max(X)) + 1)
    plt.xticks([i for i in range(int(min(X)) - 3, int(max(X)) + 3, 1)])
    plt.yticks([i for i in range(int(min(Y)) - 3, int(max(Y)) + 3, 1)])
    plt.legend()

    plt.grid(True)

    plt.axis('equal')
    plt.savefig(cell_path[:-3] + '_2d_position' + '.png', dpi=300)
    print("2D position graph DONE!")
    plt.show()
    plt.close()


def ECEF_2D_save_only_cell_3min(cell_path):
    print(cell_path)
    cell_datestrings = []

    with open(cell_path, 'rb') as fc:
        cell_barr = fc.readlines()
        cell_nmea_data = [y.decode('utf-8') for y in cell_barr]

    cell_data_split_list = cell_nmea_data[0].split(' ')

    for buf in cell_nmea_data:
        cell_data_split_list = buf.split(' ')
        cell_seconds_digit_split_by_zfill = cell_data_split_list[2].split('.')
        cell_seconds_digit_split_by_zfill[0] = cell_seconds_digit_split_by_zfill[0].zfill(2)
        cell_datestrings.append(cell_data_split_list[0] + ":" + cell_data_split_list[1].zfill(2) + ":" +
                                cell_seconds_digit_split_by_zfill[0] + '.' + cell_seconds_digit_split_by_zfill[1])

    print("Cell start time = ", cell_datestrings[0])
    print("Cell end time = ", cell_datestrings[len(cell_datestrings) - 1])

    # ----------- cell data---------------
    str_nmea_data = ECEF_2D_data_extract(cell_path)
    lla_list = make_lla_list(str_nmea_data)
    print(len(lla_list))
    x_list, y_list = lla_to_ecef_list(lla_list)
    print("0000", len(x_list), len(y_list))

    sum_error_distance = 0
    plt.rcParams["figure.figsize"] = (18, 12)
    axes = plt.gca()
    # axes.set_xlim([-65-3.027e6, -50-3.027e6])
    # axes.set_ylim([15+4.0786e6, 30+4.0786e6])
    print("asd", cell_path)

    # plt.rcParams["figure.figsize"] = (18, 12)
    plt.title("ECEF 2D graph")
    plt.axis('equal')
    plt.plot(x_list, y_list, label="Start time = '{0}' \n End time = '{1}'".format(str(cell_datestrings[0]), str(cell_datestrings[len(cell_datestrings) - 1])), color='red')
    plt.legend(loc='best')

    major_ticks = np.arange(min(min(x_list), min(y_list)), max(max(x_list), max(y_list)), 5)
    minor_ticks = np.arange(min(min(x_list), min(y_list)), max(max(x_list), max(y_list)), 0.1)

    plt.set_xticks(major_ticks)
    plt.set_xticks(minor_ticks, minor=True)
    plt.set_yticks(major_ticks)
    plt.set_yticks(minor_ticks, minor=True)

    plt.grid(which='both')
    plt.grid(which='minor', alpha=0.2)
    plt.grid(which='major', alpha=0.5)

    x_mean = numpy.mean(x_list)
    y_mean = numpy.mean(y_list)

    # 평균점을 원점으로 삼고 다른 점과의 거리를 오차로 생각하여 비교
    print(x_mean, y_mean)
    for i, j in zip(x_list, y_list):
        x_delta = x_mean - i
        y_delta = y_mean - j
        error_distance = math.sqrt(math.pow(x_delta, 2) + math.pow(y_delta, 2))
        sum_error_distance += error_distance
    mae = sum_error_distance/len(x_list)

    standard_dev_file_name = open( cell_path[:-14] +"Position mean absolute error(MAE)=" + str(round(mae, 4)) + '.txt', 'w')
    standard_dev_file_name.close()
    plt.show()
    plt.savefig(cell_path[:-3] + '_2d_3_min_position' + '.png', dpi=300)
    plt.close()
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
