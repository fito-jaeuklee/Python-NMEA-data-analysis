from datetime import datetime
from tkinter import filedialog
import NMEA_graph_2D as nmea2d
import math
import glob
import os
import numpy as np

# 2d position error(mean) / speed error(mean) / test time / portion of used data
# 7140 / 15343
# 데이터가 없는 시간 계산 알고리즘
# 시간을 먼저 만들어 놓고 채워 넣어서 없는 부분을 찾아(곱하기) 계산


# Extract test degree from
folder_index_list = ['60', '90']

offset_x = 0
offset_y = 0


def decision_start_time_end_time_extract_from_txt(GT_txt_path, cell_txt_path):
    gt_datestrings = []
    cell_datestrings = []

    # ---------------- GT time -----------------------
    with open(GT_txt_path, 'rb') as f:
        barr = f.readlines()
        gt_nmea_data = [x.decode('utf-8') for x in barr]

    gt_data_split_list = gt_nmea_data[0].split(' ')

    for buf in gt_nmea_data:

        gt_data_split_list = buf.split(' ')
        gt_seconds_digit_split_by_zfill = gt_data_split_list[2].split('.')
        gt_seconds_digit_split_by_zfill[0] = gt_seconds_digit_split_by_zfill[0].zfill(2)
        gt_datestrings.append(gt_data_split_list[0] + ":" + gt_data_split_list[1].zfill(2) + ":" +
                              gt_seconds_digit_split_by_zfill[0] + '.' + gt_seconds_digit_split_by_zfill[1])

    # -----------------cell time ----------------------
    with open(cell_txt_path, 'rb') as fc:
        cell_barr = fc.readlines()
        cell_nmea_data = [y.decode('utf-8') for y in cell_barr]

    cell_data_split_list = cell_nmea_data[0].split(' ')

    for buf in cell_nmea_data:
        cell_data_split_list = buf.split(' ')
        cell_seconds_digit_split_by_zfill = cell_data_split_list[2].split('.')
        cell_seconds_digit_split_by_zfill[0] = cell_seconds_digit_split_by_zfill[0].zfill(2)
        cell_datestrings.append(cell_data_split_list[0] + ":" + cell_data_split_list[1].zfill(2) + ":" +
                                cell_seconds_digit_split_by_zfill[0] + '.' + cell_seconds_digit_split_by_zfill[1])
    # print(gt_datestrings)
    print("GT start time = ", gt_datestrings[0])
    print("GT end time = ", gt_datestrings[len(gt_datestrings) - 1])

    print("Cell start time = ", cell_datestrings[0])
    print("Cell end time = ", cell_datestrings[len(cell_datestrings) - 1])

    if datetime.strptime(gt_datestrings[0], "%H:%M:%S.%f") > datetime.strptime(cell_datestrings[0], "%H:%M:%S.%f"):
        print("here")
        start_time = datetime.strptime(gt_datestrings[0], "%H:%M:%S.%f")
    else:
        print("here2")
        start_time = datetime.strptime(cell_datestrings[0], "%H:%M:%S.%f")

    if datetime.strptime(gt_datestrings[len(gt_datestrings) - 1], "%H:%M:%S.%f") > datetime.strptime(
            cell_datestrings[len(cell_datestrings) - 1], "%H:%M:%S.%f"):
        print("here3")
        end_time = datetime.strptime(cell_datestrings[len(cell_datestrings) - 1], "%H:%M:%S.%f")
    else:
        print("here4")
        end_time = datetime.strptime(gt_datestrings[len(gt_datestrings) - 1], "%H:%M:%S.%f")

    print("Final data use time = ", start_time, end_time)
    print("gt time list =", gt_datestrings)
    print("cell time list =", cell_datestrings)

    return start_time, end_time, gt_datestrings, cell_datestrings


