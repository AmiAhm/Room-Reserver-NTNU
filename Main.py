
from lxml import html
from datetime import date, timedelta
import numpy as np
import pandas as pd

from SlackLogger import SlackLogger
from Statics import *

import ArgumentReader
import FeideLogin
from RoomInfo import find_areas, find_buildings, find_roomtypes
from RoomReserver import find_room_to_reserve, reserve_room, get_room_info

## Read arguments from script initialization
username, password = ArgumentReader.read_feide_user()
init, reserve, store_found = ArgumentReader.red_state_args()

if not init:
    duration, min_size, reserve_in_n_days, start = ArgumentReader.read_reservation_args()
else:
    duration = '00:30'
    reserve_in_n_days = 14
    start = '17:00'

if reserve and not init:
    reservation_description = ArgumentReader.read_reservation_description()

slack_log, slack_token, slack_url, slack_channel = ArgumentReader.read_slack_args()

if slack_log:
    slack_logger = SlackLogger(slack_token, slack_channel, slack_url)


auth_request, login_session = FeideLogin.login_to_feide(username, password, MAIN_URL, ORG)
login_session_js_confirmed = FeideLogin.confirm_js(auth_request, login_session)



date_to_reserve = date.today()+timedelta(days=reserve_in_n_days)
date_to_reserve_type1 = date_to_reserve.strftime("%d.%m.%Y")
date_to_reserve_type2 = date_to_reserve.strftime("%Y-%m-%d")
day_to_reserve = date_to_reserve.strftime('%a').upper()


buildings, areas, roomtypes = get_room_info()


if not init:
    area, roomtype, building, room = find_room_to_reserve(login_session, store_found, areas, roomtypes, buildings)
    if reserve and len(room)>0:
        reserve_request = reserve_room(login_session, room, area, roomtype, building)
        if slack_log:
            message = ''.join(html.fromstring(request.content).xpath('//h3/../section/div/span//text()')) + ":mazemap: :tornadotor: :powerstonk:"
            slack_logger.log_to_slack(message)
