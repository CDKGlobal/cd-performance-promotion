from packages import requests

class BlazeMeter:
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self):
        """
        Blazemeter API querent/data-gatherer
        """
        #TODO Implement the data storage

    def get_data(self):
        """
        Get the data from the API
        """
        print("Retrieving the BlazeMeter data . . .")

        #TODO Request the data from BlazeMeter

        test_session = "r-op-beta5589cdb371a9d"
        transactions_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/data".format(test_session)

        #Need to write the request stuffs
        #transactions_request_get = requests.get(transactions_url)
