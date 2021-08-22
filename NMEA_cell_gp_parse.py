import itertools
import time
import glob
import os
from tkinter import filedialog
import os
import glob
import re



fix_mode_mapping_dict = {'N': 0, 'E': 1, 'F': 2, 'R': 3, 'D': 0, 'A': 1, '': 0}

# all_file_path_glob = filedialog.askdirectory()
# print(all_file_path_glob)


# ex) $GNRMC,074730.70,A,3731.05452,N,12658.18911,E,0.165,,190821,,,D,V*18
def extract_position_fix_mode_from_RMC(one_chuck_data):
    find_berry = 'RMC'
    select_i = 0

    print(one_chuck_data)
    # berries = [i for i in range(len(one_chuck_data)) if find_berry in one_chuck_data[i]]

    for i in range(len(one_chuck_data)):
        if find_berry in one_chuck_data[i]:
            print("find ", i)
            select_i = i
        else:
            print("RMC not exist ", i)

    print("resultlll", one_chuck_data[select_i])

    if find_berry in one_chuck_data[select_i]:
        b_list = one_chuck_data[select_i].split(",")
        print(b_list)
        print(b_list[len(b_list) - 2])
        return fix_mode_mapping_dict[b_list[len(b_list) - 2]]
    else:
        print("not RMC return 0")
        return 0


# ex) $PUBX,00,074730.60,3731.05453,N,12658.18909,E,22.028,D3,5.1,15,0.351,0.00,0.090,1.6,3.99,7.40,6.41,4,0,0*56
def extract_altitude_satellite_num_from_PUBX(one_chuck_data):
    find_berry = 'PUBX,00'
    select_i = 0

    print(one_chuck_data)
    # berries = [i for i in range(len(one_chuck_data)) if find_berry in one_chuck_data[i]]

    for i in range(len(one_chuck_data)):
        if find_berry in one_chuck_data[i]:
            print("find ", i)
            select_i = i
        else:
            print("PUBX not exist ", i)

    print("resultlll", one_chuck_data[select_i])

    if find_berry in one_chuck_data[select_i]:
        b_list = one_chuck_data[select_i].split(",")
        print("pubx = ", b_list)
        return b_list[7], b_list[18]
    else:
        print("not PUBX return 0")
        return 0


def chksum_nmea(sentence):
    # This is a string, will need to convert it to hex for
    # proper comparsion below
    cksum = sentence[len(sentence) - 2:]

    # String slicing: Grabs all the characters
    # between '$' and '*' and nukes any lingering
    # newline or CRLF
    chksumdata = re.sub("(\n|\r\n)", "", sentence[sentence.find("$") + 1:sentence.find("*")])

    # Initializing our first XOR value
    csum = 0

    # For each char in chksumdata, XOR against the previous
    # XOR'd char.  The final XOR of the last char will be our
    # checksum to verify against the checksum we sliced off
    # the NMEA sentence

    for c in chksumdata:
        # XOR'ing value of csum against the next char in line
        # and storing the new XOR value in csum
        csum ^= ord(c)

    # Do we have a validated sentence?
    try:
        if hex(csum) == hex(int(cksum, 16)):
           return True
    except:
        pass

    return False


def erase_ubx_gp_dummy_data_and_checksum(filepath):
    print(filepath)
    decoded_data_list = []
    decode_error_cnt = 0
    checksum_error_cnt = 0
    carriage_rtn_value_set = 0

    for path in filepath:
        print("jaeuk path", path)
        with open(path, 'rb') as f:
            barr = f.readlines()
            for x in barr:
                try:
                    str_nmea_data = x.decode('utf-8')
                    decoded_data_list.append(str_nmea_data)
                except:
                    decode_error_cnt += 1
        print("barr", barr)
        print("decoded = ", decoded_data_list)

    # ubx 는 -1
    # gp 파일 일때는 -2 로
    # one_line_nmea[:()]

    if ".ubx" in path:
        print(".UBX here")
        carriage_rtn_value_set = -2
    else:
        print(".GP here")
        carriage_rtn_value_set = -2

    with open(path, "w") as new_file:
        for one_line_nmea in decoded_data_list:
            # new_file.write(one_line_nmea)
            # print(one_line_nmea[:carriage_rtn_value_set])
            checksum_rtn = chksum_nmea(one_line_nmea[:carriage_rtn_value_set])
            if checksum_rtn:
                new_file.write(one_line_nmea)
            elif not checksum_rtn:
                checksum_error_cnt += 1
            else:
                print("Not either True or False")

    print("Decode error count = ", decode_error_cnt)
    print("Checksum error count = ", checksum_error_cnt)


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


def rtn_total_chunk_data(all_file_path_glob):
    check_flag = 0
    list_add_flag = 0
    one_chunk_data = []
    total_chunk_data = []

    gp_file_path = glob.glob(os.path.join(all_file_path_glob, "*.gp"))

    print(gp_file_path)
    if len(gp_file_path) == 0:
        print("Ublox file.")
        gp_file_path = glob.glob(os.path.join(all_file_path_glob, "*.ubx"))
    else:
        print("GP file")

    # # NMEA data checksum & save re-define dat
    # erase_ubx_gp_dummy_data_and_checksum(gp_file_path)
    # gp_file_path_list = gp_file_path[0].split('/')
    # gp_file_path_len = len(gp_file_path_list)
    # gp_file_name = gp_file_path_list[gp_file_path_len - 1]

    for path in gp_file_path:
        with open(path, 'rb') as f:
            barr = f.readlines()
            print(barr)
            print(barr[0])
            if 'start' in str(barr[0]):
                print("Dummy(~~~~start) data in this file")
                barr[0] = barr[0][12:]
                print(barr[0])

            # for x in barr:
            #     try:
            #         str_nmea_data = x.decode('utf-8')
            #     except:
            #         pass
            check_flag += 1
            print(check_flag)
            str_nmea_data = [x.decode('utf-8') for x in barr]

            # print(str_nmea_data)
            index_cnt_list = index_for_GGA(str_nmea_data)
            # print("index_cnt_list", index_cnt_list)
            # print("3242", index_cnt_list[1]-index_cnt_list[0])

            for i in range(0, len(index_cnt_list) - 1):
                for j in range(index_cnt_list[i],
                               (index_cnt_list[i+1]-index_cnt_list[i]) + index_cnt_list[i]):
                    print(j)
                    one_chunk_data.append(str_nmea_data[j])
                print(one_chunk_data)
                total_chunk_data.append(one_chunk_data)
                one_chunk_data = []
                # print(total_chunk_data)

        return total_chunk_data, gp_file_path

# rtn_total_chunk_data()
# erase_ubx_gp_dummy_data_and_checksum(all_file_path_glob)





