import json
import sys
import requests
from requests.auth import HTTPBasicAuth

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
        # Look for arguments telling us where the config file is located
        if (self.arg_lr != None):
            # Config is located remotely
            try:
                config_file = requests.get(self.arg_lr)
                return config_file.json()
            except:
                # Not able to find a configuration file at the specified location, quit out
                print("ERROR: Unable to find properly formatted remote configuration file")
                sys.exit(1)

        # Config is stored locally
        try:
            with open(self.filename) as config_file:
                return json.load(config_file)
        except:
            print("ERROR: Unable to find properly formatted config.json file")
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
        webpagetest_exists = False

        # Make sure that all of the config sections are there
        if "appdynamics" in config_json:
            appdynamics_exists = True
        if "blazemeter" in config_json:
            blazemeter_exists = True
        if "webpagetest" in config_json:
            webpagetest_exists = True
        if "promotion_gates" not in config_json:
            # If the promotion gates aren't in there, there's no use running the program
            self.required_config_error("promotion gates")
        if (appdynamics_exists == False and blazemeter_exists == False and webpagetest_exists == False):
            # If all of the modules don't exist, there's no way to get any data
            self.required_config_error("AppDynamics, BlazeMeter or WebPageTest")

        # AppDynamics Module
        config_output["appdynamics"] = {}
        if (appdynamics_exists):
            # AppDynamics Configuration Information -- Required
            if ("username" not in config_json["appdynamics"]) and (self.arg_appduser == None):
                self.required_config_error("AppDynamics username")
            elif ("password" not in config_json["appdynamics"]) and (self.arg_appdpass == None):
                self.required_config_error("AppDynamics password")
            elif ("application_name" not in config_json["appdynamics"]) and (self.arg_appdapp == None):
                self.required_config_error("AppDynamics application name")
            # Two ways to set length (load_test_length_min or load_test_start_ms and load_test_end_ms)
            # Check for:
            # - load_test_length_min is not set and at least one of the start/end times are not set
            # - load_test_length_min and load_test_start_ms or load_test_end_ms are set (both of the options are set)
            elif ((("load_test_length_min" not in config_json["appdynamics"]) and (("load_test_start_ms" not in config_json["appdynamics"]) or ("load_test_end_ms" not in config_json["appdynamics"]))) or
                  (("load_test_length_min" in config_json["appdynamics"]) and (("load_test_start_ms" in config_json["appdynamics"]) or ("load_test_end_ms" in config_json["appdynamics"])))):
                self.required_config_error("AppDynamics load test length")
            else:
                if (self.arg_appduser == None):
                    config_output["appdynamics"]["username"] = config_json["appdynamics"]["username"]
                else:
                    config_output["appdynamics"]["username"] = self.arg_appduser

                if (self.arg_appdpass == None):
                    config_output["appdynamics"]["password"] = config_json["appdynamics"]["password"]
                else:
                    config_output["appdynamics"]["password"] = self.arg_appdpass

                if (self.arg_appdapp == None):
                    config_output["appdynamics"]["application_name"] = config_json["appdynamics"]["application_name"]
                else:
                    config_output["appdynamics"]["application_name"] = self.arg_appdapp

                # The complicated load test length stuff
                if ("load_test_length_min" in config_json["appdynamics"]):
                    config_output["appdynamics"]["load_test_length"] = config_json["appdynamics"]["load_test_length_min"]
                elif (("load_test_start_ms" in config_json["appdynamics"]) and ("load_test_end_ms" in config_json["appdynamics"])):
                    config_output["appdynamics"]["load_test_start_ms"] = config_json["appdynamics"]["load_test_start_ms"]
                    config_output["appdynamics"]["load_test_end_ms"] = config_json["appdynamics"]["load_test_end_ms"]
                else:
                    # Something slipped through the cracks somehow, error out
                    self.required_config_error("AppDynamics load test length")

            # AppDynamics Promotion Gates -- Optional
            if ((("warning" not in config_json["promotion_gates"]) and ("critical" not in config_json["promotion_gates"])) or
                (("warning" in config_json["promotion_gates"]) and (config_json["promotion_gates"]["warning"] == False) and
                 ("critical" in config_json["promotion_gates"]) and (config_json["promotion_gates"]["critical"] == False))):
                # AppDynamics configuration information exists, but none of the metrics do (or we were told to ignore those that do exist)
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
        else:
            config_output["appdynamics"]["exists"] = False


        # BlazeMeter Module
        config_output["blazemeter"] = {}
        if (blazemeter_exists):
            # BlazeMeter Configuration Information -- Required
            if ("api" not in config_json["blazemeter"]) and (self.arg_blzkey == None):
                self.required_config_error("BlazeMeter API key")
            elif ("test_id" not in config_json["blazemeter"]) and (self.arg_blztest == None):
                self.required_config_error("BlazeMeter test ID")
            elif "test_length_sec" not in config_json["blazemeter"]:
                self.required_config_error("BlazeMeter test length (seconds)")
            else:
                if (self.arg_blzkey == None):
                    config_output["blazemeter"]["api_key"] = config_json["blazemeter"]["api"]
                else:
                    config_output["blazemeter"]["api_key"] = self.arg_blzkey

                if (self.arg_blztest == None):
                    config_output["blazemeter"]["test_id"] = config_json["blazemeter"]["test_id"]
                else:
                    config_output["blazemeter"]["test_id"] = self.arg_blztest

                config_output["blazemeter"]["test_length_sec"] = config_json["blazemeter"]["test_length_sec"]

            # BlazeMeter Promotion Gates -- Optional
            if (("response_time_avg"     not in config_json["promotion_gates"]) and
                ("response_time_max"     not in config_json["promotion_gates"]) and
                ("response_time_geomean" not in config_json["promotion_gates"]) and
                ("response_time_stdev"   not in config_json["promotion_gates"]) and
                ("response_time_tp90"    not in config_json["promotion_gates"]) and
                ("response_time_tp95"    not in config_json["promotion_gates"]) and
                ("response_time_tp99"    not in config_json["promotion_gates"]) and
                ("latency_max"           not in config_json["promotion_gates"]) and
                ("latency_avg"           not in config_json["promotion_gates"]) and
                ("latency_stdev"         not in config_json["promotion_gates"]) and
                ("bandwidth_avg"         not in config_json["promotion_gates"]) and
                ("transaction_rate"      not in config_json["promotion_gates"])):
                # Blazemeter configuration inforamtion exists, but none of the metrics do
                # Pretend BlazeMeter configuration information doesn't exist either so
                # that we don't waste our time querying the BlazeMeter API
                blazemeter_exists = False
                config_output["blazemeter"] = {"exists": False}
            else:
                # BlazeMeter still exists, put it in the config
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

                # Response time geometric mean
                if ("response_time_geomean" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_geomean"] = config_json["promotion_gates"]["response_time_geomean"]
                else:
                    config_output["promotion_gates"]["response_time_geomean"] = 0

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
                    config_output["promotion_gates"]["response_time_tp95"] = 0

                # Response time #99% line
                if ("response_time_tp99" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["response_time_tp99"] = config_json["promotion_gates"]["response_time_tp99"]
                else:
                    config_output["promotion_gates"]["response_time_tp99"] = 0

                # Maximum latency
                if ("latency_max" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["latency_max"] = config_json["promotion_gates"]["latency_max"]
                else:
                    config_output["promotion_gates"]["latency_max"] = 0

                # Average latency
                if ("latency_avg" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["latency_avg"] = config_json["promotion_gates"]["latency_avg"]
                else:
                    config_output["promotion_gates"]["latency_avg"] = 0

                # Latency Standard Deviation
                if ("latency_stdev" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["latency_stdev"] = config_json["promotion_gates"]["latency_stdev"]
                else:
                    config_output["promotion_gates"]["latency_stdev"] = 0

                # Average Bandwidth (AKA average bytes/second)
                if ("bandwidth_avg" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["bandwidth_avg"] = config_json["promotion_gates"]["bandwidth_avg"]
                else:
                    config_output["promotion_gates"]["bandwidth_avg"] = 0

                # Transaction Rate (AKA hits/second)
                if ("transaction_rate" in config_json["promotion_gates"]):
                    config_output["promotion_gates"]["transaction_rate"] = config_json["promotion_gates"]["transaction_rate"]
                else:
                    config_output["promotion_gates"]["transaction_rate"] = 0
        else:
            config_output["blazemeter"]["exists"] = False

        # WebPageTest Module
        config_output["webpagetest"] = {}
        if (webpagetest_exists):
            # WebPageTest Configuration Information -- Required
            if ("test_id" not in config_json["webpagetest"]) and (self.arg_wpgttest == None):
                self.required_config_error("WebPageTest test ID")
            else:
                config_output["webpagetest"] = {}
                if (self.arg_wpgttest == None):
                    config_output["webpagetest"]["test_id"] = config_json["webpagetest"]["test_id"]
                else:
                    config_output["webpagetest"]["test_id"] = self.arg_wpgttest

            # WebPageTest Promotion Gates -- Optional
            if ("first_view" not in config_json["promotion_gates"] and
                "repeat_view" not in config_json["promotion_gates"]):
                # WebPageTest configuration inforamtion exists, but none of the metrics do
                # Pretend WebPageTest configuration information doesn't exist either so
                # that we don't waste our time querying the WebPageTest API
                webpagetest_exists = False
                config_output["webpagetest"] = {"exists": False}
            else:
                # At least one of them exists
                config_output["webpagetest"]["exists"] = True

                # Make sure that we can put in promotion gates
                if ("promotion_gates" not in config_output):
                    config_output["promotion_gates"] = {}

                # All of the views that we have to loop over
                views = ["first_view", "repeat_view"]

                for view in views:
                    if (view in config_json["promotion_gates"]):
                        # Set up the view
                        config_output["promotion_gates"][view] = {}
                        # Speed Index
                        if ("speed_index" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["speed_index"] = config_json["promotion_gates"][view]["speed_index"]
                        else:
                            config_output["promotion_gates"][view]["speed_index"] = 0

                        # Time to First Paint
                        if ("first_paint" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["first_paint"] = config_json["promotion_gates"][view]["first_paint"]
                        else:
                            config_output["promotion_gates"][view]["first_paint"] = 0

                        # Time to First Byte
                        if ("first_byte" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["first_byte"] = config_json["promotion_gates"][view]["first_byte"]
                        else:
                            config_output["promotion_gates"][view]["first_byte"] = 0

                        # Time to Fully Loaded
                        if ("fully_loaded" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["fully_loaded"] = config_json["promotion_gates"][view]["fully_loaded"]
                        else:
                            config_output["promotion_gates"][view]["fully_loaded"] = 0

                        # Time to Visual Complete
                        if ("visual_complete" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["visual_complete"] = config_json["promotion_gates"][view]["visual_complete"]
                        else:
                            config_output["promotion_gates"][view]["visual_complete"] = 0

                        # Time to Start Render
                        if ("visual_complete" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["start_render"] = config_json["promotion_gates"][view]["start_render"]
                        else:
                            config_output["promotion_gates"][view]["start_render"] = 0

                        # Time to Last Visual Change
                        if ("last_visual_change" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["last_visual_change"] = config_json["promotion_gates"][view]["last_visual_change"]
                        else:
                            config_output["promotion_gates"][view]["last_visual_change"] = 0

                        # Time to <title></title> Tags Loaded
                        if ("title_time" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["title_time"] = config_json["promotion_gates"][view]["title_time"]
                        else:
                            config_output["promotion_gates"][view]["title_time"] = 0

                        # Page Size (Bytes In)
                        if ("page_size" in config_json["promotion_gates"][view]):
                            config_output["promotion_gates"][view]["page_size"] = config_json["promotion_gates"][view]["page_size"]
                        else:
                            config_output["promotion_gates"][view]["page_size"] = 0
        else:
            config_output["webpagetest"]["exists"] = False

        # Return all of the now properly formatted config data
        return config_output

    def __init__(self, filename, arg_lr, arg_blzkey, arg_blztest, arg_appduser, arg_appdpass, arg_appdapp, arg_wpgttest):
        """
        Class starting point
        """
        # Configuration file name
        self.filename = filename
        # Argument - Location Remote
        self.arg_lr = arg_lr
        # Argument - BlazeMeter API key
        self.arg_blzkey = arg_blzkey
        # Argument - BlazeMeter API test ID
        self.arg_blztest = arg_blztest
        # Argument - AppDynamics username
        self.arg_appduser = arg_appduser
        # Argument - AppDynamics password
        self.arg_appdpass = arg_appdpass
        # Argument - AppDynamics application name
        self.arg_appdapp = arg_appdapp
        # Argument - WebPageTest test ID
        self.arg_wpgttest = arg_wpgttest
