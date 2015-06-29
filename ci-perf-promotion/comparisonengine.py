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

    def compare_data(self, tool, metric_title, real_data, target_data):
        """
        Performs the comparison between configuration promotion gates and the
        actual data
        """
        # Loop over all of the transactions
        for session, metric_data in real_data:
            # Put the data into the JSON
            self.output_json[tool][metric_title] = metric_data

            # Check if the stats are up to snuff
            if metric_data < target_data:
                # Pass
                self.output_json["promotion_gates"][metric_title + "_passed"] = True
            else:
                # Fail
                self.output_json["promotion_gates"][metric_title + "_passed"] = False
                self.build_status_passed = False

    def process_performance_data(self):
        """
        Processes the data retrieved from the APIs, determines if the code
        meets the promotion gate criteria, and outputs the data as a JSON file
        """
        print("Processing performance data . . .")

        # Compare BlazeMeter metrics
        # Average Response Time
        if (self.configengine.response_time_avg > 0):
            self.compare_data("blazemeter", "response_time_avg", self.blazemeter.response_time_avg.items(), self.configengine.response_time_avg)
        # Max Response Time
        if (self.configengine.response_time_max > 0):
            self.compare_data("blazemeter", "response_time_max", self.blazemeter.response_time_max.items(), self.configengine.response_time_max)
        # Response Time Standard Deviation
        if (self.configengine.response_time_stdev > 0):
            self.compare_data("blazemeter", "response_time_stdev", self.blazemeter.response_time_stdev.items(), self.configengine.response_time_stdev)
        #TODO Add other checks for metrics

        # Set the overall status in the JSON file
        self.output_json["promotion_gates"]["passed"] = self.build_status_passed

        # JSON output file name
        filename = "ciperfpromodata_{0}.json".format(time.strftime("%m%d%y_%H%M%S"))

        # Create and write all of the data to a JSON file for later examination
        with open(filename, "w") as jsonoutput:
            json.dump(self.output_json, jsonoutput, sort_keys = True)

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

        # Output JSON report data - for use later
        self.output_json = {"promotion_gates": {}, "blazemeter": {},"appdynamics": {}}

        # Get the load testing data from the BlazeMeter API
        self.blazemeter = BlazeMeter(self.configengine.blazemeter_api_key, self.configengine.blazemeter_test_id)
        self.blazemeter.get_data()

        # Get the load testing data from the AppDynamics API
        self.appdynamics = AppDynamics()
        self.appdynamics.get_data()

        # Process the data
        self.process_performance_data()
