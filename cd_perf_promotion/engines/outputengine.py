from time import gmtime, strftime
import time
import sys
import json
import requests

class OutputEngine:
    """
    Handles the output of all of the data
    """

    def print_results_short(self, build_passed):
        """
        Print out the status of the build
        """
        if (build_passed == True):
            print("\nBuild Status: SUCCESS")
            sys.exit(0)
        else:
            print("\nBuild Status: FAILURE")
            sys.exit(1)

    def print_results_long(self, evaluation):
        """
        Print out all of the data to the console
        """
        print("\nData Output:\n")
        print(json.dumps(evaluation, indent = 4, sort_keys = True))

    def output_file(self, evaluation):
        """
        Write all of the data to an output file
        """
        filename = "cdperfeval_{0}.json".format(time.strftime("%m%d%y_%H%M%S"))
        try:
            print("Saving data to file... ({0})".format(filename))
            with open(filename, "w") as jsonoutput:
                json.dump(evaluation, jsonoutput, indent = 4, sort_keys = True)
        except:
            print("ERROR: Unable to save results file")
            sys.exit(1)

        print("Data saved to file")

    def output_kibana(self, evaluation, server, index):
        """
        Send the data to Kibana/ElasticSearch
        """
        print("Sending data to ElasticSearch/Kibana...")

        # Singular time record used for ElasticSearch
        timestamp = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

        # Prepare the data for ElasticSearch consumption
        if ("appdynamics" in evaluation):
            appdynamics = evaluation["appdynamics"]
        if ("blazemeter" in evaluation):
            blazemeter = evaluation["blazemeter"]
        if ("webpagetest" in evaluation):
            webpagetest = evaluation["webpagetest"]
        if ("promotion_gates" in evaluation): # Should always exist, but just in case
            promotion_gates = evaluation["promotion_gates"]

        try:
            # AppDynamics
            if ("appdynamics" in evaluation):
                for idx, violation in enumerate(appdynamics["healthrule_violations"]):
                    appdynamics["healthrule_violations"][idx]["DateTime"] = timestamp
                    requests.post("{0}/{1}/appdynamics.healthrule_violations".format(server, index), data=json.dumps(appdynamics["healthrule_violations"][idx]))
            # BlazeMeter
            if ("blazemeter" in evaluation):
                for idx, transaction in enumerate(blazemeter["transactions"]):
                    blazemeter["transactions"][idx]["DateTime"] = timestamp
                    requests.post("{0}/{1}/blazemeter.transactions".format(server, index), data=json.dumps(blazemeter["transactions"][idx]))
            # WebPageTest
            if ("webpagetest" in evaluation):
                for idx, transaction in enumerate(webpagetest["runs"]):
                    webpagetest["runs"][idx]["first_view"]["DateTime"] = timestamp
                    webpagetest["runs"][idx]["repeat_view"]["DateTime"] = timestamp
                    requests.post("{0}/{1}/webpagetest.first_view".format(server, index), data=json.dumps(webpagetest["runs"][idx]["first_view"]))
                    requests.post("{0}/{1}/webpagetest.repeat_view".format(server, index), data=json.dumps(webpagetest["runs"][idx]["repeat_view"]))
            # Promotion Gates
            if ("promotion_gates" in evaluation):
                promotion_gates["Date"] = timestamp
                requests.post("{0}/{1}/promotion_gates".format(server, index), data=json.dumps(promotion_gates))
        except:
            print("ERROR: Unable to output the results to ElasticSearch/Kibana")
            sys.exit(1)

        print("Data sent to Kibana")

    def release_judgement(self, evaluation, arg_oc, elastic_kibana):
        """
        Handle the results output -- Basically serve as the switchboard for the output engine
        """
        # Write the data to the file
        filename = self.output_file(evaluation)

        # Check if we need to output the data to Kibana
        if (elastic_kibana["exists"] == True):
            # Send it over to Kibana/ElasticSearch
            self.output_kibana(evaluation, elastic_kibana["elastic_server"], elastic_kibana["index"])

        # Check if we need to print it out to the console as well
        if (arg_oc):
            # Print full data to the console
            self.print_results_long(evaluation)

        # Let the user know the final verdict
        self.print_results_short(evaluation['promotion_gates']['passed'])
