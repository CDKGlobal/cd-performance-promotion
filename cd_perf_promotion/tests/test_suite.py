import unittest
import xmlrunner
import time
import os
import glob
import sys
from cd_perf_promotion.engines.configengine     import ConfigEngine
from cd_perf_promotion.engines.dataengine       import DataEngine
from cd_perf_promotion.engines.comparisonengine import ComparisonEngine

class TestSuite(unittest.TestCase):

    def test_overall_running_time(self):
        start = time.clock()

        ##################################################################################
        # main.py file -- (start)
        ##################################################################################
        print("\n####################################################################\n"
              "Continuous Delivery Performance Promotion Tool\n"
              "CDK Global, LLC\n"
              "####################################################################\n")

        # Grab the configuration information
        configengine = ConfigEngine("config_test_perf.json")
        config_data = configengine.process_config()

        # Grab the performance data
        dataengine = DataEngine()
        perf_data = dataengine.get_data(config_data)

        # Begin evaluating the build
        comparison_engine = ComparisonEngine()
        comparison_engine.process_data(config_data, perf_data)
        comparison_engine.output_results()
        ##################################################################################
        # main.py file -- (end)
        ##################################################################################

        end = time.clock()
        elapsed = end - start

        # Remove the output file -- we wanted it earlier for a more realistic running time
        for filename in glob.glob("cdperfpromodata_*.json"):
            os.remove(filename)

        # Make sure the program doesn't take more than 10 seconds to run
        assert elapsed <= 10


if __name__ == '__main__':
    sys.stdout = open(os.devnull, 'w')
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False, catchbreak=False)
