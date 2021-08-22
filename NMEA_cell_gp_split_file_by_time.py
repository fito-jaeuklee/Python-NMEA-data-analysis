from tkinter import filedialog
import os
import glob
import re
import NMEA_cell_gp_parse

# 각각 0, 30, 60, 90 도
time_divide_by_deg = ["164800.00,165500.00", "165800.00,170500.00"]

# "164800.00,165500.00",
# "165800.00,170500.00"]
#'60', '90']

degree_list = ['60', "90"]


def create_each_degree_directory(base_dir):
    print(base_dir)
    for deg in degree_list:
        dir = os.path.join(base_dir + "/" + deg)
        if not os.path.exists(dir):
            os.mkdir(dir)


def split_file_by_time_and_save_each_directory(ubx_flag, total_gp_data, total_dict_data, degree, start_end_time, save_path):
    split_gp_data = []
    new_save_format = ""

    if ubx_flag == 1:
        new_save_format = ".ubx"
    else:
        new_save_format = ".gp"

    print("Split %s degree data" % degree)
    start_end_time_list = start_end_time.split(",")
    start_time = start_end_time_list[0]
    end_time = start_end_time_list[1]
    with open(save_path + "/" + degree + "/" + "test_gp_split_deg%s" %degree + new_save_format, 'w') as fw:
        print("Split time check = ", total_dict_data[start_time], total_dict_data[end_time])
        for i in range(total_dict_data[start_time], total_dict_data[end_time]):
            split_gp_data.append(total_gp_data[i])
            fw.write(total_gp_data[i])


def find_split_index_by_timeline():
    cell_datestrings_dic = {}
    cut_time_list = []
    timeline_cnt = 0
    ubx_flag = 0

    all_file_path_glob = filedialog.askdirectory()
    print(all_file_path_glob)
    gp_file_path = glob.glob(os.path.join(all_file_path_glob, "*.gp"))

    print(gp_file_path)
    if len(gp_file_path) == 0:
        print("Ublox file.")
        ubx_flag = 1
        gp_file_path = glob.glob(os.path.join(all_file_path_glob, "*.ubx"))
    else:
        print("GP file")
        ubx_flag = 0

    print(gp_file_path)
    # Remove useless data & line checksum
    NMEA_cell_gp_parse.erase_ubx_gp_dummy_data_and_checksum(gp_file_path)

    create_each_degree_directory(all_file_path_glob)

    with open(gp_file_path[0], 'rb') as fc:
        cell_barr = fc.readlines()
        if 'start' in str(cell_barr[0]):
            print("Dummy(~~~~start) data in this file")
            cell_barr[0] = cell_barr[0][12:]
            print(cell_barr[0])
        cell_nmea_data = [y.decode('utf-8') for y in cell_barr]

    for buf in cell_nmea_data:
        if "GGA" in buf:
            print("123", buf)
            cell_data_split_list = buf.split(',')
            print("Split , =", cell_data_split_list)
            print("Time split = ", cell_data_split_list[1])

            cell_datestrings_dic[cell_data_split_list[1]] = timeline_cnt
        timeline_cnt += 1

    print(cell_datestrings_dic)
    std_key_gp_time_keys = list(cell_datestrings_dic.keys())
    for i in range(0, len(degree_list)):
        split_file_by_time_and_save_each_directory(ubx_flag, cell_nmea_data, cell_datestrings_dic,
                                                   degree_list[i], time_divide_by_deg[i], all_file_path_glob)


find_split_index_by_timeline()