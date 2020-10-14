
from lxml import html
from datetime import date, timedelta
import numpy as np
import pandas as pd

import SlackLogger
import ArgumentReader
import Statics
import FeideLogin

## Read arguments from script initialization
username, password = ArgumentReader.read_user_name_password()
init, reserve, store_found = ArgumentReader.red_state_args()
duration, min_size, reserve_in_n_days, start = ArgumentReader.read_reservation_args()

if reserve and not init:
    reservation_description = read_reservation_description()

slack_log, slack_token, slack_url, slack_channel = read_slack_args()

slack_logger = SlackLogger(slack_token, slack_channel, slack_url)


login_session = FeideLogin.login_to_feide(USERNAME, PASSWORD, MAIN_URL, ORG)
login_session_js_confirmed = FeideLogin.confirm_js(login_session)



date_to_reserve = date.today()+timedelta(days=reserve_in_n_days)
date_to_reserve_type1 = date_to_reserve.strftime("%d.%m.%Y")
date_to_reserve_type2 = date_to_reserve.strftime("%Y-%m-%d")
day_to_reserve = date_to_reserve.strftime('%a').upper()

def find_areas(request):
    areas = html.fromstring(request.content).xpath('//select[contains(@name,"area")]/option/text()')
    area_ids = html.fromstring(request.content).xpath('//select[contains(@name,"area")]/option/@value')
    area_df = pd.DataFrame(np.array([areas, area_ids]).T, columns = ["area", "area_id"])
    area_df["rank"] = 0
    area_df.to_csv(AREAS_PATH, index=False)

def find_buildings(request):
    buildings = html.fromstring(request.content).xpath('//select[contains(@name,"building")]/option/text()')
    buildings_ids = html.fromstring(request.content).xpath('//select[contains(@name,"building")]/option/@value')
    buildings_df = pd.DataFrame(np.array([buildings, buildings_ids]).T, columns = ["building", "building_id"])
    buildings_df["rank"] = 0
    buildings_df.to_csv(BUILDINGS_PATH, index=False)

def find_roomtypes(request):
    roomtypes = html.fromstring(request.content).xpath('//select[contains(@name,"roomtype")]/option/text()')
    roomtypes_ids = html.fromstring(request.content).xpath('//select[contains(@name,"roomtype")]/option/@value')
    roomtypes_df = pd.DataFrame(np.array([roomtypes, roomtypes_ids]).T, columns = ["roomtype", "roomtype_id"])
    roomtypes_df["rank"] = 0
    roomtypes_df.to_csv(ROOMTYPES_PATH, index=False)

def max_room_rank(room_id, found_rooms):
    room_ranks = found_rooms.loc[found_rooms['room_id'] == room_id]['rank'].values
    if len(room_ranks) == 0:
        return -1

    return max(room_ranks)


def find_available_rooms(area, roomtype, building, store_found = False, prioritize = True):
    room_filter_data = {
      'start': start,
      'duration': duration,
      'preset_date': date_to_reserve_type1,
      'area': area,
      'building': building,
      'roomtype': roomtype,
      'size': min_size,
      'new_equipment': '',
      'preformsubmit': '1'
    }

    request = session.post(MAIN_URL, data=room_filter_data)
    print("Find available rooms request: " + str(request))

    available_room_ids = html.fromstring(request.content).xpath('//form//table[contains(@class,"possible-rooms-table")]/tbody/tr/td/@title')
    available_room_ids = available_room_ids[0::3]

    available_room_names = html.fromstring(request.content).xpath('//form//table[contains(@class,"possible-rooms-table")]/tbody/tr/td/a/text()')
    available_room_names = [room.strip() for room in available_room_names]

    if len(available_room_ids) == 0:
        return np.array([])

    new_rooms = []
    if store_found:
        path_exists = path.exists(ROOM_PRIORITY_PATH)
        if path_exists:
            found_rooms = pd.read_csv(ROOM_PRIORITY_PATH, encoding='utf8')

        for room in np.c_[available_room_names, available_room_ids]:
            if not path_exists or not room[0] in found_rooms['room_name'].values:
                new_rooms.append([room[0],room[1], 0])
        new_rooms = pd.DataFrame(new_rooms,columns=['room_name','room_id','rank'])
        with open(ROOM_PRIORITY_PATH, 'a+') as f:
            new_rooms.to_csv(f, header=(not path_exists),index = False, encoding='utf8')

    if prioritize:
        path_exists = path.exists(ROOM_PRIORITY_PATH)
        if path_exists:
            found_rooms = pd.read_csv(ROOM_PRIORITY_PATH, encoding='utf8')
        else:
            return np.array(available_room_ids)

        available_room_ids_ordered = []

        for room_id in available_room_ids:
            max_room_rank_value =  max_room_rank(room_id, found_rooms)
            if max_room_rank_value < 0:
                continue
            available_room_ids_ordered += [[room_id, max_room_rank_value]]
        available_room_ids_ordered = sorted(available_room_ids_ordered, key=lambda row: row[1], reverse = True)

        return np.array(available_room_ids_ordered)[:,0]
    return np.array(available_room_ids)



