from packages import requests
from packages.requests.auth import HTTPBasicAuth
from datetime import datetime
from datetime import timedelta

class AppDynamics:
    """
    Handles all of the AppDynamics API querying/data gathering
    """

    def __init__(self, username, password, application_name, test_length):
        """
        Sets up all of the instance variables

        Keyword arguments:
        username         - AppDynamics username as a string, used for API
                           authentication
        password         - AppDynamics password as a string, used for API
                           authentication
        application_name - The name of the AppDynamics application (string)
        test_length      - The length of the test in minutes. (e.g. When a user
                           specifies 60 minutes in the config, the monitoring
                           timeframe is from the time this program is run to
                           60 minutes before)
        """
        # API Credentials
        self.username = username
        self.password = password
        self.application_name = application_name
        self.test_length = test_length

    def get_data(self):
        """
        Get the data from the API
        """
        print("Retrieving the AppDynamics data . . .")

        # Figure out the start-time and end-time parameters for our API request
        # We need the time in milliseconds, but that time has to be the Unix
        # epoch time -- Time is hard
        epoch_time = datetime(1970, 1, 1)
        # Using this timestamp to ensure that we're working off of the same time
        # Works off of the system time zone, so as long as this is run on the
        # timezone as AppDynamics, we should be good to go
        timestamp = datetime.now()
        # Have to round because the API doesn't like partial milliseconds
        end_time = round((timestamp - epoch_time).total_seconds() * 1000)
        start_time = round((timestamp - epoch_time).total_seconds() * 1000)
        # Get all of the health violations (HTTP GET request)
        health_url = "https://cdkpe.saas.appdynamics.com/controller/rest/applications/{0}/problems/healthrule-violations?output=JSON&time-range-type=BETWEEN_TIMES&start-time={1}&end-time={2}".format(self.application_name, start_time, end_time)
        health_request = requests.get(health_url, auth=HTTPBasicAuth(self.username, self.password))

        healthrule_violations = health_request.json()

        # Reformat the data to only provide useful information
        for violation in healthrule_violations:
            # Remove uneccessary keys
            del violation["affectedEntityDefinition"]
            del violation["deepLinkUrl"]
            del violation["detectedTimeInMillis"]
            del violation["endTimeInMillis"]
            del violation["startTimeInMillis"]
            del violation["triggeredEntityDefinition"]

        return healthrule_violations
