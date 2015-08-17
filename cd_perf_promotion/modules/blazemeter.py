import requests
import sys
import time

class BlazeMeter:
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self, api_key, test_id, test_length_sec):
        """
        Sets up all of the instance variables

        Keyword arguments:
        api_key - The BlazeMeter API key (string)
        test_id - The BlazeMeter Test ID (string)
        """
        # Test configuration information
        self.api_key = api_key
        self.test_id = test_id
        self.test_length = test_length_sec

    def connection_error(self):
        # User likely lost their internet connection or used incorrect credentials
        print("ERROR: Unable to query BlazeMeter API")
        sys.exit(1)

    def run_test(self, api_key, test_id):
        """
        Runs the load test
        """
        api_headers = {"Content-Type": "application/json", "x-api-key": api_key}

        # Run Performance test (HTTP GET request)
        run_test_url = "https://a.blazemeter.com/api/latest/tests/{0}/start".format(test_id)
        try:
            run_test_request = requests.get(run_test_url, headers=api_headers)
        except:
            self.connection_error()

        # Make sure that the module actually got something back
        if run_test_request.status_code != 200:
            self.connection_error()

        session_id = run_test_request.json()["result"]["sessionsId"][0]

        # Notify the user that the BlazeMeter test has run successfully
        print("Started BlazeMeter load test - standby for data")

        return session_id

    def get_data(self):
        """
        Gets the load test data from the API
        """
        api_headers = {"Content-Type": "application/json", "x-api-key": self.api_key}

        # Run the test and get the test session ID
        session_id = self.run_test(self.api_key, self.test_id)

        # Wait for the test to Complete
        # It takes max 4 minutes to launch test servers, so add how long it takes to run the test_summary_url
        # with how long it takes to get servers up.
        time.sleep(self.test_length + 240)

        # Get all of the aggregate (HTTP GET request)
        test_summary_url = "https://a.blazemeter.com/api/latest/sessions/{0}/reports/main/summary".format(session_id)
        try:
            test_summary_request = requests.get(test_summary_url, headers=api_headers)
        except:
            self.connection_error()

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
        print("Retrieved BlazeMeter data")

        return alltransactions