def search_GT_cell_start_end_index_by_follow_time(start_time, end_time, gt_time_list, cell_time_list):
    gt_eval_use_list_index_5Hz = []
    cell_eval_use_list_index_10_to_5Hz = []
    std_key_gt_time_value_cell_time = {}
    cell_time_list_index_match_to_gt_time_list = []
    # my_dict["Name"].append("Guru")
    not_matched_cnt = 0

    gt_time_index_cnt = 0

    print(str(start_time), str(end_time))
    start_time = datetime.strftime(start_time, "%H:%M:%S.%f")
    end_time = datetime.strftime(end_time, "%H:%M:%S.%f")
    start_time = start_time[1:-5]
    end_time = end_time[1:-5]

    print(start_time, end_time)

    gt_start_time_index = gt_time_list.index(gt_time_list[0])
    gt_end_time_index = gt_time_list.index(gt_time_list[len(gt_time_list) - 1])

    for i in range(gt_start_time_index, gt_end_time_index + 1, 1):
        std_key_gt_time_value_cell_time[gt_time_list[i]] = ""

    std_key_gt_time_keys = list(std_key_gt_time_value_cell_time.keys())

    for time_buf in std_key_gt_time_keys:
        try:
            std_key_gt_time_value_cell_time[time_buf] = cell_time_list.index(time_buf)
        except:
            print("Not match this time =", time_buf)
            not_matched_cnt += 1
            pass
    print(std_key_gt_time_value_cell_time)

    # key를 gt_time_index_list 로 변경
    # 즉 key = gt_time_index_list / Value cell_time_index_list (빠지는거 있음)
    # dictionary[new_key] = dictionary[old_key]
    # del dictionary[old_key]
    # Or in 1
    # step:
    #
    # dictionary[new_key] = dictionary.pop(old_key)

    for new_key in range(gt_start_time_index, gt_end_time_index, 1):
        # print(std_key_gt_time_keys[new_key])
        try:
            std_key_gt_time_value_cell_time[new_key] = std_key_gt_time_value_cell_time[std_key_gt_time_keys[new_key]]
            del std_key_gt_time_value_cell_time[std_key_gt_time_keys[new_key]]
        except:
            print("Except error")
            pass

    # RTK는 빠지는게 없어야함
    print("&&&&&&&&&&&&", std_key_gt_time_value_cell_time)
    print("Not match data number =", not_matched_cnt)

    print("gt_time_list.index(start_time) =", gt_time_list.index(gt_time_list[0]))
    print("gt_time_list.index(end_time) =", gt_time_list.index(gt_time_list[len(gt_time_list) - 1]))
    print("")
    for z in range(0, len(gt_time_list)):
        try:
            print("cell_time_list.index(start_time) =", cell_time_list.index(gt_time_list[z]))
            break
        except:
            pass
    for j in range(1, len(gt_time_list)):
        try:
            print("cell_time_list.index(start_time) =", cell_time_list.index(gt_time_list[len(gt_time_list) - j]))
            break
        except:
            pass

    print("gt time list len / cell time list len = ", len(gt_time_list), len(cell_time_list))

    return std_key_gt_time_value_cell_time, not_matched_cnt


def save_lla_coords_and_speed_from_txt(filepath):
    lla_coords = []
    speed_list = []

    sat_sum = 0
    hdop_sum = 0

    alt_sum = 0
    sum_alt_diff = 0
    satellites_used = 0

    with open(filepath, 'rb') as f:
        barr = f.readlines()
        str_nmea_data = [x.decode('utf-8') for x in barr]

    for buf in str_nmea_data:
        nmea_data_split_list = buf.split(' ')
        lat_buf = float(nmea_data_split_list[3] + "." + nmea_data_split_list[4].replace(".", ""))
        lon_buf = float(nmea_data_split_list[6] + "." + nmea_data_split_list[7].replace(".", ""))
        alt_buf = float(nmea_data_split_list[9])

        sat_sum += float(nmea_data_split_list[11])
        hdop_sum += float(nmea_data_split_list[13])
        alt_sum += alt_buf

        speed_list.append(float(nmea_data_split_list[14]))
        lla_coords.append((lat_buf, lon_buf, alt_buf))



    # Calculate variance of altitude
    print("var")
    print(lla_coords[0], lla_coords[0][2], len(lla_coords))
    alt_mean = alt_sum / len(lla_coords)
    sat_used_mean = sat_sum / len(lla_coords)
    hdop_mean = hdop_sum / len(lla_coords)

    for alt in lla_coords:
        sum_alt_diff += math.pow(alt[2] - alt_mean, 2)
    alt_variance = sum_alt_diff / len(lla_coords)
    alt_std_deviation = math.sqrt(alt_variance)
    print(alt_variance)

    return lla_coords, speed_list, alt_std_deviation, sat_used_mean, hdop_mean


