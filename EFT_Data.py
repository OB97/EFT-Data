import requests
import pandas
import json
import csv
from datetime import datetime, date, time, timezone


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        x = response.json()
        with open('eft-JSONdata-raw.json', 'w') as json_file:
            json.dump(x, json_file)
        return x
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def set_query():
    new_query = """
    {
        itemsByType(type: ammo) {
            id
            shortName
            types
            avg24hPrice
            link
            sellFor{
                price
                source
            }
        }
    }
    """

    result = run_query(new_query)
    print(result)

    with open('eft-data-raw.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key in result:
            writer.writerow([key])
        writer.writerow(str(datetime.now()))
    csv_file.close()
