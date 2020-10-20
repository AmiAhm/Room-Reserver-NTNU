from lxml import html
import pandas as pd

from Statics import *

def find_areas(page):
    areas = html.fromstring(page.content).xpath('//select[contains(@name,"area")]/option/text()')
    area_ids = html.fromstring(page.content).xpath('//select[contains(@name,"area")]/option/@value')
    area_df = pd.DataFrame(np.array([areas, area_ids]).T, columns = ["area", "area_id"])
    area_df["rank"] = 0
    area_df.to_csv(AREAS_PATH, index=False)

def find_buildings(page):
    buildings = html.fromstring(page.content).xpath('//select[contains(@name,"building")]/option/text()')
    buildings_ids = html.fromstring(page.content).xpath('//select[contains(@name,"building")]/option/@value')
    buildings_df = pd.DataFrame(np.array([buildings, buildings_ids]).T, columns = ["building", "building_id"])
    buildings_df["rank"] = 0
    buildings_df.to_csv(BUILDINGS_PATH, index=False)

def find_roomtypes(page):
    roomtypes = html.fromstring(page.content).xpath('//select[contains(@name,"roomtype")]/option/text()')
    roomtypes_ids = html.fromstring(page.content).xpath('//select[contains(@name,"roomtype")]/option/@value')
    roomtypes_df = pd.DataFrame(np.array([roomtypes, roomtypes_ids]).T, columns = ["roomtype", "roomtype_id"])
    roomtypes_df["rank"] = 0
    roomtypes_df.to_csv(ROOMTYPES_PATH, index=False)
