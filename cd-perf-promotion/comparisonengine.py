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

        Keyword arguments:
        violation - dictionary that contains all of the information for a single
                    violation (as determined by AppDynamics)
        """
        # Add the violation to the output file after removing unecessary data
        self.output_json["appdynamics"]["healthrule_violations"].append(violation)
        # Fail the build
        self.output_json["promotion_gates"]["appdynamics_health"] = False
        self.build_status_passed = False

    def compare_appdynamics(self, healthrule_violations, warning, critical):
        """
        Performs the comparison between the defined violation severity settings
        and the violations that occurred

        Keyword arguments:
        healthrule_violations  - Dictionary that contains all of the AppDynamics
                                 health violations
        warning                - Boolean that indicates whether the user thinks
                                 that health rule violations with a status of
                                 "WARNING" are important enough to evaluate
        critical               - Boolean that indicates whether the user thinks
                                 that health rule violations with a status of
                                 "CRITICAL" are important enough to evaluate
        """
        # Set the health to True by default and flip it if necessary
        self.output_json["promotion_gates"]["appdynamics_health"] = True

        for violation in healthrule_violations:
            # Check if the severity settings that we care about exist in the health rule violations
            if ((warning == True) and (violation["severity"] == "WARNING")):
                self.check_health_severity(violation)
            if ((critical == True) and (violation["severity"] == "CRITICAL")):
                self.check_health_severity(violation)

    def compare_blazemeter(self, metric_title, target_data, metric_data, transaction_index, operator):
        """
        Performs the comparison between configuration promotion gates and the
        actual blazemeter test data

        Keyword arguments:
        metric_title      - String title that indicates the data item that is being
                            evaluated
        target_data       - Number that indicates the cutoff point for the specific
                            metric as determined by the user in the config
        metric_data       - The actual performance data number that is compared
                            against
        transaction_index - The index of the transaction in the list of
                            transactions
        operator          - <, >, <=, >, == which is used to compare the real
                            data against the config
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

    def output_results(self):
        """
        Output the results to a JSON file
        """
        filename = "cdperfpromodata_{0}.json".format(time.strftime("%m%d%y_%H%M%S"))
        with open(filename, "w") as jsonoutput:
            json.dump(self.output_json, jsonoutput, indent = 4, sort_keys = True)

        # Let the user know where they can get all of the results
        print("\nPlease see {0} for more information".format(filename))

        # Print the final build status to the console
        if self.build_status_passed:
            print("\nBuild Status: SUCCESS")
        else:
            print("\nBuild Status: FAILURE")

    def process_data(self, config_data, perf_data):
        """
        Determines if the build meets promotion gate criteria based off of the
        information in the config file (retrieved by configengine) and the data
        from the modules (retrieved by dataengine)

        Keyword Arguments:
        config_data - dictionary that contains all of the information retrieved
                      by the config engine
        perf_data   - dictionary that contains all of the information retrieved
                      by the data engine
        """
        print("Processing performance data . . .")

        # Prepare the output file promotion gates section
        self.output_json["promotion_gates"] = {}

        # AppDynamics Module
        if (config_data["appdynamics"]["exists"] == True):
            # Check for AppDynamics Health Violations (only if the user cares)
            if ((config_data["promotion_gates"]["warning"] == True) or (config_data["promotion_gates"]["critical"] == True)):
                if (perf_data["appdynamics"]["healthrule_violations"] != []):
                    # Uh-oh, there's something wrong with the build
                    self.output_json["appdynamics"] = {"healthrule_violations": []}
                    self.compare_appdynamics(perf_data["appdynamics"]["healthrule_violations"], config_data["promotion_gates"]["warning"], config_data["promotion_gates"]["critical"])
                else:
                    # No health violations, good to go!
                    self.output_json["promotion_gates"]["appdynamics_health"] = True

        # BlazeMeter Module
        if (config_data["blazemeter"]["exists"] == True):
            # Compare BlazeMeter metrics
            # Add BlazeMeter into the output file
            self.output_json["blazemeter"] = {"transactions": []}
            for index, transaction in enumerate(perf_data["blazemeter"]["transactions"]):
                # Add transaction information into the output
                self.output_json["blazemeter"]["transactions"].append({"transaction_id": transaction["transaction_id"], "transaction_name": transaction["transaction_name"]})
                # Average Response Time
                self.compare_blazemeter("response_time_avg", config_data["promotion_gates"]["response_time_avg"], transaction["response_time_avg"], index, operator.lt)
                # Max Response Time
                self.compare_blazemeter("response_time_max", config_data["promotion_gates"]["response_time_max"], transaction["response_time_max"], index, operator.lt)
                # Response Time Standard Deviation
                self.compare_blazemeter("response_time_stdev", config_data["promotion_gates"]["response_time_stdev"], transaction["response_time_stdev"], index, operator.lt)
                # Response Time 90% Line
                self.compare_blazemeter("response_time_tp90", config_data["promotion_gates"]["response_time_tp90"], transaction["response_time_tp90"], index, operator.lt)
                # Response Time 95% Line
                self.compare_blazemeter("response_time_tp95", config_data["promotion_gates"]["response_time_tp95"], transaction["response_time_tp95"], index, operator.lt)
                # Response Time 99% Line
                self.compare_blazemeter("response_time_tp99", config_data["promotion_gates"]["response_time_tp99"], transaction["response_time_tp99"], index, operator.lt)
                # Transaction Rate
                self.compare_blazemeter("transaction_rate", config_data["promotion_gates"]["transaction_rate"], transaction["transaction_rate"], index, operator.gt)

        # Set the overall status in the output JSON file
        self.output_json["promotion_gates"]["passed"] = self.build_status_passed

    def __init__(self):
        """
        Class starting point
        """
        # Build Status
        self.build_status_passed = True

        # Output JSON report data
        # Later appended by the AppDynamics and BlazeMeter processing functions
        self.output_json = {}
