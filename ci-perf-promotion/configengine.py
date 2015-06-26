import json
import sys

class ConfigEngine:
    """
    Processes the configuration file to find what the promotion gates are and
    the information necessary to grab the test data
    """

    def __init__(self):
        """
        Sets up all of the instance variables
        """
        # BlazeMeter
        self.blazemeter_api_key = ""
        self.blazemeter_test_id = ""
        # Performance Gate Criteria
        self.response_time_avg = 0

    def retrieve_config(self):
        """
        Finds the configuration file and processes it
        """
        with open("config.json") as config_file:
            try:
                # Load the JSON file
                config_data = json.load(config_file)
                # Get data out of the config
                self.blazemeter_api_key = config_data["blazemeter"]["api"]
                self.blazemeter_test_id = config_data["blazemeter"]["test_id"]
                self.response_time_avg = config_data["promotion_gate"]["response_time_avg"]
            except KeyError:
                # Was not able to find all of the JSON keys
                print("ERROR: Improperly named keys in configuration file")
                sys.exit(1)
            except:
                # Something else is very, very wrong with the configuration file
                print("ERROR: Improperly formatted configuration file")
                sys.exit(1)
