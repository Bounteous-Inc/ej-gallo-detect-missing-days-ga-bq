import json

from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from google.cloud import bigquery


def return_dataset_ids():
    """
    Arguments :
    None

    Returns :
    Array of strings
    """

    client = bigquery.Client()

    datasets = list(client.list_datasets())
    dataset_ids = []

    for dataset in datasets:
        dataset_ids.append(dataset.dataset_id)

    return dataset_ids


def find_missing_bq_date_shards(project_id, months=-13):
    """
    Generates a master list of all missing BQ date shards for every dataset found. (Client BQ only contains UA datasets)

    Arguments :
    project_id          : (string) GCP project identifier
    months              : (integer) Number of months needed for lookback date

    Returns :
    Dictionary
        Key : (string) BQ Dataset Id (Google View Id)
        Value : (array) Dates
    """

    dataset_ids = return_dataset_ids()
    end_date = date.today() - timedelta(days=1)
    formatted_end_date = end_date.strftime("%Y%m%d")
    start_date = end_date + relativedelta(months=months)
    formatted_start_date = start_date.strftime("%Y%m%d")
    return_obj = {}

    dataset_ids = ['101822448']  # ----- HARDCODED FOR TESTING -----

    client = bigquery.Client()

    for dataset_id in dataset_ids:
        sql_string = """
            SELECT date FROM UNNEST(GENERATE_DATE_ARRAY(PARSE_DATE("%Y%m%d", '{}'), PARSE_DATE("%Y%m%d", '{}'))) date
            EXCEPT DISTINCT
            SELECT PARSE_DATE("%Y%m%d", _TABLE_SUFFIX) as `date` FROM `{}.{}.ga_sessions_*`
            WHERE _TABLE_SUFFIX BETWEEN '{}' AND '{}'
            GROUP BY date
            ORDER BY date ASC
        """.format(formatted_start_date, formatted_end_date, project_id, dataset_id, formatted_start_date, formatted_end_date)

        query_job = client.query(sql_string)
        results = query_job.result()
        date_array = []
        for row in results:
            date_array.append(row.date.strftime("%Y-%m-%d"))
        return_obj[dataset_id] = date_array

    return return_obj
