import requests
import xmltodict
import json
import sys

class WebPageTest:
    """
    Handles all of the WebPageTest API querying/data gathering
    """

    def __init__(self, test_session):
        """
        Sets up all of the instance variables

        Keyword arguments:
        api_key      - The WebPageTest API key (string)
        test_session - The WebPageTest Test ID (string)
        """
        # Test configuration information
        self.test_session = test_session

    def get_data(self):
        """
        Gets the load test data from the API
        """
        # Notify the user that the WebPageTest data is being grabbed
        print("Retrieving WebPageTest data . . .")

        # Get all of the aggregate (HTTP GET request)
        test_summary_url = "http://www.webpagetest.org/xmlResult/{0}/".format(self.test_session)
        try:
            test_summary_request = requests.get(test_summary_url)
        except:
            # User likely lost their internet connection
            print("ERROR: Unable to query WebPageTest API")
            sys.exit(1)
        # Convert all of the WebPageTest data from XML to JSON and return it
        test_results = json.loads(json.dumps(xmltodict.parse(test_summary_request.content)))
        return test_results
