import requests
import sys

class BlazeMeter:
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self, api_key, test_session):
        """
        Sets up all of the instance variables

        Keyword arguments:
        api_key      - The BlazeMeter API key (string)
        test_session - The BlazeMeter Test ID (string)
        """
        # Test configuration information
        self.api_key = api_key
        self.test_session = test_session

    def connection_error(self):
        # User likely lost their internet connection or used incorrect credentials
        print("ERROR: Unable to query BlazeMeter API")
        sys.exit(1)

    def get_data(self):
        """
        Gets the load test data from the API
        """
        api_headers = {"Content-Type": "application/json", "x-api-key": self.api_key}

        # Get all of the aggregate (HTTP GET request)
        test_summary_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/summary".format(self.test_session)
        try:
            test_summary_request = requests.get(test_summary_url, headers=api_headers)
        except:
            connection_error()

        alltransactions = []

        # Make sure that the module actually got something back
        if test_summary_request.status_code != 200:
            self.connection_error()

        for transaction in test_summary_request.json()["result"]["summary"]:
            alltransactions.append({
                    "transaction_id": transaction["id"],
                    "transaction_name": transaction["lb"],
                    "response_time_avg": transaction["avg"],
                    "response_time_max": transaction["max"],
                    "response_time_geomean": transaction["geoMean"],
                    "response_time_stdev": transaction["std"],
                    "response_time_tp90": transaction["tp90"],
                    "response_time_tp95": transaction["tp95"],
                    "response_time_tp99": transaction["tp99"],
                    "latency_max": transaction["latencyMax"],
                    "latency_avg": transaction["latencyAvg"],
                    "latency_stdev": transaction["latencySTD"],
                    "bandwidth_avg": transaction["bytes"] / transaction["duration"],
                    "transaction_rate": transaction["hits"] / transaction["duration"]
                })

        # Notify the user that the BlazeMeter data has grabbed
        print("Retrieved BlazeMeter  data")

        return alltransactions
