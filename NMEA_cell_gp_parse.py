import itertools
import time
import glob
import os
from tkinter import filedialog
import os
import glob

all_file_path_glob = filedialog.askdirectory()
print(all_file_path_glob)


class GGA_toggle_flag:
    pass


# GGA로 시작되는 리스트의 위치 찾기
def index_for_GGA(sentence_list):
    # print("")
    cnt = 0
    index_cnt_list = []

    for sentence in sentence_list:
        s = sentence
        target = 'GGA'
        index = -1
        while True:
            # print(index)
            index = s.find(target, index + 1)
            if index == -1:
                cnt += 1
                break
            else:
                # print(sentence, cnt)
                index_cnt_list.append(cnt)
    # print(index_cnt_list)
    index_cnt_list = index_cnt_list[:-1]

    return index_cnt_list


def rtn_total_chunk_data():
    check_flag = 0
    list_add_flag = 0
    one_chunk_data = []
    total_chunk_data = []

    gp_file_path = glob.glob\
        (os.path.join(all_file_path_glob, "*.gp"))

    print(gp_file_path)
    # gp_file_path_list = gp_file_path[0].split('/')
    # gp_file_path_len = len(gp_file_path_list)
    # gp_file_name = gp_file_path_list[gp_file_path_len - 1]

    for path in gp_file_path:
        with open(path, 'rb') as f:
            barr = f.readlines()
            print(barr[0])
            barr[0] = barr[0][12:]
            print(barr[0])
            str_nmea_data = [x.decode('utf-8') for x in barr]
            # print(str_nmea_data)
            index_cnt_list = index_for_GGA(str_nmea_data)

            for i in index_cnt_list:
                for j in range(i, i+9):
                    one_chunk_data.append(str_nmea_data[j])
                print(one_chunk_data)
                total_chunk_data.append(one_chunk_data)
                one_chunk_data = []
                # print(total_chunk_data)

        return total_chunk_data, gp_file_path





