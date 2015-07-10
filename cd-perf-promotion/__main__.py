from configengine     import ConfigEngine
from dataengine       import DataEngine
from comparisonengine import ComparisonEngine

class Main:
  """
  Continuous Delivery Main class
  """

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
    configengine = ConfigEngine()
    config_data = configengine.process_config()

    # Grab the performance data
    dataengine = DataEngine()
    perf_data = dataengine.get_data(config_data)

    # Begin evaluating the build
    comparison_engine = ComparisonEngine()
    comparison_engine.process_data(config_data, perf_data)
    comparison_engine.output_results()

  if __name__ == '__main__':
    main()
