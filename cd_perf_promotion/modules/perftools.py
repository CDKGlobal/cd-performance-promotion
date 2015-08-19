import sys

class PerfTools:
    """
    Parent class for all of the performance testing/monitoring tools
    """
    def __init__(self, tool_name):
        self.tool_name = tool_name

    def connection_error(self):
        # User likely lost their internet connection or used incorrect credentials
        print("ERROR: Unable to query {0} API".format(self.tool_name))
        sys.exit(1)
