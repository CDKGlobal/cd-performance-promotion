from cd_perf_promotion.engines.argumentengine   import ArgumentEngine
from cd_perf_promotion.engines.configengine     import ConfigEngine
from cd_perf_promotion.engines.dataengine       import DataEngine
from cd_perf_promotion.engines.comparisonengine import ComparisonEngine
from cd_perf_promotion.engines.outputengine     import OutputEngine

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

    arguments = ArgumentEngine().process_arguments()

    # Grab the configuration information
    configengine = ConfigEngine("config.json", arguments['lr'])
    config_data = configengine.process_config()

    # Grab the performance data
    dataengine = DataEngine()
    perf_data = dataengine.get_data(config_data)

    # Begin evaluating the build
    comparisonengine = ComparisonEngine()
    evaluation = comparisonengine.process_data(config_data, perf_data)

    # Output the data
    outputengine = OutputEngine()
    outputengine.release_judgement(evaluation, arguments['oc'])

    if __name__ == '__main__':
        main()