def compare_evaluation_value_gt_cell(dict_gt_cell, GT_file_path_glob, Cell_file_path_glob):
    gt_lla_coords = []
    cell_lla_coords = []

    gt_speed_list = []
    cell_speed_list = []

    gt_vs_cell_speed = []

    gt_ecef_list = []
    cell_ecef_list = []

    gt_vs_cell_x = []
    gt_vs_cell_y = []
    gt_vs_cell_speed = []

    # GT and Cell LLA to ECEF coords from txt file

    gt_lla_coords, gt_speed_list, gt_altitude_var, gt_sat_used_mean, gt_hdop_mean = \
        save_lla_coords_and_speed_from_txt(GT_file_path_glob)
    cell_lla_coords, cell_speed_list, cell_altitude_var, cell_sat_used_mean, cell_hdop_mean = \
        save_lla_coords_and_speed_from_txt(Cell_file_path_glob)

    print("lla length check = ", len(gt_lla_coords), len(cell_lla_coords))

    gt_ecef_list_x, gt_ecef_list_y = nmea2d.lla_to_ecef_list(gt_lla_coords, cell_path)
    cell_ecef_list_x, cell_ecef_list_y = nmea2d.lla_to_ecef_list(cell_lla_coords, cell_path)

    print("ecef length check = ", len(gt_ecef_list), len(cell_ecef_list))

    # Follow dictionary of gt cell data index list, each data append

    print("$%^ = ", dict_gt_cell)
    dict_gt_cell = dict_gt_cell
    print(list(dict_gt_cell.keys())[0])
    print(list(dict_gt_cell.keys())[len(dict_gt_cell) - 1])

    gt_start_index = list(dict_gt_cell.keys())[1]
    gt_end_index = list(dict_gt_cell.keys())[len(dict_gt_cell) - 1]

    for i in range(gt_start_index, gt_end_index + 1):
        if dict_gt_cell[i] == '':
            print("This index data has no VALUE")
        else:
            # list key value 따라 ecef 데이터와 스피드 데이터 넣기
            print("(((", i, dict_gt_cell[i])
            gt_vs_cell_x.append([gt_ecef_list_x[i], cell_ecef_list_x[dict_gt_cell[i]]])
            gt_vs_cell_y.append([gt_ecef_list_y[i], cell_ecef_list_y[dict_gt_cell[i]]])
            gt_vs_cell_speed.append([gt_speed_list[i], cell_speed_list[dict_gt_cell[i]]])

    #print("VS", gt_vs_cell_x, gt_vs_cell_y, gt_vs_cell_speed)
    print("VS", gt_vs_cell_x)
    print("VS length = ", len(gt_vs_cell_x), len(gt_vs_cell_y), len(gt_vs_cell_speed))

    avr=np.average(gt_vs_cell_x[:][0])
    print(avr)
    x_sum=0
    x_gt_sum=0
    x_cell_sum=0
    y_gt_sum=0
    y_cell_sum=0

    for i in range(0, len(gt_vs_cell_x)):
        x_gt_sum += gt_vs_cell_x[i][0]
        x_cell_sum += gt_vs_cell_x[i][1]
        y_gt_sum += gt_vs_cell_y[i][0]
        y_cell_sum += gt_vs_cell_y[i][1]

    x_gt_avg = x_gt_sum / len(gt_vs_cell_x)
    x_cell_avg = x_cell_sum / len(gt_vs_cell_x)
    y_gt_avg = y_gt_sum / len(gt_vs_cell_x)
    y_cell_avg = y_cell_sum / len(gt_vs_cell_x)
    print(x_gt_avg)
    print(x_cell_avg)
    print(y_gt_avg)
    print(y_cell_avg)

    for i in range(0, len(gt_vs_cell_x)):
        gt_vs_cell_x[i][0]= gt_vs_cell_x[i][0]-x_gt_avg
        gt_vs_cell_x[i][1]= gt_vs_cell_x[i][1]-x_cell_avg
        gt_vs_cell_y[i][0]= gt_vs_cell_y[i][0]-y_gt_avg
        gt_vs_cell_y[i][1]= gt_vs_cell_y[i][1]-y_cell_avg

    offset_x= x_gt_avg -x_cell_avg
    offset_y = y_gt_avg - y_cell_avg
    print(offset_x)
    print(offset_y)

    OFFSET_xy= math.sqrt(math.pow(offset_x, 2) + math.pow(offset_y, 2))
    print(OFFSET_xy)
    return OFFSET_xy,gt_vs_cell_x, gt_vs_cell_y, gt_vs_cell_speed, cell_altitude_var, cell_sat_used_mean, cell_hdop_mean


