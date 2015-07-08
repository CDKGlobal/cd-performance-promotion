from configengine import ConfigEngine
from blazemeter import BlazeMeter
from appdynamics import AppDynamics
import time
import json
import operator

class ComparisonEngine:
    """
    Queries the performance tools' APIs and determines if the build passes
    the target requirements.
    """

    def check_health_severity(self, violation):
        """
        Fails the build if the defined severity is found in the health rule
        violations
        """
        # Add the violation to the output file after removing unecessary data
        self.output_json["appdynamics"]["healthrule_violations"].append(violation)
        # Fail the build
        self.output_json["promotion_gates"]["appdynamics_health"] = False
        self.build_status_passed = False

    def compare_appdynamics(self):
        """
        Performs the comparison between the defined violation severity settings
        and the violations that occurred
        """
        # Set the health to True by default and flip it if necessary
        self.output_json["promotion_gates"]["appdynamics_health"] = True

        for violation in self.appdynamics.healthrule_violations:
            # Check if the severity settings that we care about exist in the health rule violations
            if ((self.configengine.warning == True) and (violation["severity"] == "WARNING")):
                self.check_health_severity(violation)
            if ((self.configengine.critical == True) and (violation["severity"] == "CRITICAL")):
                self.check_health_severity(violation)

    def compare_blazemeter(self, metric_title, target_data, metric_data, transaction_index, operator):
        """
        Performs the comparison between configuration promotion gates and the
        actual blazemeter test data
        """
        if (target_data > 0):
            # Metric is set in config, begin comparison

            # Add the data to the output file
            self.output_json["blazemeter"]["transactions"][transaction_index][metric_title] = metric_data

            # Get the "passed" JSON key name ready
            metric_title_passed = metric_title + "_passed"

            # Determine if promotion gate was met
            # Uses the operator module so that the process_performance_data function can determine
            # what operator (<, >, <=, >=, etc.) should be used
            if operator(metric_data, target_data):
                # Success
                if metric_title_passed not in self.output_json["promotion_gates"]:
                    # Not mentioned before, add it in
                    # Not necessary to make the overall status True again if it's True
                    # and if it was False for one transaction the overall status should still be False
                    self.output_json["promotion_gates"][metric_title_passed] = True
                # Regardless, add it into the transaction data
                self.output_json["blazemeter"]["transactions"][transaction_index][metric_title_passed] = True
            else:
                # Failure
                self.output_json["promotion_gates"][metric_title_passed] = False
                self.output_json["blazemeter"]["transactions"][transaction_index][metric_title_passed] = False
                self.build_status_passed = False

    def process_performance_data(self):
        """
        Processes the data retrieved from the APIs, determines if the code
        meets the promotion gate criteria, and outputs the data as a JSON file
        """
        print("Processing performance data . . .")

        # AppDynamics Module
        if (self.configengine.appdynamics_exists):
            # Check for AppDynamics Health Violations (only if the user cares)
            if (self.configengine.warning or self.configengine.critical):
                if (self.appdynamics.healthrule_violations != []):
                    # Uh-oh, there's something wrong with the build
                    self.output_json["appdynamics"] = {"healthrule_violations": []}
                    self.compare_appdynamics()
                else:
                    # No health violations, good to go!
                    self.output_json["promotion_gates"]["appdynamics_health"] = True

        # BlazeMeter Module
        if (self.configengine.blazemeter_exists):
            # Compare BlazeMeter metrics
            # Add BlazeMeter into the output file
            self.output_json["blazemeter"] = {"transactions": []}
            for index, transaction in enumerate(self.blazemeter.transactions):
                # Add transaction information into the output
                self.output_json["blazemeter"]["transactions"].append({"transaction_id": transaction["transaction_id"], "transaction_name": transaction["transaction_name"]})
                # Average Response Time
                self.compare_blazemeter("response_time_avg", self.configengine.response_time_avg, transaction["response_time_avg"], index, operator.lt)
                # Max Response Time
                self.compare_blazemeter("response_time_max", self.configengine.response_time_max, transaction["response_time_max"], index, operator.lt)
                # Response Time Standard Deviation
                self.compare_blazemeter("response_time_stdev", self.configengine.response_time_stdev, transaction["response_time_stdev"], index, operator.lt)
                # Response Time 90% Line
                self.compare_blazemeter("response_time_tp90", self.configengine.response_time_tp90, transaction["response_time_tp90"], index, operator.lt)
                # Response Time 95% Line
                self.compare_blazemeter("response_time_tp95", self.configengine.response_time_tp95, transaction["response_time_tp95"], index, operator.lt)
                # Response Time 99% Line
                self.compare_blazemeter("response_time_tp99", self.configengine.response_time_tp99, transaction["response_time_tp99"], index, operator.lt)
                # Transaction Rate
                self.compare_blazemeter("transaction_rate", self.configengine.transaction_rate, transaction["transaction_rate"], index, operator.gt)

        # Set the overall status in the JSON file
        self.output_json["promotion_gates"]["passed"] = self.build_status_passed

        # Create and write all of the data to a JSON file for later examination
        filename = "ciperfpromodata_{0}.json".format(time.strftime("%m%d%y_%H%M%S"))
        with open(filename, "w") as jsonoutput:
            json.dump(self.output_json, jsonoutput, indent = 4, sort_keys = True)

        # Let the user know where they can get all of the information
        print("\nPlease see {0} for more information".format(filename))

        # Print the final build status to the console
        if self.build_status_passed:
            print("\nBuild Status: SUCCESS")
        else:
            print("\nBuild Status: FAILURE")

    def get_performance_data(self):
        """
        Begins retrieving the data and comparing it against the targets
        """
        #TODO Look into making this multithreaded, one thread for each api call and closing them all off with join()
        # Get the configuration file information
        self.configengine = ConfigEngine()
        self.configengine.retrieve_config()

        # Build Status
        self.build_status_passed = True

        # Check if the AppDynamics module was requested
        if (self.configengine.appdynamics_exists):
            self.appdynamics = AppDynamics(self.configengine.appdynamics_username,
                                           self.configengine.appdynamics_password,
                                           self.configengine.appdynamics_application_name,
                                           self.configengine.appdynamics_load_test_length)
            self.appdynamics.get_data()

        # Get the load testing data from the BlazeMeter API
        # Check if the BlazeMeter module was requested
        if (self.configengine.blazemeter_exists):
            self.blazemeter = BlazeMeter(self.configengine.blazemeter_api_key, self.configengine.blazemeter_test_id)
            self.blazemeter.get_data()

        # Output JSON report data
        # Later appended by the AppDynamics and BlazeMeter modules in
        # process_performance_data()
        self.output_json = {"promotion_gates": {}}

        # Process the data
        self.process_performance_data()
