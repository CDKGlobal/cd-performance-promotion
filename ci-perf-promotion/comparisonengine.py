from configengine import ConfigEngine
from blazemeter import BlazeMeter
from appdynamics import AppDynamics
import time
import json

class ComparisonEngine:
    """
    Queries the performance tools' APIs and determines if the build passes
    the target requirements.
    """

    def compare_blazemeter(self, metric_title, target_data, metric_data, transaction_index):
        """
        Performs the comparison between configuration promotion gates and the
        actual blazemeter test data
        """
        if (target_data > 0):
            # Metric is set in config, begin comparison

            # Get the "passed" JSON key name ready
            metric_title_passed = metric_title + "_passed"

            if metric_data[metric_title] < target_data:
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

        # Compare BlazeMeter metrics
        for index, metric_data in enumerate(self.blazemeter.transactions):

            # Average Response Time
            self.compare_blazemeter("response_time_avg", self.configengine.response_time_avg, metric_data, index)

            # Max Response Time
            self.compare_blazemeter("response_time_max", self.configengine.response_time_max, metric_data, index)

            # Response Time Standard Deviation
            self.compare_blazemeter("response_time_stdev", self.configengine.response_time_stdev, metric_data, index)

        #TODO Add other checks for metrics

        # Set the overall status in the JSON file
        self.output_json["promotion_gates"]["passed"] = self.build_status_passed

        # JSON output file name
        filename = "ciperfpromodata_{0}.json".format(time.strftime("%m%d%y_%H%M%S"))

        # Create and write all of the data to a JSON file for later examination
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

        # Get the load testing data from the BlazeMeter API
        self.blazemeter = BlazeMeter(self.configengine.blazemeter_api_key, self.configengine.blazemeter_test_id)
        self.blazemeter.get_data()

        # Get the load testing data from the AppDynamics API
        self.appdynamics = AppDynamics()
        self.appdynamics.get_data()

        # Output JSON report data - for use later
        self.output_json = {"promotion_gates": {}, "blazemeter": {"transactions": self.blazemeter.transactions}, "appdynamics": {}}

        # Process the data
        self.process_performance_data()
