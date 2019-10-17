# Automatic room reserver
Reserves room by user-selected criterias following a prioritized list. You will never need to wake up early to reserve a room again! 

## Setup:
1. Make sure you have python setup with the correct libraries.
1. Create env variable "FUSER" with feide-username
2.  Create env variable "FPASSWORD" with feide-password
3.  Run `python3 roomreserver.py init=True`
4. In the newly created `buildings.csv` rank what buildings you want to choose from. HIGHER IS BETTER.  0 will be ignored. 
5. In the newly created `roomtypes.csv` rank what buildings you want to choose from. HIGHER IS BETTER.  0 will be ignored. 
6. In the newly created `areas.csv` rank what buildings you want to choose from. HIGHER IS BETTER.  0 will be ignored. 
7. If you want to rank rooms before reserving run `python3 roomreserver.py start="HH:MM" duration="HH:MM" min_size="XX" reserve=F` and edit ranks in the newly created `room_priority.csv`. Rooms with negative rank will be ignored. 

## How to run:
`python3 roomreserver.py start="HH:MM" desc="Reservation description HERE" duration="HH:MM" min_size="XX"`
By default:
`duration="02:00" min_size="10"`

To run without reserving rooms and only search for new rooms at selected filters:
`reserve=False`

If you want to run without saving newly found rooms add:
`store=False`

Arguments: 

| Parameter  | Description                                                                               | Default value | Format             |
|------------|-------------------------------------------------------------------------------------------|---------------|--------------------|
| init       | Is script in initialize state. E.g. needs to search rooms and create necessary .csv files | False         | T/F/True/False     |
| reserve    | If not init, should post reserve requests?                                                | True          | T/F/True/False     |
| store      | Store new rooms found in .csv?  (Will make script somewhat slower)                        | True          | T/F/True/False     |
| duration   | Length of reservation                                                                     | 02:00         | HR:MM              |
| min_size   | Minimum size of room (number of people)                                                   | 10            | XX                 |
| reserve_in | Days into the future for when to reserve                                                  | 14            | XX                 |
| start      | Start time of reservation (Not needed when init)                                          |               | HR:MM              |
| desc       | Description of reservation (Not needed when init)                                         |               | "YOUR DESCRIPTION" |


## Requirements
Runs python3 using the following libraries:

- requests

- lxml

- numpy

- pandas
