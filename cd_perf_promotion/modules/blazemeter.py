import requests
import time
from cd_perf_promotion.modules.perftools import PerfTools

class BlazeMeter(PerfTools):
    """
    Handles all of the BlazeMeter API querying/data gathering
    """

    def __init__(self, api_key, test_id):
        """
        Sets up all of the instance variables

        Keyword arguments:
        api_key - The BlazeMeter API key (string)
        test_id - The BlazeMeter Test ID (string)
        """
        # Test configuration information
        self.api_key = api_key
        self.test_id = test_id
        # Inherit methods from parent class "PerfTools"
        PerfTools.__init__(self, "BlazeMeter")

    def run_test(self, api_key, test_id):
        """
        Runs the load test
        """
        api_headers = {"Content-Type": "application/json", "x-api-key": api_key}

        # Run performance test (HTTP GET request)
        run_test_url = "https://a.blazemeter.com/api/latest/tests/{0}/start".format(test_id)
        try:
            run_test_request = requests.get(run_test_url, headers=api_headers)
        except:
            self.connection_error() # Inherited from the parent class

        # Make sure that the module actually got something back
        if run_test_request.status_code != 200:
            self.connection_error() # Inherited from the parent class

        session_id = run_test_request.json()["result"]["sessionsId"][0]

        # Notify the user that the BlazeMeter test has run successfully
        print("Booting up BlazeMeter servers... ({0})".format(session_id))

        return session_id

    def get_data(self):
        """
        Gets the load test data from the API
        """

        # Run the test and get the test session ID
        session_id = self.run_test(self.api_key, self.test_id)

        # Wait for the test to complete
        finished = False
        current_status = "BOOT_STARTING"
        while (finished == False):
            # Check the test status
            api_headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
            status_url = "https://a.blazemeter.com/api/latest/sessions/"
            try:
                sessions_request = requests.get(status_url, headers=api_headers)
            except:
                self.connection_error()

            # Make sure we got something back
            if sessions_request.status_code != 200:
                self.connection_error()

            # Examine the data
            sessions_data = sessions_request.json()

            for session in sessions_data["result"]:
                # Find our test session
                if session["id"] == session_id:
                    # Update the user on the current status
                    if (session["status"] == "INIT_SCRIPT") and (session["status"] != current_status):
                        print("Initializing BlazeMeter load test...")
                        current_status = session["status"]
                    elif (session["status"] == "DATA_RECIEVED") and (session["status"] != current_status):
                        print("Running BlazeMeter load test...")
                        current_status = session["status"]
                    elif (session["status"] == "ENDED"):
                        # Test is complete
                        finished = True
                        break
                    # We already found our session, no need to continue looping over the sessions
                    # returned by this request
                    break

        # Get all of the aggregate data (HTTP GET request)
        api_headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
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
            # Have to correct for BlazeMeter improperly informing you that a transaction took 0 ms
            if (transaction["duration"] == 0):
                bandwidth_avg = 0
                transaction_rate = 0
            else:
                bandwidth_avg = transaction["bytes"] / transaction["duration"]
                transaction_rate = transaction["hits"] / transaction["duration"]

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
                    "bandwidth_avg": bandwidth_avg,
                    "transaction_rate": transaction_rate
                })

        # Notify the user that the BlazeMeter data has grabbed
        print("Retrieved BlazeMeter data")

        return alltransactions
