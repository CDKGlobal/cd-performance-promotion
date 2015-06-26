from packages import requests
#import json

class BlazeMeter:
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self, api_key, test_session):
        """
        Blazemeter API querent/data-gatherer
        """
        # Universal API Headers
        self.api_headers = {"Content-Type": "application/json", "x-api-key": api_key}
        # Test configuration information
        self.api_key = api_key
        self.test_session = test_session
        # Test result information
        self.response_time_avg = {}


    def get_data(self):
        """
        Gets the load test data from the API
        """
        # Notify the user that the BlazeMeter data is being grabbed
        print("Retrieving the BlazeMeter data . . .")

        # Get all of the business transactions (HTTP GET request)
        transaction_list_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/data".format(self.test_session)
        transaction_list_request = requests.get(transaction_list_url, headers=self.api_headers)

        for transaction in transaction_list_request.json()["result"]["labels"]:
            # Get the overall information on the transaction
            transaction_detail_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/labels/{1}".format(self.test_session, transaction["id"])
            transaction_id = transaction["id"]
            transaction_name = transaction["name"]

            # Output it to the console
            print("     " + transaction_id + " --- " + transaction_name)

            # Get the detail information on the transaction (HTTP GET request)
            transaction_detail_request = requests.get(transaction_detail_url, headers=self.api_headers)

            # Store the data for later usage and output it to the console
            self.response_time_avg[transaction_id] = transaction_detail_request.json()["result"]["summary"]["avg"]
            print("          Response Time Avg: {0}".format(self.response_time_avg[transaction_id]))
            #TODO Grab more data

            #print(transaction_detail_request.text)
