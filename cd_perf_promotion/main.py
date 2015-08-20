from cd_perf_promotion.engines.configengine     import ConfigEngine
from cd_perf_promotion.engines.dataengine       import DataEngine
from cd_perf_promotion.engines.comparisonengine import ComparisonEngine
import sys

def main():
    """
    Main function
    Prints and introduction statement and starts the comparison engine
    """
    # Print the introduction message
    print("\n####################################################################\n"
          "Continuous Delivery Performance Promotion Tool\n"
          "CDK Global, LLC\n"
          "####################################################################\n")

    # Grab the configuration information
    configengine = ConfigEngine("config.json")
    config_data = configengine.process_config()

    # Grab the performance data
    dataengine = DataEngine()
    perf_data = dataengine.get_data(config_data)

    # Begin evaluating the build
    comparison_engine = ComparisonEngine()
    comparison_engine.process_data(config_data, perf_data)
    build_passed = comparison_engine.output_results()
    if (build_passed == True):
        print("\nBuild Status: SUCCESS")
        sys.exit(0)
    else:
        print("\nBuild Status: FAILURE")
        sys.exit(1)

    if __name__ == '__main__':
        main()
