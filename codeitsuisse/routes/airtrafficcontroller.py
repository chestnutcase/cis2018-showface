import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def air_traffic_controller(jsoninput):
    flights = jsoninput["Flights"]
    reserve_time = int(jsoninput["Static"]["ReserveTime"]) // 60

    #print(flights)
    #print(reserve_time)

    runway_exist = False
    runways = ["A"]

    if "Runways" in jsoninput["Static"]:
        runway_exist = True
        runways = jsoninput["Static"]["Runways"]

    #print(runways)

    for flight in flights:
        flight["str_time"] = flight["Time"]
        flight["int_time"] = 60 * int(flight["Time"][:2]) + int(flight["Time"][2:])
        del flight["Time"]

    #print(flights)

    for flight in flights:
        flight["d"] = "0"
        if "Distressed" in flight:
            if flight["Distressed"] == "true":
                flight["d"] = "1"

    #print(flights)

    for flight in flights:
        flight["superstring"] = flight["str_time"] + flight["PlaneId"] + flight["d"]

    #print(flights)

    distressed_flights = []

    for flight in flights:
        if flight["d"] == '1':
            distressed_flights.append(flight)

    #print(distressed_flights)

    distressed_flights = sorted(distressed_flights, key=lambda k: k['superstring'])
    #print(distressed_flights)


    normal_flights = []

    for flight in flights:
        if flight["d"] == '0':
            normal_flights.append(flight)

    #print(normal_flights)

    flights = sorted(normal_flights, key=lambda k: k['superstring'])
    #print(flights)

    runways_avail = [flights[0]["int_time"]] * len(runways)
    c = 0  # distressed_flight_counter


    for j,flight in enumerate(flights):
        # priority for distressed flights

        reserve = False

        if c < len(distressed_flights):
            loop_lock = True

            while loop_lock:  # in case there are consecutive distressed flights
                #print(distressed_flights[c]["int_time"], min(runways_avail), j)
                if distressed_flights[c]["int_time"] - reserve_time < min(runways_avail):

                    i = runways_avail.index(min(runways_avail))
                    distressed_flights[c]["Runway"] = runways[i]
                    distressed_flights[c]["arr_time"] = distressed_flights[c]["int_time"]
                    # distressed_flights[c]["insert_location"] = j  # insert location does not matter

                    # reserve the time
                    runways_avail[i] = distressed_flights[c]["int_time"] + reserve_time

                    c += 1
                    if c == len(distressed_flights):
                        loop_lock = False
                else:
                    loop_lock = False

        # if there is a runway available at arrival time
        for i,runway_avail in enumerate(runways_avail):
            if flight["int_time"] > runway_avail:
                flight["Runway"] = runways[i]
                flight["arr_time"] = flight["int_time"]

                # reserve the time
                runways_avail[i] = flight["int_time"] + reserve_time

                #print(runways_avail)
                break
        # there is no runway available at arrival time
        else:
            runway_avail = min(runways_avail)
            i = runways_avail.index(min(runways_avail))
            flight["Runway"] = runways[i]
            flight["arr_time"] = runway_avail

            # reserve the time
            runways_avail[i] = runway_avail + reserve_time
            #print(runways_avail)


        if j == len(flights)-1 and c < len(distressed_flights):  # in case it ends with distressed flights
            loop_lock = True
            while loop_lock:  # in case there are consecutive distressed flights
                #print("===")
                #print(distressed_flights[c]["int_time"], min(runways_avail), j)
    #             if distressed_flights[c]["int_time"] - reserve_time < min(runways_avail):

                i = runways_avail.index(min(runways_avail))
                distressed_flights[c]["Runway"] = runways[i]
                distressed_flights[c]["arr_time"] = distressed_flights[c]["int_time"]

                #print(distressed_flights[c]["int_time"])
                # distressed_flights[c]["insert_location"] = j  # insert location does not matter

                # reserve the time
                runways_avail[i] = distressed_flights[c]["int_time"] + reserve_time

                c += 1
                if c == len(distressed_flights):
                    loop_lock = False
    #             else:
    #                 loop_lock = False


    for distressed_flight in distressed_flights:
        del distressed_flight["Distressed"]
        flights.insert(0, distressed_flight)

    flights = sorted(flights, key=lambda k: k['arr_time'])


    for flight in flights:
        flight['Time'] = format(flight["arr_time"]//60,'02') + format(flight["arr_time"]%60,'02')

    for flight in flights:
        del flight['arr_time']
        del flight['str_time']
        del flight['int_time']
        del flight['superstring']
        del flight['d']

    if not runway_exist:
        for flight in flights:
            del flight['Runway']

    return {"Flights":flights}


@app.route('/airtrafficcontroller', methods=['POST'])
def evaluate_air():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data));
    output = air_traffic_controller(data);
    return jsonify(output);
