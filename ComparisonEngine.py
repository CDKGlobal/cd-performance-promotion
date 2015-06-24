from BlazeMeter import BlazeMeter
from AppDynamics import AppDynamics

class ComparisonEngine:
    """ Queries the performance tools' APIs and determines if the build passes
        the target requirements. """

    def process_performance_data(self):
        """ Process the data retrieved from the APIs and determine if the code
            passes the user's metrics """
        print("Processing performance data . . .")
        #TODO Process the data
        #TODO Pass or fail the build
        print("\nBuild Status: FAILED")
        #TODO Signal Bamboo to move the build over if the build passes

    def start(self):
        """ Begin retrieving the data and comparing it against the targets """
        # Get the configuration file targets
        #TODO Make a class that reads the configuration information
        #TODO Create a sample configuration file
        # For now, just use variables to compare against

        # Get the load testing data from the BlazeMeter API
        self.blazemeter = BlazeMeter()
        self.blazemeter.get_data()

        # Get the load testing data from the AppDynamics API
        self.appdynamics = AppDynamics()
        self.appdynamics.get_data()

        # Process the data
        self.process_performance_data()
        #print("Processing performance data . . .")