def calculate_xy_position_and_speed_mean_error(gt_vs_cell_x, gt_vs_cell_y, gt_vs_cell_speed):
    euclidean_distance_sum = 0
    speed_diff_sum = 0
    data_len = len(gt_vs_cell_speed)

    #print(gt_vs_cell_x[0], gt_vs_cell_x[0][1], gt_vs_cell_x[0][0])

    print('chulwoo park2')

    for i in range(0, len(gt_vs_cell_x)):
        print(i)
        x_delta = gt_vs_cell_x[i][1] - gt_vs_cell_x[i][0]
        y_delta = gt_vs_cell_y[i][1] - gt_vs_cell_y[i][0]

        euclidean_distance_sum += math.sqrt(math.pow(x_delta, 2) + math.pow(y_delta, 2))

        speed_delta = gt_vs_cell_speed[i][1] - gt_vs_cell_speed[i][0]
        speed_diff_sum += math.pow(speed_delta, 2)

    xy_position_mean_error = euclidean_distance_sum / data_len
    speed_mean_error = math.sqrt(speed_diff_sum / data_len)

    return xy_position_mean_error, speed_mean_error


# 각도에 따라 파일 하나하나 불러오지 않도록 폴더 하나 지정하면, 폴더 0 / 30 / 60 / 90도 로 불러와서 분석할 수 있도록

GT_file_path_glob = filedialog.askdirectory()
Cell_file_path_glob = filedialog.askdirectory()

gt_full_txt_file_path = []
cell_full_txt_file_path = []

print("GLOB")
print(GT_file_path_glob)
print(Cell_file_path_glob)


for i in range(0, len(folder_index_list)):
    Cell_file_path_glob_add_degree = Cell_file_path_glob + '/' + folder_index_list[i]
    gt_file_path_glob_add_degree = GT_file_path_glob + '/' + folder_index_list[i]

    cell_full_txt_file_path.append(glob.glob(os.path.join(Cell_file_path_glob_add_degree, "*_filtered.txt")))
    gt_full_txt_file_path.append(glob.glob(os.path.join(gt_file_path_glob_add_degree, "*_filtered.txt")))

# cell_full_txt_file_path.append(glob.glob(os.path.join("/Users/jaeuklee/Downloads/8월18일_분석완/CELL", "*_filtered.txt")))
# gt_full_txt_file_path.append(glob.glob(os.path.join("/Users/jaeuklee/Downloads/8월18일_분석완/GT", "*_filtered.txt")))


