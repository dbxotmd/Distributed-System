#!/usr/bin/python3

import reservationapi
import configparser
import time

# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel  = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Your code goes here
band  = reservationapi.ReservationApi(config['band']['url'],
                                       config['band']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))


#function finding the common slot of band and hotel
def find_common(band,hotel):
    reserving  = []
    print("### band available slot ###")
    band_numbers = band.get_slots_available()
    time.sleep(1)
    print("### hotel available slot ###")
    hotel_numbers = hotel.get_slots_available()
    time.sleep(1)
    for i in hotel_numbers:
        if(len(reserving) == 2):
            break
        hotel_first_index = i
        if hotel_first_index in band_numbers:
            reserving.append(hotel_first_index)
    return reserving

#checking holding slots
print("### band holding slot ###")
b_helding_slot = band.get_slots_held()
time.sleep(1)
print("### hotel holding slot ###")
h_helding_slot = hotel.get_slots_held()
time.sleep(1)

#releasing all holding slots
print("### band releasing holding slots ###")
for i in b_helding_slot:
    band.release_slot(i['id'])
    time.sleep(1)
print("### hotel releasing holding slots ###")
for i in h_helding_slot:
    hotel.release_slot(i['id'])
    time.sleep(1)

#reserving all common slots
while(True):
    inserted =0
    reserving = find_common(band,hotel) # getting the least free common slot
    print("common slots",reserving)
    for i in reserving:
        if ("code" in i): # check if there's an exception
            if("409" in i): # slot unavailable
                reserving = find_common(band,hotel)
                print("retrying to reserve")
                print("common slots",reserving)
                continue
            elif("451" in i): # slot limit reached
                print("### holding slot ###")# see current holding slot
                b_helding_slot = band.get_slots_held()
                time.sleep(1)
                h_helding_slot = hotel.get_slots_held()
                time.sleep(1)

                print("### releasing holding slots ###") #releasing the current slot becaue of exception
                for i in b_helding_slot:
                    band.release_slot(i['id'])
                    time.sleep(1)
                for i in h_helding_slot:
                    hotel.release_slot(i['id'])
                    time.sleep(1)
                print("retrying to reserve")
                continue
        else: # checking exception when reserving the slot
            print("### reserving slots ###")
            band_reserved_one = band.reserve_slot(i['id'])
            if ("code" in band_reserved_one): # check the exception when running band reservation function
                if (band_reserved_one['code'] == '409' or band_reserved_one['code'] == '451'): # throw exception
                    print("### holding slot ###")
                    b_helding_slot = band.get_slots_held()
                    time.sleep(1)
                    h_helding_slot = hotel.get_slots_held()
                    time.sleep(1)

                    print("### releasing holding slots ###") #releasing slots
                    for i in b_helding_slot:
                        band.release_slot(i['id'])
                        time.sleep(1)
                    for i in h_helding_slot:
                        hotel.release_slot(i['id'])
                        time.sleep(1)
                    print("retrying to reserve ")
                    break
            time.sleep(1)
            hotel_reserved_one = hotel.reserve_slot(i['id'])
            if ("code" in hotel_reserved_one): # check the exception for hotel
                if (hotel_reserved_one['code'] == '409'or hotel_reserved_one['code'] == '451'):
                    print("### holding slot ###")
                    b_helding_slot = band.get_slots_held()
                    time.sleep(1)
                    h_helding_slot = hotel.get_slots_held()
                    time.sleep(1)

                    print("### releasing holding slots ###")
                    for i in b_helding_slot:
                        band.release_slot(i['id'])
                        time.sleep(1)
                    for i in h_helding_slot:
                        hotel.release_slot(i['id'])
                        time.sleep(1)
                    print("retrying to reserve ")
                    break
            time.sleep(1)
            inserted += 1
    if(inserted ==2 ): # checking if two values really inserted
        break


#check if common slots reserved
print("### band holding slots ###")
b_helding_slot = band.get_slots_held()
time.sleep(1)
print("### hotel holding slots ###")
h_helding_slot = hotel.get_slots_held()
time.sleep(1)

