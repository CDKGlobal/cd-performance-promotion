# Updating the CD Performance Promotion Tool

## Adding Additional Data items
#### Config Engine
1. Go into the ```cd_perf_promotion/engines/configengine.py``` and navigate to the tool section your new data item belongs to.
2. If your data item is a required data item used to perform the API calls, add another ```else if``` statement to the required section (usually titled, ```<TOOL NAME HERE> Configuration Information -- Required```).
3. If your data item is a promotion gate (which are always optional), follow the steps below:
  1. Add another line to the ``if`` statement directly below the optional section (usually titled, ```# <TOOL NAME HERE> Promotion Gates -- Optional```) for your specific data item. This new line should look something like this:

    ```
    # <TOOL NAME HERE> Promotion Gates -- Optional
    if (("data_1"         not in config_json["promotion_gates"]) and
        ("data_2"         not in config_json["promotion_gates"]) and
        ("data_3"         not in config_json["promotion_gates"]) and
        ("your_data_item" not in config_json["promotion_gates"]) and
        ("data_4"         not in config_json["promotion_gates"])):
    ```
  2. Add another section the ``else`` statement of the previous mentioned ``if`` statement for your specific data item. It should look something like this:

    ```
    # Your Data Item Here
    if ("data_item" in config_json["promotion_gates"]):
      config_output["promotion_gates"]["data_item"] = config_json["promotion_gates"]["data_item"]
    else:
      config_output["promotion_gates"]["data_item"] = 0
    ```
4. Save the file. Your configuration engine is now able to pull the new data from your ```config.json``` file.

#### Data Engine
1. If your data item is required to gather data from the performance tools (API-based information), navigate to the ```get_data``` function in ```cd_perf_promotion/engine/dataengine.py```. Otherwise, move on to the next section!
2. Navigate to your tool's section (usually titled ```# Check if the <TOOL NAME HERE> module was requested by the config``` ) and add another parameter to the call to instantiate your tool's module so that the call looks something like this:

  ```
  # Start up <TOOL NAME HERE>
  tool_name_here = Tool_Module_Name(config_data["tool_name_here"]["data_1"],
                                    config_data["tool_name_here"]["data_2"],
                                    config_data["tool_name_here"]["new_data_item_here"])
  ```
3. Save the file. Your data item's module is now able to access your required data item.

#### Your Data Item's Tool Module
1. Go into the ```cd_perf_promotion/modules/yourtoolnamehere.py``` file.
2. If your data item is required to perform API calls, follow the steps below:
  1. Add a new parameter to the ``__init__`` function for your data item
  2. Add a new global variable line in the ``__init__`` function so that it looks something like this:

    ```
    # Test configuration information
    self.data_1 = param_1
    self.data_2 = param_2
    self.your_data_item = your_data_item_param
    ```
  3. Go into the ```get_data``` function and add your data item to the HTTP request. This can take shape in many different forms, so just follow along with what your tool's module already does.
3. If your data item is a promotion gate, follow the steps below:
  1. Coming soon!
4. Save the file. Your tool's module is now able to request the proper data.

#### Comparison Engine
1. If your new data item is a promotion gate, navigate to the ```process_data``` function within ```cd_perf_promotion/engines/comparisonengine.py``. If not, skip down to the next section.
2. Navigate down to the tool section that your data item belongs to and add a single function call to the ```self.compare_yourtoolnamehere()``` function so that it looks something like this:

   ```
   # ToolNameHere Module
        if (config_data["toolnamehere"]["exists"] == True):
            # Compare ToolNameHere metrics
            for index, transaction in enumerate(perf_data["toolnamehere"]["transactions"]):
                # Data 1
                self.compare_toolnamehere("data_1", config_data["promotion_gates"]["data_1"], transaction["data_1"], index, operator.gt)
                # Data 2
                self.compare_toolnamehere("data_2", config_data["promotion_gates"]["data_2"], transaction["data_2"], index, operator.gt)
                # Your Data Item
                self.compare_toolnamehere("your_data_item", config_data["promotion_gates"]["your_data_item"], transaction["your_data_item"], index, operator.lt)
    ```
3. Save the file. The application is now able to evaluate your data item against the configuration file.

#### Documentation
1. Add an entry for your data item in the``dictionary.md`` file and save your changes.
2. Success! You're done!

## Adding New Performance Testing Tools
#### Add a New Module
Navigate to the ```cd_perf_promotion/modules``` directory and create a new Python module with the same name as the performance testing tool you are planning to add. The template is as follows:

  ```
  class NewToolNameHere:
      """
      Handles all of the ToolNameHere API querying/data gathering
      """

      def __init__(self, api_param_1, api_param_2):
          """
          Documentation Header Goes Here

          Keyword arguments:
          api_param_1 - Explanation Goes Here
          api_param_2 - Explanation Goes Here
          """
          # Test configuration information
          self.api_param_1 = api_param_1
          self.api_param_2 = api_param_2

      def connection_error(self):
          # User likely lost their internet connection or used incorrect credentials
          print("ERROR: Unable to query TooolNameHere API")
          sys.exit(1)

      def get_data(self):
            """
            Gets the load test data from the API
            """
            # Describe the API query here
            test_summary_url = "urlgoeshere"
            try:
                test_summary_request = requests.get(test_summary_url)
            except:
                self.connection_error()

            jsondata = []

            # Make sure that the module actually got something back
            if test_summary_request.status_code != 200:
                self.connection_error()

            # Side Note -- This is looping over all of the "transactions" the data is retrieving,
            # but if you don't need that, just return all of the JSON data that you would ever
            # want to evaluate. Grabbing data is cheap in terms of performance, so this module
            # just grabs all of the data that the program supports in terms of data evaluation
            # and lets the configuration engine grab what it needs to evaluate
            for transaction in test_summary_request.json()["jsonkeyhere"]["anotherjsonkey"]:
                jsondata.append({
                        "newkeyname_1": transaction["keyname_1"],
                        "newkeyname_2": transaction["keyname_2"],
                        "newkeyname_3": transaction["keyname_3"],
                        "newkeyname_4": transaction["keyname_4"]
                    })

            # Notify the user that the ToolNameHere data has grabbed
            print("Retrieved ToolNameHere data")

            return jsondata
    ```

#### Config Engine
Coming Soon!

#### Data Engine
Coming Soon!

#### Comparison Engine
Coming Soon!
