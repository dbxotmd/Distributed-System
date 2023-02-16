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


def band_reservation_function(band):
    print("### available slot ###")
    band_numbers = band.get_slots_available()
    band_first_index = band_numbers[0]['id']
    print("### reserving slot ###")
    band_reserved_one = band.reserve_slot(band_first_index)
    return band_reserved_one


band_reservation = []
for i in range(2):
    band_reserving = band_reservation_function(band)
    while (True):
        if ("code" in band_reserving):
            band_reserving = band_reservation_function()
            continue
        else:
            band_reservation.append(band_reserving)
            break

print("### helding slot ###")
helding_slot = band.get_slots_held()

print("### releasing held slots")
for i in helding_slot:
    band.release_slot(i['id'])