#check the length of each holding slots
#if not reached to two, then run the function again to reserve two common free slots
if (len(b_helding_slot) != 2 or len(h_helding_slot) !=2):
    print("### holding slot ###")
    b_helding_slot = band.get_slots_held()
    time.sleep(1)
    h_helding_slot = hotel.get_slots_held()
    time.sleep(1)

    print("### releasing holding slots ###")
    for i in b_helding_slot:
        band.release_slot(i['id'])
        time.sleep(1)
    for i in h_helding_slot:
        hotel.release_slot(i['id'])
        time.sleep(1)

    while(True):
        inserted =0
        reserving = find_common(band,hotel)
        print("common slots",reserving)
        for i in reserving:
            if ("code" in i): # check if there's an exception
                if("409" in i): # slot unavailable
                    reserving = find_common(band,hotel)
                    print("common slots",reserving)
                    continue
                elif("451" in i): # slot limit reached
                    print("### holding slot ###")
                    b_helding_slot = band.get_slots_held()
                    time.sleep(1)
                    h_helding_slot = hotel.get_slots_held()
                    time.sleep(1)

                    print("### releasing holding slots ###")
                    for i in b_helding_slot:
                        band.release_slot(i['id'])
                        time.sleep(1)
                    for i in h_helding_slot:
                        hotel.release_slot(i['id'])
                        time.sleep(1)
                    reserving = find_common(band,hotel)
                    continue
            else: # checking exception when reserving the slot
                print("### reserving slots ###")
                band_reserved_one = band.reserve_slot(i['id'])
                if ("code" in band_reserved_one):
                    if (band_reserved_one['code'] == '409'or band_reserved_one['code'] == '451'):
                        print("### holding slot ###")
                        b_helding_slot = band.get_slots_held()
                        time.sleep(1)
                        h_helding_slot = hotel.get_slots_held()
                        time.sleep(1)

                        print("### releasing holding slots ###")
                        for i in b_helding_slot:
                            band.release_slot(i['id'])
                            time.sleep(1)
                        for i in h_helding_slot:
                            hotel.release_slot(i['id'])
                            time.sleep(1)
                        reserving = find_common(band,hotel)
                        print("common slots",reserving)
                        print("retrying to reserve ")
                        break
                time.sleep(1)
                hotel_reserved_one = hotel.reserve_slot(i['id'])
                if ("code" in hotel_reserved_one):
                    if (hotel_reserved_one['code'] == '409' or hotel_reserved_one['code'] == '451'):
                        print("### holding slot ###")
                        b_helding_slot = band.get_slots_held()
                        time.sleep(1)
                        h_helding_slot = hotel.get_slots_held()
                        time.sleep(1)

                        print("### releasing holding slots ###")
                        for i in b_helding_slot:
                            band.release_slot(i['id'])
                            time.sleep(1)
                        for i in h_helding_slot:
                            hotel.release_slot(i['id'])
                            time.sleep(1)
                        reserving = find_common(band,hotel)
                        print("common slots",reserving)
                        print("retrying to reserve ")
                        break
                time.sleep(1)
                inserted +=1
        if inserted == 2:
            break

#checking one more time for holding
print("### holding slot ###")
b_helding_slot = band.get_slots_held()
time.sleep(1)
h_helding_slot = hotel.get_slots_held()
time.sleep(1)


