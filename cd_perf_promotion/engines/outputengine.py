import time
import sys
import json

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
        filename = "cdperfpromoevaluation_{0}.json".format(time.strftime("%m%d%y_%H%M%S"))
        try:
            with open(filename, "w") as jsonoutput:
                json.dump(evaluation, jsonoutput, indent = 4, sort_keys = True)
        except:
            print("ERROR: Unable to output results file")
            sys.exit(1)

        # Let the user know where they can get all of the results
        print("\nPlease see {0} for more information".format(filename))

    def release_judgement(self, evaluation, arg_oc):
        """
        Handle the results output
        """
        # Write the data to the file
        self.output_file(evaluation)

        # Check if we need to print it out to the console as well
        if (arg_oc):
            # Print full data to the console
            self.print_results_long(evaluation)

        # Let the user know the final verdict
        self.print_results_short(evaluation['promotion_gates']['passed'])
