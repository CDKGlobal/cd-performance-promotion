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
        # Performance Gate Criteria
        self.response_time_avg = 0
        self.response_time_max = 0
        self.response_time_stdev = 0
        self.response_time_tp90 = 0
        self.response_time_tp95 = 0
        self.response_time_tp99 = 0
        self.transaction_rate = 0
        # True = health violations classified as this item will fail the build
        self.warning = False
        self.critical = False

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
            except:
                # Something is wrong with the JSON config file, abort the
                # program
                print("ERROR: Improperly formatted configuration file")
                sys.exit(1)

        # Variables used to note whether or not these objects exist
        # Default to False
        self.appdynamics_exists = False
        self.blazemeter_exists = False

        # Make sure that all of the config sections are there
        if "appdynamics" in config_data:
            self.appdynamics_exists = True
        if "blazemeter" in config_data:
            self.blazemeter_exists = True
        if "promotion_gates" not in config_data:
            self.required_config_error("promotion gates")
        if (self.appdynamics_exists == False and self.blazemeter_exists == False):
            self.required_config_error("AppDynamics or BlazeMeter")

        # AppDynamics Module
        if (self.appdynamics_exists):
            # AppDynamics Configuration Information
            if "username" not in config_data["appdynamics"]:
                self.required_config_error("AppDynamics username")
            elif "password" not in config_data["appdynamics"]:
                self.required_config_error("AppDynamics password")
            elif "application_name" not in config_data["appdynamics"]:
                self.required_config_error("AppDynamics application name")
            elif "load_test_length_min" not in config_data["appdynamics"]:
                self.required_config_error("AppDynamics load test length")
            else:
                self.appdynamics_username = config_data["appdynamics"]["username"]
                self.appdynamics_password = config_data["appdynamics"]["password"]
                self.appdynamics_application_name = config_data["appdynamics"]["application_name"]
                self.appdynamics_load_test_length = config_data["appdynamics"]["load_test_length_min"]

            # Make sure that promotion gates are actually defined
            if (("warning"  not in config_data["promotion_gates"]) and
                ("critical" not in config_data["promotion_gates"])):

                # AppDynamics configuration information exists, but none of the metrics do
                # Pretend AppDynamics configuration information doesn't exist either so
                # that we don't waste our time querying the AppDynamics API
                self.appdynamics_exists = False
            else:
                # AppDynamics Promotion Gates
                if "warning" in config_data["promotion_gates"]:
                    self.warning = config_data["promotion_gates"]["warning"]
                if "critical" in config_data["promotion_gates"]:
                    self.critical = config_data["promotion_gates"]["critical"]

        # BlazeMeter Module
        if (self.blazemeter_exists):
            # BlazeMeter Configuration Information -- Required
            if "api" not in config_data["blazemeter"]:
                self.required_config_error("BlazeMeter API key")
            elif "test_id" not in config_data["blazemeter"]:
                self.required_config_error("BlazeMeter test ID")
            else:
                self.blazemeter_api_key = config_data["blazemeter"]["api"]
                self.blazemeter_test_id = config_data["blazemeter"]["test_id"]

            # BlazeMeter Promotion Gates -- Optional
            if (("response_time_avg"   not in config_data["promotion_gates"]) and
                ("response_time_max"   not in config_data["promotion_gates"]) and
                ("response_time_stdev" not in config_data["promotion_gates"]) and
                ("response_time_tp90"  not in config_data["promotion_gates"]) and
                ("response_time_tp95"  not in config_data["promotion_gates"]) and
                ("response_time_tp99"  not in config_data["promotion_gates"]) and
                ("transaction_rate"    not in config_data["promotion_gates"])):

                # Blazemeter configuration inforamtion exists, but none of the metrics do
                # Pretend BlazeMeter configuration information doesn't exist either so
                # that we don't waste our time querying the BlazeMeter API
                self.blazemeter_exists = False
            else:
                # BlazeMeter Promotion Gates
                if ("response_time_avg" in config_data["promotion_gates"]):
                    self.response_time_avg = config_data["promotion_gates"]["response_time_avg"]
                if ("response_time_max" in config_data["promotion_gates"]):
                    self.response_time_max = config_data["promotion_gates"]["response_time_max"]
                if ("response_time_stdev" in config_data["promotion_gates"]):
                    self.response_time_stdev = config_data["promotion_gates"]["response_time_stdev"]
                if ("response_time_tp90" in config_data["promotion_gates"]):
                    self.response_time_tp90 = config_data["promotion_gates"]["response_time_tp90"]
                if ("response_time_tp95" in config_data["promotion_gates"]):
                    self.response_time_tp95 = config_data["promotion_gates"]["response_time_tp95"]
                if ("response_time_tp99" in config_data["promotion_gates"]):
                    self.response_time_tp99 = config_data["promotion_gates"]["response_time_tp99"]
                if ("transaction_rate" in config_data["promotion_gates"]):
                    self.transaction_rate = config_data["promotion_gates"]["transaction_rate"]
