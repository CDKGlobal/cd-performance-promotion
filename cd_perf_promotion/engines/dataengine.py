from cd_perf_promotion.modules.appdynamics import AppDynamics
from cd_perf_promotion.modules.blazemeter import BlazeMeter
from cd_perf_promotion.modules.webpagetest import WebPageTest
from datetime import datetime
from datetime import timedelta

class DataEngine:
    """
    Queries the Module APIs and passes the data along to the comparison engine
    """
    def calculate_time(self, load_test_length_min):
        """
        Figure out the start-time and end-time parameters for our API request
        We need the time in milliseconds, but that time has to be the Unix
        epoch time -- Time is hard

        Keyword arguments:
        load_test_length_min = The duration of the load test time frame in ms
                               (Unix epoch time)
        """
        # Time starts on January 1st, 1970 according to Unix
        epoch_time = datetime(1970, 1, 1)

        # Using this timestamp to ensure that we're working off of the same time
        # Works off of the system time zone, so as long as this is run on the
        # timezone as AppDynamics, we should be good to go
        timestamp = datetime.now()

        # Have to round because the API doesn't like partial milliseconds
        # start_time is current time - the load test window length the user gave us
        end_time = round((timestamp - epoch_time).total_seconds() * 1000)
        start_time = round(end_time - (load_test_length_min * 1000))

        # Send the times back
        return {"load_test_start_ms": start_time, "load_test_end_ms": end_time}

    def get_data(self, config_data):
        """
        Retrieves the data for later passing down to the comparison engine

        Keyword arguments:
        config_data - dictionary that contains all of the information retrieved
                      by the configuration engine
        """
        # Output dictionary that has all of the data
        perf_data = {}

        # Check if the AppDynamics module was requested by the config
        if (config_data["appdynamics"]["exists"] == True):
            # Get the time stuff setup if the user hasn't specified a start and end time
            if ("load_test_length" in config_data["appdynamics"]):
                test_times = self.calculate_time(config_data["appdynamics"]["load_test_length"])
                config_data["appdynamics"]["load_test_start_ms"] = test_times["load_test_start_ms"]
                config_data["appdynamics"]["load_test_end_ms"] = test_times["load_test_end_ms"]

            # Start up AppDynamics
            appdynamics = AppDynamics(config_data["appdynamics"]["username"],
                                      config_data["appdynamics"]["password"],
                                      config_data["appdynamics"]["application_name"],
                                      config_data["appdynamics"]["load_test_start_ms"],
                                      config_data["appdynamics"]["load_test_end_ms"])
            # AppDynamics data
            healthrule_violations = appdynamics.get_data()
            perf_data["appdynamics"] = {}
            perf_data["appdynamics"]["healthrule_violations"] = healthrule_violations

        # Check if the BlazeMeter module was requested by the config
        if (config_data["blazemeter"]["exists"] == True):
            # Start up BlazeMeter
            blazemeter = BlazeMeter(config_data["blazemeter"]["api_key"],
                                    config_data["blazemeter"]["test_id"],
                                    config_data["blazemeter"]["test_length_sec"])
            # BlazeMeter data
            transactions = blazemeter.get_data()
            perf_data["blazemeter"] = {}
            perf_data["blazemeter"]["transactions"] = transactions

        # Check if the WebPageTest module was requested by the config
        if (config_data["webpagetest"]["exists"] == True):
            # Start up WebPageTest
            webpagetest = WebPageTest(config_data["webpagetest"]["url"], config_data["webpagetest"]["location"], config_data["webpagetest"]["api"])
            alldata = webpagetest.get_data()
            perf_data["webpagetest"] = { "average": { "first_view": alldata["response"]["data"]["average"]["firstView"], "repeat_view": alldata["response"]["data"]["average"]["repeatView"] }, "runs": [] }
            for run in alldata["response"]["data"]["run"]:
                perf_data["webpagetest"]["runs"].append({"run_id": run["id"], "first_view": run["firstView"], "repeat_view": run["repeatView"]})

        return perf_data
