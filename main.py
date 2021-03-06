#GGA = UTC / Lat / NS / Long / EW / GPS qual / sat Used / HDOP / Alti / Geoidal Sep / DFPS S ID / checksum
#GSA = Mode(A, M) / Fix mode(123) / Sat ID / PDOP / HDOP / VDOP / checksum
#GSV = number of msg / msg number ex )1/5 / sat in view / sat id / elevation / azimuth /snr /반복 max 4 / checksum
#RMC = UTC / status (VA) / lat / NS / Long / EW / speed / course / UTC data / Mode (NADE) / checksum

# File output(filename + 'parsed' + .txt) =
# UTC / Lat / NS / Long / EW /  satellites used # / GPS altitude / Fix mode(not, 2d, 3d) / HDOP / Speed over GND

from micropyGPS import MicropyGPS
import NMEA_cell_gp_parse
import NMEA_graph_1D
from tkinter import filedialog

folder_degree_name = ['0']
#, "30", "60", '90']
total_file_path_glob_add_degree = []

pubx_flag = 1

all_file_path_glob = filedialog.askdirectory()
print(all_file_path_glob)

#make folder list
for i in range(0, len(folder_degree_name)):
    total_file_path_glob_add_degree.append(all_file_path_glob + '/' + folder_degree_name[i])

print("^^^^^^^^^^^^^^^^=", total_file_path_glob_add_degree)

for file_path in total_file_path_glob_add_degree:
    my_gps = MicropyGPS()
    cnt = 0
    one_chunk_buf = []
    sum_chuck = []
    fix_position_list = []

    # Change 8/20 data parse from PUBX data
    altitude_high_resolution_list = []
    satellites_num_pubx_list = []

    total_chunk_data_one_file, filename = NMEA_cell_gp_parse.rtn_total_chunk_data(file_path)


    # print(total_chunk_data_one_file)
    print(len(total_chunk_data_one_file))

    if pubx_flag:
        for chuck_buf in total_chunk_data_one_file:
            fix_position_list.append(NMEA_cell_gp_parse.extract_position_fix_mode_from_RMC(chuck_buf))
            altitude_high_resolution_list.append(NMEA_cell_gp_parse.extract_altitude_satellite_num_from_PUBX(chuck_buf)[0])
            satellites_num_pubx_list.append(NMEA_cell_gp_parse.extract_altitude_satellite_num_from_PUBX(chuck_buf)[1])

    print("Fix position index list = ", fix_position_list)
    print("alti resol = ", altitude_high_resolution_list, satellites_num_pubx_list)

    for i in range(0, len(total_chunk_data_one_file)):
        for y in total_chunk_data_one_file[i]:
            # print("-----------------------------------")
            # print("sentence = ", y)
            for x in y:
                # print(x)

                out_sen = my_gps.update(x)

        one_chunk_buf.append(my_gps.timestamp)
        one_chunk_buf.append(my_gps.latitude)
        one_chunk_buf.append(my_gps.longitude)

        if pubx_flag:
            one_chunk_buf.append(altitude_high_resolution_list[cnt])
            one_chunk_buf.append(fix_position_list[cnt])
            one_chunk_buf.append(satellites_num_pubx_list[cnt])
        else:
            one_chunk_buf.append(my_gps.altitude)
            one_chunk_buf.append(my_gps.fix_type)
            one_chunk_buf.append(my_gps.satellites_in_use)

        one_chunk_buf.append(my_gps.satellites_in_view)
        one_chunk_buf.append(my_gps.hdop)
        one_chunk_buf.append(my_gps.speed[2])
        # print(one_chunk_buf)
        sum_chuck.append(one_chunk_buf)
        one_chunk_buf = []
        cnt += 1

    print(len(sum_chuck))
    print(filename)
    nmea_file_save = open(filename[0][:-3] + '_filtered' + '.txt', 'w')

    for i in range(0, len(sum_chuck)):
        # print(sum_chuck[i])

        define_new_list_from_chunck = []
        for j in range(0, 3):
            define_new_list_from_chunck.extend(sum_chuck[i][j])
        for z in range(3, 9):
            define_new_list_from_chunck.append(sum_chuck[i][z])

        for k in range(0, len(define_new_list_from_chunck)):
            print(define_new_list_from_chunck[k])
            nmea_file_save.write("%s " % str(define_new_list_from_chunck[k]))
        nmea_file_save.write("\n")
    nmea_file_save.close()

    # -------------------1D plot graph and save png----------------
    NMEA_graph_1D.NMEA_plot_and_save_png(filename[0][:-3] + '_filtered' + '.txt')

    # -------------------2D plot graph(X, Y) and save png ------------
    #--------------------Error evaluation GT vs cell ----------------


