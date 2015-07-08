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
        """
        # API Credentials
        self.username = username
        self.password = password
        self.application_name = application_name
        self.test_length = test_length
        # Health rule violations that exist
        self.healthrule_violations = []

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

        self.healthrule_violations = health_request.json()

        # Reformat the data to only provide useful information
        for violation in self.healthrule_violations:
            # Remove uneccessary keys
            del violation["affectedEntityDefinition"]
            del violation["deepLinkUrl"]
            del violation["detectedTimeInMillis"]
            del violation["endTimeInMillis"]
            del violation["startTimeInMillis"]
            del violation["triggeredEntityDefinition"]