print("final path list")
print(gt_full_txt_file_path)
print(cell_full_txt_file_path)

for cell_path, gt_path in zip(cell_full_txt_file_path, gt_full_txt_file_path):
    print("Show me the file path")
    print("---", cell_path[0])
    print("+++", gt_path[0])

    start_time, end_time, gt_time_list, cell_time_list = \
        decision_start_time_end_time_extract_from_txt(gt_path[0], cell_path[0])

    dict_key_gt_time_list_matched_cell_time_list_index, not_match_num = search_GT_cell_start_end_index_by_follow_time \
        (start_time, end_time, gt_time_list, cell_time_list)

    print(len(dict_key_gt_time_list_matched_cell_time_list_index))

    # position_OFFSET, gt_vs_cell_x, gt_vs_cell_y, gt_vs_cell_speed, cell_altitude_std, cell_sat_used_mean, cell_hdop_mean = \
    #     compare_evaluation_value_gt_cell(dict_key_gt_time_list_matched_cell_time_list_index, gt_path[0], cell_path[0])
    #
    # position_mean_error, speed_mean_error = calculate_xy_position_and_speed_mean_error(gt_vs_cell_x, gt_vs_cell_y,
    #                                                                                    gt_vs_cell_speed)
    #
    # print("-----------------", cell_path[0], "------------------")
    # print("Test start time =", start_time)
    # print("Test end time =", end_time)
    # print("Total estimation time = ", end_time - start_time)
    # print("Time used percentage = ", (len(gt_time_list) - not_match_num) / len(gt_time_list))
    # print()
    # print("X-Y position difference mean(Meters) = ", position_mean_error)
    # print("Speed difference mean(km/h) = ", speed_mean_error)
    # print("Standard deviation of altitude [Test cell] = ", cell_altitude_std)
    # print("Mean of satellites used number [Test cell] =", cell_sat_used_mean)
    # print("Mean of HDOP [Test cell] = ", cell_hdop_mean)
    #
    # print("-------------------------------------")
    # print("Save TXT data & 2D position plot")
    # analysis_data_file = open(cell_path[0][:-13] + '_analysis_data' + '.txt', 'w')
    # analysis_data_file.write("X-Y position mean absolute error(MAE) = %.3f \n" % position_mean_error)
    # analysis_data_file.write("\n")
    # analysis_data_file.write("X-Y position OFFSET = %.3f \n" % position_OFFSET)
    # analysis_data_file.write("\n")
    # analysis_data_file.write("Speed root-mean square difference(RMSD) = %.3f \n" % speed_mean_error)
    # analysis_data_file.write("\n")
    # analysis_data_file.write("Standard deviation of altitude [Cell] = %.3f \n" % cell_altitude_std)
    # analysis_data_file.write("\n")
    # analysis_data_file.write("Mean of satellites used number [Cell] = %.3f \n" % cell_sat_used_mean)
    # analysis_data_file.write("\n")
    # analysis_data_file.write("Mean of HDOP [Cell] = %.3f \n" % cell_hdop_mean)

    nmea2d.NMEA_2d_plot_main(gt_path[0], cell_path[0])

# nmea2d.ECEF_2D_save_only_cell_3min('/Users/jaeuklee/Downloads/8월18일_분석완/CELL_only_human/dual/human_dual._filtered.txt')
# nmea2d.ECEF_2D_save_only_cell_3min('/Users/jaeuklee/Downloads/8월18일_분석완/CELL_only_human/single/human_single._filtered.txt')


# cell_path = []
# gt_path =[]
#
# gt_path.append('/Users/jaeuklee/Downloads/7월27일_분석완/GT_zed-f9p/human/test_2021-07-27_human_filtered.txt')
# cell_path.append('/Users/jaeuklee/Downloads/7월27일_분석완/GT_zed-f9p/human/test_2021-07-27_human_filtered.txt')
#
# nmea2d.NMEA_2d_plot_main(gt_path[0], cell_path[0])
