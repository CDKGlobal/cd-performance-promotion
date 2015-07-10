from packages import requests

class BlazeMeter:
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self, api_key, test_session):
        """
        Sets up all of the instance variables
        """
        # Test configuration information
        self.api_key = api_key
        self.test_session = test_session

    def get_data(self):
        """
        Gets the load test data from the API
        """
        # Notify the user that the BlazeMeter data is being grabbed
        print("Retrieving the BlazeMeter data . . .")

        api_headers = {"Content-Type": "application/json", "x-api-key": self.api_key}

        # Get all of the aggregate (HTTP GET request)
        test_summary_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/summary".format(self.test_session)
        test_summary_request = requests.get(test_summary_url, headers=api_headers)

        alltransactions = []

        for transaction in test_summary_request.json()["result"]["summary"]:
            alltransactions.append({
                    "transaction_id": transaction["id"],
                    "transaction_name": transaction["lb"],
                    "response_time_avg": transaction["avg"],
                    "response_time_max": transaction["max"],
                    "response_time_stdev": transaction["std"],
                    "response_time_tp90": transaction["tp90"],
                    "response_time_tp95": transaction["tp95"],
                    "response_time_tp99": transaction["tp99"],
                    "transaction_rate": transaction["hits"] / transaction["duration"]
                })

        return alltransactions
