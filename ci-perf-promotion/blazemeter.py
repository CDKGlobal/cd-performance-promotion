from packages import requests
import json

class BlazeMeter:
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self):
        """
        Blazemeter API querent/data-gatherer
        """
        #TODO Implement the data storage

    def get_data(self, api_key, test_session):
        """
        Gets the load test data from the API
        """
        print("Retrieving the BlazeMeter data . . .")

        # Universal API Headers
        api_headers = {"Content-Type": "application/json", "x-api-key": api_key}

        # Get all of the business transactions
        transaction_list_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/data".format(test_session)
        transaction_list_request = requests.get(transaction_list_url, headers=api_headers)

        # Prepare the dict for data to be added
        test_data = {}

        for transaction in json.loads(transaction_list_request.text)["result"]["labels"]:
            transaction_detail_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/labels/{1}".format(test_session, transaction["id"])
            print("     " + transaction["id"] + " --- " + transaction["name"])
            transaction_detail_request = requests.get(transaction_detail_url, headers=api_headers)
            print(transaction_detail_request.text)
