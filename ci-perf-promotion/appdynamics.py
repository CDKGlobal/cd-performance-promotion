from packages import requests
from packages.requests.auth import HTTPBasicAuth

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

        # Get all of the aggregate (HTTP GET request)
        health_url = "https://cdkpe.saas.appdynamics.com/controller/rest/applications/{0}/problems/healthrule-violations?output=JSON&time-range-type=BEFORE_NOW&duration-in-mins={1}".format(self.application_name, self.test_length)
        health_request = requests.get(health_url, auth=HTTPBasicAuth(self.username, self.password))

        self.healthrule_violations = health_request.json()
        # For debugging purposes
        #print(health_request.json())
