import bq_api
import ga_api

def init(request={}, context={}):
    print("init")

    # ENVIRONMENT VARIABLES
    project_id = os.environ.get('PROJECT_ID', 'gallo-ga360-raw-291721')

    if request == {}:
        print("run local")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/Documents/credentials/ej-gallo-gcp.json")


    """
    TODO:
    • Finish ga_api.find_days_with_no_traffic function. Instructions found inside function.
    • Client wasn't able to unblock with json service account credential so I coded all in local
    env with no way to test so things like requirements.txt includes, file imports and all
    general debugging still needs to take place
    • This Init function should create a master list of missing BQ data by calling
    bq_api.find_missing_bq_date_shards() then loop through results to request a GA report
    for each view_id present
    • Use the results of the ga_api.find_days_with_no_traffic function to qualify if
    which days from the master list should remain. (Pop date from array since there's no traffic)
    What's remaining in the master list should now be your actionable list of days you can present
    to GA 360 Support to request a backfill 
    """


init() #                                                                        ---- LOCAL TESTING ONLY ----
