from comparisonengine import ComparisonEngine

class Main:
  """
  Continuous Integration main class
  """

  def main():
    """
    Main function
    Prints and introduction statement and starts the comparison engine
    """
    # Print the introduction message
    print("\n######################################################\n"
          "Continuous Integration Performance Promotion Tool\n"
          "CDK Global, LLC\n"
          "######################################################\n")

    # Begin evaluating the build
    comparison_engine = ComparisonEngine()
    comparison_engine.start()

  if __name__ == '__main__':
    main()
