from bs4 import BeautifulSoup as bs
import requests


def get_flight_list():
    target_url = "https://clj-ws.visionairfids.com/static-flights?type=arrival"

    flights = []
    req = requests.get(target_url)

    if req.status_code == 200:
        soup = bs(req.content, "lxml")
        flights_as_elems = soup.find_all("tr")
        del flights_as_elems[0]

        for fl in flights_as_elems:
            fl_no = fl.contents[0].string
            origin = fl.contents[1].string
            time = fl.contents[2].string
            status = fl.contents[3].string
            flights.append((fl_no, origin, time, status))
        return flights
    else:
        return None


def get_status_time(flight: tuple) -> str:
    if flight[3] is None:
        return flight[2]
    elif flight[3].find("EST") != -1:
        return flight[3][len(flight[3]) - 5:]
    else:
        return flight[2]


def get_time(elem):
    return elem[4]


def get_next_flight() -> dict:
    flist = get_flight_list()
    if flist is not None:
        i = 0
        while flist[i][3] is not None:
            if flist[i][3].find("LANDED") != -1:
                i += 1
            else:
                break
        arriv_flights = []
        j = i
        while j < len(flist) - 1 and flist[j+1][2] > flist[j][2]:
            if flist[j][3] is None:
                flist[j] += get_status_time(flist[j]),
                arriv_flights.append(flist[j])
            else:
                if flist[j][3].find("LANDED") == -1 and flist[j][3].find("DELAYED") == -1:
                    flist[j] += get_status_time(flist[j]),
                    arriv_flights.append(flist[j])
            j += 1
        if i < len(flist) and flist[i+1][2] < flist[i][2]:
            if flist[i][3] is None:
                flist[i] += get_status_time(flist[i]),
                arriv_flights.append(flist[i])
            else:
                if flist[j][3].find("LANDED") == -1 and flist[j][3].find("DELAYED") == -1:
                    flist[j] += get_status_time(flist[j]),
                    arriv_flights.append(flist[j])
        arriv_flights.sort(key=get_time)

        flight = {
            "fl_no": str(arriv_flights[0][0].string),
            "origin": str(arriv_flights[0][1].string),
            "time": str(arriv_flights[0][2].string),
        }
        if arriv_flights[0][3] is None:
            flight["status"] = "ETA: " + flight["time"]
        else:
            flight["status"] = str(arriv_flights[0][3].string)
        return flight
    return None

