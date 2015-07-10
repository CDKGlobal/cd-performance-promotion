from packages import requests
from packages.requests.auth import HTTPBasicAuth

class AppDynamics:
    """
    Handles all of the AppDynamics API querying/data gathering
    """

    def __init__(self, username, password, application_name, start_time, end_time):
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
        self.start_time = start_time
        self.end_time = end_time

    def get_data(self):
        """
        Get the data from the API
        """
        print("Retrieving the AppDynamics data . . .")

        # Get all of the health violations (HTTP GET request)
        health_url = "https://cdkpe.saas.appdynamics.com/controller/rest/applications/{0}/problems/healthrule-violations?output=JSON&time-range-type=BETWEEN_TIMES&start-time={1}&end-time={2}".format(self.application_name, self.start_time, self.end_time)
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
