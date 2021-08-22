import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil


def NMEA_plot_and_save_png(filtered_fliepath):
    datestrings = []
    altitude = []
    fix_mode = []
    number_of_sat_in_use = []
    sat_view = []

    hdop = []
    speed = []

    with open(filtered_fliepath, 'rb') as f:
        barr = f.readlines()
        str_nmea_data = [x.decode('utf-8') for x in barr]

    print()
    print(str_nmea_data[0])
    nmea_data_split_list = str_nmea_data[0].split(' ')
    print(nmea_data_split_list)

    # Make (X-Axis / Y-Axis data)
    for buf in str_nmea_data:
        nmea_data_split_list = buf.split(' ')
        datestrings.append(nmea_data_split_list[0] + ":"
                                    + nmea_data_split_list[1] + ":" + nmea_data_split_list[2])

        altitude.append(float(nmea_data_split_list[9]))
        fix_mode.append(float(nmea_data_split_list[10]))
        number_of_sat_in_use.append(float(nmea_data_split_list[11]))
        sat_view.append(float(nmea_data_split_list[12]))
        hdop.append(float(nmea_data_split_list[13]))
        speed.append(float(nmea_data_split_list[14]))

    # datestrings = ['1 8 12.7', '12:15:32.453000', '23:26:23.734000', '17:42:15.804000']
    dates = [dateutil.parser.parse(s) for s in datestrings]

    plt.rcParams["figure.figsize"] = (18, 12)
    plt.subplot(5, 1, 1)
    plt.plot(dates, altitude, label="GPS altitude(m)", color='red')
    plt.legend(loc='best')

    plt.subplot(5, 1, 2)
    plt.plot(dates, fix_mode, label=
    "# N(0) =  No position fix  /  E(1) = Dead reckoning fix  /  F(2) = RTK float  /  R(3) = RTK fixed \n M9 = D(0) : differential /  A(1) : autonomous", color="blue")
    plt.legend(loc='best')

    plt.subplot(5, 1, 3)
    plt.plot(dates, number_of_sat_in_use, label="Number of satellites in use", color='purple')
    # plt.plot(dates, sat_view, label="Satellites of view", color="magenta")
    plt.legend(loc='best')

    plt.subplot(5, 1, 4)
    plt.plot(dates, hdop, label="HDOP", color="salmon")
    plt.legend(loc='best')

    plt.subplot(5, 1, 5)
    # plt.title("Dilution of precision")
    plt.plot(dates, speed, label="Speed(km/h)", color="salmon")
    plt.legend(loc='best')

    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=45)

    ax=plt.gca()
    ax.set_xticks(dates)
    # ax.set_ylim([0.5, 10])

    xfmt = md.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    # plt.plot(dates,plt_data, "o-")

    plt.locator_params(axis='x', nbins=50)
    # plt.tight_layout()
    # /Users/jaeuklee/Downloads/8월19일_분석완_second_round/CLBY-1A-11-ant-0deg/0

    path_split = filtered_fliepath.split("/")

    plt.suptitle("Fitogether GPS Test : NMEA data plot\n %s  degree : %s" % (path_split[5], path_split[6]), fontsize=20)
    plt.savefig(filtered_fliepath[:-3] + '.png', dpi=300)

    plt.close()
    print("1D graph save DONE!")
    # plt.show()
