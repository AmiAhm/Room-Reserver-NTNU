import sys
from os import path, environ

args = {}
for pair in sys.argv[1:]:
    args.__setitem__(*((pair.split('=', 1) + [''])[:2]))

def read_feide_user():
    if 'FUSER' not in environ.keys():
        raise Exception("No feide username found. Create env var: FUSER")

    if 'FPASSWORD' not in environ.keys():
        raise Exception("No feide username found. Create env var: FPASSWORD")

    username = environ['FUSER'] # Feide username
    password = environ['FPASSWORD'] # Feide PASSWORD


    return username, password

def red_state_args():
    if 'init' in args.keys():
        init = args['init'].lower() in ("yes", "true", "t", "1")
    else:
        init = False

    if 'reserve' in args.keys() and args['reserve'].lower() in ("no", "false", "f", "0"):
        reserve = False
    else:
        reserve = True


    if 'store' in args.keys()and args['store'].lower() in ("no", "false", "f", "0"):
        store_found = False
    else:
        store_found = True

    return init, reserve, store_found

def read_reservation_args():
    if 'duration' not in args.keys():
        duration='02:00'
    else:
        duration = args['duration'] # Reservation time in hr, max 4hr

    if 'min_size' not in args.keys():
        min_size='10'
    else:
        min_size = args['min_size']

    if 'reserve_in' not in args.keys():
        reserve_in_n_days = 14
    else:
        reserve_in_n_days = args['reserve_in']

    if 'start' not in args.keys():
        raise Exception("Need start time. Pass start='HH:MM'")
    start = args['start']

    return duration, min_size, reserve_in_n_days, start


def read_reservation_description():
    if 'desc' not in args.keys() and reserve:
        raise Exception("Need description. Pass description='Your room reservation description here'")

    reservation_description = args['desc'] # Title of reservation

    return reservation_description


def read_slack_args():
    if 'slack_log' in args.keys():
        slack_log = args['slack_log'].lower() in ("yes", "true", "t", "1")
    else:
        slack_log = False

    slack_token = None
    slack_url = None
    slack_channel = None

    if slack_log:
        if 'SLACK_TOKEN' not in environ.keys():
            raise Exception("No feide SLACK TOKEN found. Create env var: SLACK_TOKEN")

        if 'SLACK_CHANNEL' not in environ.keys():
            raise Exception("No SLACK CHANNEL found. Create env var: SLACK_CHANNEL")
        if 'SLACK_URL ' not in environ.keys():
            raise Exception("No SLACK URL found. Create env var: SLACK_URL")


        slack_token = environ['SLACK_TOKEN']
        slack_url = environ['SLACK_URL']
        slack_channel = environ['SLACK_CHANNEL']

    return slack_log, slack_token, slack_url, slack_channel
