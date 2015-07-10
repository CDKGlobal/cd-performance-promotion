import json
import sys

class ConfigEngine:
    """
    Processes the configuration file to find what the promotion gates are and
    the information necessary to grab the test data
    """

    def required_config_error(self, required_item):
        """
        Prints an error message if a part of the configuration file is not found

        Keyword arguments:
        required_item - the item that is missing from the configuration file
        """
        print("ERROR: Unable to find {0}".format(required_item))
        sys.exit(1)

    def retrieve_config(self):
        """
        Finds the configuration file and grabs the JSON data out of it
        """
        with open("config.json") as config_file:
            try:
                # Load the JSON file
                return json.load(config_file)
            except:
                # Something is wrong with the JSON config file, abort the
                # program
                print("ERROR: Improperly formatted configuration file")
                sys.exit(1)

    def process_config(self):
        """
        Gets the configuration file and processes it
        """
        # Get the config file
        config_json = self.retrieve_config()

        # Stores all of the data in a format that the dataengine and
        # comparsionengine can deal with
        config_output = {}

        # Variables used to note whether or not these modules were set up in
        # the configuration file. Default to False
        appdynamics_exists = False
        blazemeter_exists = False

        # Make sure that all of the config sections are there
        if "appdynamics" in config_json:
            appdynamics_exists = True
        if "blazemeter" in config_json:
            blazemeter_exists = True
        if "promotion_gates" not in config_json:
            # If the promotion gates aren't in there, there's no use running
            # the program
            self.required_config_error("promotion gates")
        if (appdynamics_exists == False and blazemeter_exists == False):
            # If all of the modules don't exist, there's no way to get any data
            self.required_config_error("AppDynamics or BlazeMeter")

        # AppDynamics Module
        if (appdynamics_exists):
            # AppDynamics Configuration Information -- Required
            if "username" not in config_json["appdynamics"]:
                self.required_config_error("AppDynamics username")
            elif "password" not in config_json["appdynamics"]:
                self.required_config_error("AppDynamics password")
            elif "application_name" not in config_json["appdynamics"]:
                self.required_config_error("AppDynamics application name")
            elif "load_test_length_min" not in config_json["appdynamics"]:
                self.required_config_error("AppDynamics load test length")
            else:
                config_output["appdynamics"] = {}
                config_output["appdynamics"]["username"] = config_json["appdynamics"]["username"]
                config_output["appdynamics"]["password"] = config_json["appdynamics"]["password"]
                config_output["appdynamics"]["application_name"] = config_json["appdynamics"]["application_name"]
                config_output["appdynamics"]["load_test_length"] = config_json["appdynamics"]["load_test_length_min"]

            # AppDynamics Promotion Gates -- Optional
            if (("warning"  not in config_json["promotion_gates"]) and
                ("critical" not in config_json["promotion_gates"])):
                # AppDynamics configuration information exists, but none of the metrics do
                # Pretend AppDynamics configuration information doesn't exist either so
                # that we don't waste our time querying the AppDynamics API
                appdynamics_exists = False
                config_output["appdynamics"] = {"exists": False}
            else:
                # AppDynamics still exists
                config_output["appdynamics"]["exists"] = True

                # Make sure that we can put in promotion gates
                if ("promotion_gates" not in config_output):
                    config_output["promotion_gates"] = {}

                # Warning health violation
                if "warning" in config_json["promotion_gates"]:
                    config_output["promotion_gates"]["warning"] = config_json["promotion_gates"]["warning"]
                else:
                    # Warning = False means that the user doesn't care about
                    # health violations with a status of WARNING
                    config_output["promotion_gates"]["warning"] = False

                # Critical health violation
                if "critical" in config_json["promotion_gates"]:
                    config_output["promotion_gates"]["critical"] = config_json["promotion_gates"]["critical"]
                else:
                    # Critical = False means that the user doesn't care about
                    # health violations with a status of CRITICAL
                    config_output["promotion_gates"]["critical"] = False

        # BlazeMeter Module
        if (blazemeter_exists):
            # BlazeMeter Configuration Information -- Required
            if "api" not in config_json["blazemeter"]:
                self.required_config_error("BlazeMeter API key")
            elif "test_id" not in config_json["blazemeter"]:
                self.required_config_error("BlazeMeter test ID")
            else:
                config_output["blazemeter"] = {}
                config_output["blazemeter"]["api_key"] = config_json["blazemeter"]["api"]
                config_output["blazemeter"]["test_id"] = config_json["blazemeter"]["test_id"]

            # BlazeMeter Promotion Gates -- Optional
            if (("response_time_avg"   not in config_json["promotion_gates"]) and
                ("response_time_max"   not in config_json["promotion_gates"]) and
                ("response_time_stdev" not in config_json["promotion_gates"]) and
                ("response_time_tp90"  not in config_json["promotion_gates"]) and
                ("response_time_tp95"  not in config_json["promotion_gates"]) and
                ("response_time_tp99"  not in config_json["promotion_gates"]) and
                ("transaction_rate"    not in config_json["promotion_gates"])):
                # Blazemeter configuration inforamtion exists, but none of the metrics do
                # Pretend BlazeMeter configuration information doesn't exist either so
                # that we don't waste our time querying the BlazeMeter API
                blazemeter_exists = False
                config_output["blazemeter"] = {"exists": False}
            else:
                # BlazeMeter still exists
                config_output["blazemeter"]["exists"] = True

                # Make sure that we can put in promotion gates
                if ("promotion_gates" not in config_output):
                    config_output["promotion_gates"] = {}

                # Average response time
                if ("response_time_avg" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_avg"] = config_json["promotion_gates"]["response_time_avg"]
                else:
                    # 0 means that the user doesn't care about the metric
                    config_output["promotion_gates"]["response_time_avg"] = 0

                # Maximum response time
                if ("response_time_max" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_max"] = config_json["promotion_gates"]["response_time_max"]
                else:
                    config_output["promotion_gates"]["response_time_max"] = 0

                # Response time standard deviation
                if ("response_time_stdev" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_stdev"] = config_json["promotion_gates"]["response_time_stdev"]
                else:
                    config_output["promotion_gates"]["response_time_stdev"] = 0

                # Response time 90% line
                # e.g. 90% of the requests fell at or below this response time
                # e.g. 90% of the requests had this response time
                if ("response_time_tp90" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_tp90"] = config_json["promotion_gates"]["response_time_tp90"]
                else:
                    config_output["promotion_gates"]["response_time_tp90"] = 0

                # Response time 95% line
                if ("response_time_tp95" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_tp95"] = config_json["promotion_gates"]["response_time_tp95"]
                else:
                    config_output["promotion_gates"]["response_time_tp90"] = 0

                # Response time #99% line
                if ("response_time_tp99" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_tp99"] = config_json["promotion_gates"]["response_time_tp99"]
                else:
                    config_output["promotion_gates"]["response_time_tp99"] = 0

                # Transaction Rate (AKA hits/second)
                if ("transaction_rate" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["transaction_rate"] = config_json["promotion_gates"]["transaction_rate"]
                else:
                    config_output["promotion_gates"]["transaction_rate"] = 0

        # Return all of the now properly formatted config data
        return config_output