# Start reservation of room
def reserve_room(room, area, roomtype, building):
    reservation_data = {
      'start': start,
      'size': min_size,
      'roomtype': roomtype,
      'duration': duration,
      'area': area,
      'building': building,
      'preset_date': date_to_reserve_type1,
      'exam': '',
      'single_place': '',
      'room[]': room,
      'submitall': 'Bestill \u21E8'
    }

    reserve_request = session.post(MAIN_URL, data=reservation_data)
    print("reserve request: " + str(reserve_request))

    # Confrim reservation
    csrftoken = html.fromstring(reserve_request.content).xpath('//form//input[contains(@name,"csrftoken")]/@value')[0]
    reservation_confirmation_data = {
      'name': reservation_description,
      'notes': '',
      'confirmed': 'true',
      'confirm': '',
      'start': start,
      'size': min_size,
      'roomtype': roomtype,
      'duration': duration,
      'area': area,
      'room[]': room,
      'building': building,
      'preset_day': day_to_reserve,
      'preset_date': date_to_reserve_type2,
      'exam': '',
      'single_place': '',
      'dates[]': date_to_reserve_type2,
      'csrftoken': csrftoken
    }

    reserve_confirmation_request = session.post(MAIN_URL, data=reservation_confirmation_data)
    print("reserve_confirmation_request: " + str(reserve_confirmation_request))
    return reserve_confirmation_request

def find_room_to_reserve():
	if len(areas["area_id"].values)==0:
		print("Need to set area ranks")
	if len(roomtypes["roomtype_id"].values) == 0:
		print("Need to set roomtype ranks")
	if len(buildings["building_id"].values) == 0:
		print("Need to set building ranks")

	for area in areas["area_id"].values:
		for roomtype in roomtypes["roomtype_id"].values:
			for building in buildings["building_id"].values:
				print(area, roomtype, building)
				rooms = find_available_rooms(area, roomtype, building, store_found = store_found, prioritize = True)
				if len(rooms)>0 and reserve:
					return (area, roomtype, building, rooms[0])
	return "", "", "", ""



if not path.exists(BUILDINGS_PATH):
    find_buildings(nojs_auth_confirmation_request)
if not path.exists(ROOMTYPES_PATH):
    find_roomtypes(nojs_auth_confirmation_request)
if not path.exists(AREAS_PATH):
    find_areas(nojs_auth_confirmation_request)

buildings = pd.read_csv(BUILDINGS_PATH)
buildings = buildings.loc[buildings["rank"] != 0]
buildings = buildings.sort_values(by=["rank"], ascending = False)
buildings["building_id"] = buildings["building_id"].astype(int)

areas = pd.read_csv(AREAS_PATH)
areas = areas.loc[areas["rank"] != 0]
areas = areas.sort_values(by=["rank"], ascending = False)
areas["area_id"] = areas["area_id"].astype(int)

roomtypes = pd.read_csv(ROOMTYPES_PATH)
roomtypes = roomtypes.loc[roomtypes["rank"] != 0]
roomtypes = roomtypes.sort_values(by=["rank"], ascending = False)




if not init:
	area, roomtype, building, room = find_room_to_reserve()
	if reserve and len(room)>0:
		reserve_request = reserve_room(room, area, roomtype, building)
		if slack_log:
            message = ''.join(html.fromstring(request.content).xpath('//h3/../section/div/span//text()')) + ":mazemap: :tornadotor: :powerstonk:"
            slack_logger.log_to_slack(message)
