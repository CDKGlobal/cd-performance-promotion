from configengine import ConfigEngine
from blazemeter import BlazeMeter
from appdynamics import AppDynamics

class ComparisonEngine:
    """
    Queries the performance tools' APIs and determines if the build passes
    the target requirements.
    """

    def process_performance_data(self):
        """
        Processes the data retrieved from the APIs and determine if the code
        passes the user's metrics
        """
        print("Processing performance data . . .")

        # Compare BlazeMeter metrics
        # Average Response Time
        for session, time in self.blazemeter.response_time_avg.items():
            if self.configengine.response_time_avg > time:
                self.build_status_failed = True

        #TODO Add other checks for metrics

        # Final build status check
        if self.build_status_failed:
            print("\nBuild Status: FAILURE")
        else:
            print("\nBuild Status: SUCCESS")

    def get_performance_data(self):
        """
        Begins retrieving the data and comparing it against the targets
        """
        #TODO Look into making this multithreaded, one thread for each api call and closing them all off with join()
        # Get the configuration file information
        self.configengine = ConfigEngine()
        self.configengine.retrieve_config()

        # Build Status
        self.build_status_failed = False

        # Get the load testing data from the BlazeMeter API
        self.blazemeter = BlazeMeter(self.configengine.blazemeter_api_key, self.configengine.blazemeter_test_id)
        self.blazemeter.get_data()

        # Get the load testing data from the AppDynamics API
        self.appdynamics = AppDynamics()
        self.appdynamics.get_data()

        # Process the data
        self.process_performance_data()
        #print("Processing performance data . . .")
