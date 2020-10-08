import json
from pymongo import MongoClient

import helpers
from jobs import FenixJob

def load_config():
    config = {}
    with open('./Config/config.json') as c:
        config = json.load(c)

    return config


def extract_target_config(target, config):
    if 'sites' not in config:
        return None

    for site in config['sites']:
        if site['target'] == target:
            return site

    return None


def extract_db_config(config):
    if 'db' not in config:
        return None 

    return config['db']


def job_factory(config):
    if config['target'] == 'fenix':
        return FenixJob(config)


def write_to_db(client, schedules):
    db = client['Terminal']
    schedulesCol = db['api_schedule']

    for schedule in schedules:
        query = {'terminal' : schedule['terminal'], 'date': schedule['date'], 'shift': schedule['shift']}

        data = {
            "$setOnInsert": {'terminal' : schedule['terminal'], 'date': schedule['date'], 'shift': schedule['shift']},
            "$set": {'lines': schedule['lines'], 'timestamp': schedule['timestamp']},
        }
    
        schedulesCol.update(query, data, upsert=True)


def scrap_handler(event, context):
    config = load_config()
    targetConfig = extract_target_config(event['target'], config)
    dbConfig = extract_db_config(config)

    client = MongoClient(dbConfig['connectionString'])

    if targetConfig == None:
        return

    job = job_factory(targetConfig)

    schedules = job.run_job()
    
    write_to_db(client, schedules)


def fenix_handler(event, context):
    event['target'] = 'fenix'
    scrap_handler(event, context)

fenix_handler({}, None)