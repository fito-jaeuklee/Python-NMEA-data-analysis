from micropyGPS import MicropyGPS
import NMEA_cell_gp_parse
import NMEA_graph

my_gps = MicropyGPS()
my_sentence = '$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62'

#GGA = UTC / Lat / NS / Long / EW / GPS qual / sat Used / HDOP / Alti / Geoidal Sep / DFPS S ID / checksum
#GSA = Mode(A, M) / Fix mode(123) / Sat ID / PDOP / HDOP / VDOP / checksum
#GSV = number of msg / msg number ex )1/5 / sat in view / sat id / elevation / azimuth /snr /반복 max 4 / checksum
#RMC = UTC / status (VA) / lat / NS / Long / EW / speed / course / UTC data / Mode (NADE) / checksum

# File output(filename + 'parsed' + .txt) = UTC / Lat / NS / Long / EW /  / satellites used # / Satellites of view / Fix mode(not, 2d, 3d) / HDOP / PDOP / VDOP /


total_chunk_data_one_file, filename = NMEA_cell_gp_parse.rtn_total_chunk_data()

test_sen = ['$GNGGA,010742.20,3742.24078,N,12707.77221,E,1,10,1.06,105.0,M,,M,,*55',

            '$GNGSA,A,3,07,17,30,08,14,21,194,195,,,,,2.16,1.06,1.88,1*0F',
            '$GNGSA,A,3,27,07,,,,,,,,,,,2.16,1.06,1.88,4*05',
            '$GNGSA,A,3,,,,,,,,,,,,,2.16,1.06,1.88,3*00',

            '$GPGSV,5,1,17,07,19,205,39,08,27,078,41,14,51,311,41,17,32,289,44,0*61',
            '$GPGSV,5,2,17,21,52,044,42,30,33,244,43,01,,,43,03,,,33,0*65',
            '$GPGSV,5,3,17,28,,,42,22,,,37,194,52,166,40,195,83,064,42,0*61',
            '$GPGSV,5,4,17,199,,,36,42,44,159,,50,42,152,39,40,05,258,,0*6C',
            '$GPGSV,5,5,17,41,26,237,43,0*53',
            # 5 개 파싱 안됌
            '$GBGSV,4,1,14,07,89,193,38,27,63,301,43,28,,,43,30,,,42,0*7C',
            '$GBGSV,4,2,14,10,,,40,33,,,38,37,,,41,13,,,38,0*72',
            '$GBGSV,4,3,14,14,,,41,01,,,35,02,,,36,03,,,36,0*73',
            '$GBGSV,4,4,14,04,,,33,08,,,37,0*7A',
            '$GAGSV,1,1,01,01,,,40,0*70',
            #
            '$GNRMC,010711.30,A,3242.24078,N,12707.11121,E,0.100,0.00,130721,,,A,V*07']
cnt = 0
one_chunk_buf = []
sum_chuck = []


# print(total_chunk_data_one_file)
print(len(total_chunk_data_one_file))

for i in range(0, len(total_chunk_data_one_file)):
    for y in total_chunk_data_one_file[i]:
        # print("-----------------------------------")
        # print("sentence = ", y)
        for x in y:
            # print(x)
            cnt += 1
            out_sen = my_gps.update(x)
            # if out_sen:
            #     print("Timestamp [h, m, s] = ", my_gps.timestamp)
            #     print("Latitude = ", my_gps.latitude)
            #     print("Longitude = ", my_gps.longitude)
            #
            #     # print(my_gps.course)
            #     # print(my_gps.altitude)
            #     # print(my_gps.geoid_height)
            #
            #     # print(my_gps.speed)
            #     # print("time", my_gps.timestamp)
            #     # print(my_gps.date)
            #     # print(my_gps.local_offset)
            #     # print("Satellites Used = ", my_gps.satellites_used)
            #
            #     print("Satellites in use = ", my_gps.satellites_in_use)
            #     print("Satellites of view = ", my_gps.satellites_in_view)
            #     print("Fix_type = ", my_gps.fix_type)
            #
            #     print("HDOP = ", my_gps.hdop)
            #     print("VDOP = ", my_gps.vdop)
            #     print("PDOP = ", my_gps.pdop)
            #
            #     # print(my_gps.satellite_data)
            #     # print(my_gps.satellites_visible())
            #
            #     print(my_gps.parsed_sentences)
            #     print(my_gps.clean_sentences)
            #     print(my_gps.crc_fails)
            #
            #     print()
    one_chunk_buf.append(my_gps.timestamp)
    one_chunk_buf.append(my_gps.latitude)
    one_chunk_buf.append(my_gps.longitude)
    # one_chunk_buf.append(my_gps.satellites_used)
    one_chunk_buf.append(my_gps.satellites_in_use)
    one_chunk_buf.append(my_gps.satellites_in_view)
    one_chunk_buf.append(my_gps.fix_type)
    one_chunk_buf.append(my_gps.hdop)
    one_chunk_buf.append(my_gps.vdop)
    one_chunk_buf.append(my_gps.pdop)
    # print(one_chunk_buf)
    sum_chuck.append(one_chunk_buf)
    one_chunk_buf = []

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

    # print(define_new_list_from_chunck)

    # nmea_file_save.write("UTC(h, m, s) / Lat / Long / satellites used No. / Satellites of view / Fix mode(not, 2d, 3d) / HDOP / PDOP / VDOP / \n")

    for k in range(0, len(define_new_list_from_chunck)):
        nmea_file_save.write("%s " % str(define_new_list_from_chunck[k]))
    nmea_file_save.write("\n")
nmea_file_save.close()

# -------------------plot graph and save png----------------
NMEA_graph.NMEA_plot_and_save_png(filename[0][:-3] + '_filtered' + '.txt')

