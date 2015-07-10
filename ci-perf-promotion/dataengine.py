from appdynamics import AppDynamics
from blazemeter import BlazeMeter
import json

class DataEngine:
    """
    Queries the Module APIs and passes the data along to the comparison engine
    """
    def get_data(self, config_data):
        """
        Retrieves the data for later passing down to the comparison engine

        Keyword arguments:
        config_data - dictionary that contains all of the information retrieved
                      by the configuration engine
        """
        #TODO Look into making this multithreaded, one thread for each api call and closing them all off with join()

        # Output dictionary that has all of the data
        perf_data = {}

        # Check if the AppDynamics module was requested by the config
        if (config_data["appdynamics"]["exists"] == True):
            appdynamics = AppDynamics(config_data["appdynamics"]["username"],
                                      config_data["appdynamics"]["password"],
                                      config_data["appdynamics"]["application_name"],
                                      config_data["appdynamics"]["load_test_length"])
            healthrule_violations = appdynamics.get_data()
            perf_data["appdynamics"] = {}
            perf_data["appdynamics"]["healthrule_violations"] = healthrule_violations

        # Check if the BlazeMeter module was requested by the config
        if (config_data["blazemeter"]["exists"] == True):
            blazemeter = BlazeMeter(config_data["blazemeter"]["api_key"],
                                    config_data["blazemeter"]["test_id"])
            transactions = blazemeter.get_data()
            perf_data["blazemeter"] = {}
            perf_data["blazemeter"]["transactions"] = transactions

        return perf_data
