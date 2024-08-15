import datetime as dt
import math as m

from .orbit import Orbit

def to_radians(degrees) -> float:
    return float(degrees) * (m.pi / 180)


def mean_motion_to_radians(mean_motion) -> float:
    return mean_motion * 2 * m.pi / 86400


def parse_data(data: list, mu):
    """Parse data into data structures

    We should use an array of dicts (to start)

    TODO: I'd like to add name parsing to this. So it'd be a 3 line data file instead of 2 lines that we'd be parsing
    """
    out = []
    for i in range(len(data) // 2):
        if data[i * 2][0] != "1":
            print("Wrong TLE format at line " + str(i * 2) + ". Lines ignored.")
            continue

        # Reference wiki for the TLE format
        # https://en.wikipedia.org/wiki/Two-line_element_set#Title_line_(optional)

        idx = i * 2
        line_num = data[idx][0]
        epoch_year = data[idx][18:20]
        epoch_day = data[idx][20:23]

        # second row
        idx = i * 2 + 1
        name = data[idx][2:7]
        e = float(f".{data[idx][26:34]}")

        # To calculate the semi-major axis, we need to use the mean motion (n)
        n = mean_motion_to_radians(float(data[idx][52:63]))
        a = (mu / (n ** 2)) ** (1. / 3)

        inclination = float(data[idx][9:17]) * m.pi / 180
        RANN = to_radians(data[idx][17:26])  # right ascention of ascending node
        omega = to_radians(data[idx][34:43])  # argument of perigee

        # TODO: clean this up. It's capturing the time data in the first line of TLE data
        # if int(data[i * 2][18:20]) > int(dt.date.today().year % 100):
        #     orb = {
        #         "t":
        #            dt.datetime.strptime("19" + data[i*2][18:20] + " " + data[i*2][20:23] + " " + str(int(24 * float(data[i * 2][23:33])//1))+" "+str(int(((24*float(data[i*2][23:33])%1)*60)//1))+" "+str(int((((24*float(data[i*2][23:33])%1)*60)%1)//1)), "%Y %j %H %M %S")
        #     }
        # else:
        #     orb = {
        #         "t":
        #         dt.datetime.strptime("20"+data[i*2][18:20]+" "+data[i*2][20:23]+" "+str(int(24*float(data[i*2][23:33])//1))+" "+str(int(((24*float(data[i*2][23:33])%1)*60)//1))+" "+str(int((((24*float(data[i*2][23:33])%1)*60)%1)//1)), "%Y %j %H %M %S")
        #     }

        out.append(Orbit(name=name, e=e, a=a, i=inclination, RANN=RANN, omega=omega))
    return out
