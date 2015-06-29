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
        self.response_time_max = 0
        self.response_time_stdev = 0

    def required_config_error(self, required_item):
        print("ERROR: Unable to find {0}".format(required_item))
        sys.exit(1)

    def retrieve_config(self):
        """
        Finds the configuration file and processes it
        """
        with open("config.json") as config_file:
            try:
                # Load the JSON file
                config_data = json.load(config_file)
                # Just do a check to make sure that all of the sections are included in the config file
                #config_data["blazemeter"]
                #config_data["appdynamics"]
                #config_data["promotion_gate"]
            except:
                # Something is wrong with the JSON config file, abort the program
                print("ERROR: Improperly formatted configuration file")
                sys.exit(1)

            # Make sure that all of the config sections are there
            if "blazemeter" not in config_data:
                self.required_config_error("Blazemeter")
            elif "promotion_gates" not in config_data:
                self.required_config_error("promotion gates")

            # Get the mandatory configuration information (api keys, test IDs, etc.)
            if "api" not in config_data["blazemeter"]:
                self.required_config_error("BlazeMeter API key")
            elif "test_id" not in config_data["blazemeter"]:
                self.required_config_error("BlazeMeter test ID")
            else:
                self.blazemeter_api_key = config_data["blazemeter"]["api"]
                self.blazemeter_test_id = config_data["blazemeter"]["test_id"]

            # Begin evaluating the promotion gates
            # All of these are allowed to be non-mandatory so that the user can select as many or as few
            # criteria as they would like
            if "response_time_avg" in config_data["promotion_gates"]:
                self.response_time_avg = config_data["promotion_gates"]["response_time_avg"]
            if "response_time_max" in config_data["promotion_gates"]:
                self.response_time_max = config_data["promotion_gates"]["response_time_max"]
            if "response_time_stdev" in config_data["promotion_gates"]:
                self.response_time_stdev = config_data["promotion_gates"]["response_time_stdev"]
