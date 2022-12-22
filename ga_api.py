import utils

from google.oauth2 import service_account
from googleapiclient.discovery import build


def initialize_analytics_reporting(secret_manager_id, secret_manager_name):
    """
    Initializes an Analytics Reporting API V4 service object.
    Returns:
    An authorized Analytics Reporting API V4 service object.
    """
    creds = utils.access_secret_version(secret_manager_id, secret_manager_name, 'latest')

    credentials = service_account.Credentials.from_service_account_info(creds)
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/analytics.readonly']
    )

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=scoped_credentials, cache_discovery=False)

    return analytics


def get_ga_report(view_id, start_date, end_date, metrics_json, dimensions_json):
    """
    Arguments :
    view_id             : (string) GA View Id
    start_date          : (date) YYYY-MM-DD formatted start date
    end_date            : (date) YYYY-MM-DD formatted end date
    metrics_json        : (json) Array of objects containing GA metric config
    dimensions_json     : (json) Array of objects containing GA dimensions config

    Returns :
    The Analytics Reporting API V4 response
    """
    analytics = initialize_analytics_reporting()

    return_obj = analytics.reports().batchGet(
      body={
        'reportRequests': [
            {
                'viewId': view_id,
                'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                'metrics': metrics_json,
                'dimensions': dimensions_json
                }]
      }
    ).execute()

    return return_obj


def find_days_with_no_traffic(view_id):
    """
    TODO:
    • Create return object with the following JSON structure {'123456789' : []} where 123456789 is the view_id
    • Request a 13 month report of pageviews per day for the given GA view.
    • Loop through the report response, for each day with 0 pageviews append date to the return object Array
      Example: {'123123123' : ['2022-01-01', '2022-01-02']}
    • Return the final return object
    """