#recheck if there's optimal value
print("### rechecking optimal value ###")
reserving = find_common(band,hotel)
print("common slots",reserving)
if(reserving[0]['id']< b_helding_slot[1]['id']): # if new free spot is smaller than second value of holding
    if(reserving[0]['id']< b_helding_slot[0]['id']): # if new free spot is smaller than the smallest value of holding
        band.release_slot(b_helding_slot[1]['id'])
        time.sleep(1)
        hotel.release_slot(h_helding_slot[1]['id'])
        time.sleep(1)
        while(True):
            inserted = 0
            if ("code" in i):
                if("409" in i):
                    reserving = find_common(band,hotel)
                    continue
                elif("451" in i):
                    print("### holding slot ###")
                    b_helding_slot = band.get_slots_held()
                    time.sleep(1)
                    h_helding_slot = hotel.get_slots_held()
                    time.sleep(1)

                    print("### releasing holding slots ###")
                    for i in b_helding_slot:
                        band.release_slot(i['id'])
                        time.sleep(1)
                    for i in h_helding_slot:
                        hotel.release_slot(i['id'])
                        time.sleep(1)
                    reserving = find_common(band,hotel)
                    continue
            else: # checking exception when reserving the slot
                print("### reserving slots ###")
                band_reserved_one = band.reserve_slot(reserving[0]['id'])
                if ("code" in band_reserved_one):
                    if (band_reserved_one['code'] == '409'or band_reserved_one['code'] == '451'):
                        print("### holding slot ###")
                        b_helding_slot = band.get_slots_held()
                        time.sleep(1)
                        h_helding_slot = hotel.get_slots_held()
                        time.sleep(1)

                        print("### releasing holding slots ###")
                        for i in b_helding_slot:
                            band.release_slot(i['id'])
                            time.sleep(1)
                        for i in h_helding_slot:
                            hotel.release_slot(i['id'])
                            time.sleep(1)
                        print("retrying to reserve ")
                        reserving = find_common(band,hotel)
                        print("common slots",reserving)
                        continue
                time.sleep(1)
                hotel_reserved_one = hotel.reserve_slot(reserving[0]['id'])
                if ("code" in hotel_reserved_one):
                    if (hotel_reserved_one['code'] == '409' or hotel_reserved_one['code'] == '451'):
                        print("### holding slot ###")
                        b_helding_slot = band.get_slots_held()
                        time.sleep(1)
                        h_helding_slot = hotel.get_slots_held()
                        time.sleep(1)

                        print("### releasing holding slots ###")
                        for i in b_helding_slot:
                            band.release_slot(i['id'])
                            time.sleep(1)
                        for i in h_helding_slot:
                            hotel.release_slot(i['id'])
                            time.sleep(1)
                        print("retrying to reserve ")
                        reserving = find_common(band,hotel)
                        print("common slots",reserving)
                        continue
                time.sleep(1)
                inserted +=1
            if inserted ==2:
                break
    else:
        band.release_slot(b_helding_slot[1]['id'])
        time.sleep(1)
        hotel.release_slot(h_helding_slot[1]['id'])
        time.sleep(1)
        while(True):
            inserted =0
            if ("code" in i):
                if("409" in i):
                    reserving = find_common(band,hotel)
                    continue
                elif("451" in i):
                    print("### holding slot ###")
                    b_helding_slot = band.get_slots_held()
                    time.sleep(1)
                    h_helding_slot = hotel.get_slots_held()
                    time.sleep(1)

                    print("### releasing holding slots ###")
                    for i in b_helding_slot:
                        band.release_slot(i['id'])
                        time.sleep(1)
                    for i in h_helding_slot:
                        hotel.release_slot(i['id'])
                        time.sleep(1)
                    reserving = find_common(band,hotel)
                    continue
            else: # checking exception when reserving the slot
                print("### reserving slots ###")
                band_reserved_one = band.reserve_slot(reserving[0]['id'])
                if ("code" in band_reserved_one):
                    if (band_reserved_one['code'] == '409'or band_reserved_one['code'] == '451'):

                        print("### holding slot ###")
                        b_helding_slot = band.get_slots_held()
                        time.sleep(1)
                        h_helding_slot = hotel.get_slots_held()
                        time.sleep(1)

                        print("### releasing holding slots ###")
                        for i in b_helding_slot:
                            band.release_slot(i['id'])
                            time.sleep(1)
                        for i in h_helding_slot:
                            hotel.release_slot(i['id'])
                            time.sleep(1)
                        print("### retry reserving ###")
                        reserving = find_common(band,hotel)
                        print("common slots",reserving)
                        continue
                time.sleep(1)
                hotel_reserved_one = hotel.reserve_slot(reserving[0]['id'])
                if ("code" in hotel_reserved_one):
                    if (hotel_reserved_one['code'] == '409' or hotel_reserved_one['code'] == '451'):
                        print("### holding slot ###")
                        b_helding_slot = band.get_slots_held()
                        time.sleep(1)
                        h_helding_slot = hotel.get_slots_held()
                        time.sleep(1)

                        print("### releasing holding slots ###")
                        for i in b_helding_slot:
                            band.release_slot(i['id'])
                            time.sleep(1)
                        for i in h_helding_slot:
                            hotel.release_slot(i['id'])
                            time.sleep(1)
                        print("### retry reserving ###")
                        reserving = find_common(band,hotel)
                        print("common slots",reserving)
                        continue
                time.sleep(1)
                inserted +=1
            if inserted ==2:
                break

#keep checking holding
print("### holding slot ###")
b_helding_slot = band.get_slots_held()
time.sleep(1)
h_helding_slot = hotel.get_slots_held()
time.sleep(1)

#relaseing the largest value from holding slot
print("### releasing holding slots ###")
if (b_helding_slot[0]['id']) > (b_helding_slot[1]['id']):
    band.release_slot(b_helding_slot[0]['id'])
    time.sleep(1)
    hotel.release_slot(h_helding_slot[0]['id'])
    time.sleep(1)
else:
    band.release_slot(b_helding_slot[1]['id'])
    time.sleep(1)
    hotel.release_slot(h_helding_slot[1]['id'])
    time.sleep(1)

#printing out the final one least slot
print("### Final band holding slots ###")
b_helding_slot = band.get_slots_held()
time.sleep(1)
print("### Final hotel holding slots ###")
h_helding_slot = hotel.get_slots_held()
time.sleep(1)
print("session success")
