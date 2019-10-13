# Automatic room reserver  NTNU
Reserves room by criterias in 14 days into the future
## Requirements
Runs python3 using the following libraries:

- requests

- lxml

- numpy

- pandas
## Setup:
1. Make sure you have python setup with the correct libraries.
1. Create env variable "FUSER" with feide-username
2.  Create env variable "FPASSWORD" with feide-password
3.  Run `python3 roomreserver.py init=True`
4. In the newly created `buildings.csv` rank what buildings you want to choose from. HIGHER IS BETTER.  0 will be ignored. 
5. In the newly created `roomtypes.csv` rank what buildings you want to choose from. HIGHER IS BETTER.  0 will be ignored. 
6. In the newly created `areas.csv` rank what buildings you want to choose from. HIGHER IS BETTER.  0 will be ignored. 
7. If you want to rank rooms before reserving run `python3 roomreserver.py start="HH:MM" duration="HH:MM" min_size="XX" reserve=F` and edit ranks in the newly created `room_priority.csv`
## How to run:
`python3 roomreserver.py start="HH:MM" desc="Reservation description HERE" duration="HH:MM" min_size="XX"`
By default:
`duration="02:00" min_size="10"`

To run without reserving rooms and only search for new rooms at selected filters:
`reserve=False`

If you want to run without saving newly found rooms add:
`store=False`