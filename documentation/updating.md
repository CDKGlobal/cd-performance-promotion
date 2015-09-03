# Updating the CD Performance Promotion Tool

## Adding Data items
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

#### ElasticSearch/Kibana
If you're outputting your data to ElasticSearch/Kibana at the end of each run, update your mapping and the JSON template file included in the source code.

#### Documentation
1. Add an entry for your data item in the``dictionary.md`` file and save your changes.
2. Success! You're done!

## Adding New Performance Testing Tools
#### Add a New Module
Navigate to the ```cd_perf_promotion/modules``` directory and create a new Python module with the same name as the performance testing tool you are planning to add. The template is as follows:

  ```
  from cd_perf_promotion.modules.perftools import PerfTools

  class NewToolNameHere(PerfTools):
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
          # Inherit methods from parent class "PerfTools"
          PerfTools.__init__(self, "NewToolNameHere")

      def get_data(self):
            """
            Gets the load test data from the API
            """
            # Describe the API query here
            test_summary_url = "urlgoeshere"
            try:
                test_summary_request = requests.get(test_summary_url)
            except:
                self.connection_error() # Inherited from the parent class

            jsondata = []

            # Make sure that the module actually got something back
            if test_summary_request.status_code != 200:
                self.connection_error() # Inherited from the parent class

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
Make sure to add your new module to the ```__init__.py``` file as well.

#### Config Engine
1. Navigate to the ```cd_perf_promotion/engines/configengine``` file and the ```process_config``` function.
2. Add your new tool to the section of code that checks if the tool is defined in the configuration file. It should look something like this:

  ```
  # Variables used to note whether or not these modules were set up in
  # the configuration file. Default to False
  appdynamics_exists = False
  blazemeter_exists = False
  webpagetest_exists = False
  newtoolhere_exists = False

  # Make sure that all of the config sections are there
  if "appdynamics" in config_json:
      appdynamics_exists = True
  if "blazemeter" in config_json:
      blazemeter_exists = True
  if "webpagetest" in config_json:
      webpagetest_exists = True
  if "newtoolhere" in config_json:
      newtoolhere_exists = True
  if "promotion_gates" not in config_json:
      # If the promotion gates aren't in there, there's no use running the program
      self.required_config_error("promotion gates")
  if (appdynamics_exists == False and blazemeter_exists == False and webpagetest_exists == False):
      # If all of the modules don't exist, there's no way to get any data
      self.required_config_error("AppDynamics, BlazeMeter or WebPageTest")
  ```
3. Add a section for your new tool underneath the other tool modules. This should serve as a good template:

  ```
  # NewToolHere Promotion Gates -- Optional
  if (("data_1"     not in config_json["promotion_gates"]) and
      ("data_2"     not in config_json["promotion_gates"]) and
      ("data_3"     not in config_json["promotion_gates"])):
      # NewToolHere configuration inforamtion exists, but none of the metrics do
      # Pretend NewToolHere configuration information doesn't exist either so
      # that we don't waste our time querying the NewToolHere API
      newtoolhere_exists = False
      config_output["newtoolhere"] = {"exists": False}
  else:
      # NewToolHere still exists, put it in the config
      config_output["newtoolhere"]["exists"] = True

      # Make sure that we can put in promotion gates
      if ("promotion_gates" not in config_output):
        config_output["promotion_gates"] = {}

      # Data Item 1
      if ("data_1" in config_json["promotion_gates"]):
        config_output["promotion_gates"]["data_1"] = config_json["promotion_gates"]["data_1"]
      else:
        # 0 means that the user doesn't care about the metric
        config_output["promotion_gates"]["data_1"] = 0

      # Data Item 2
      if ("data_2" in config_json["promotion_gates"]):
        config_output["promotion_gates"]["data_2"] = config_json["promotion_gates"]["data_2"]
      else:
        config_output["promotion_gates"]["data_2"] = 0

      # Data Item 3
      if ("data_3" in config_json["promotion_gates"]):
        config_output["promotion_gates"]["data_3"] = config_json["promotion_gates"]["data_3"]
      else:
        config_output["promotion_gates"]["data_3"] = 0
  else:
    config_output["newtoolhere"]["exists"] = False
  ```
To add on new data items, consider the **Adding Data Items** section of the documentation

#### Data Engine
Navigate to the ```cd_perf_promotion/engines/dataengine.py``` file and the ```get_data`` function. Add a new section of code that processes the data from the module that you created earlier. It should look something like this:

```
# Check if the NewToolHere module was requested by the config
if (config_data["newtoolhere"]["exists"] == True):
  # Start up NewToolHere
  newtoolhere = NewToolHere(config_data["newtoolhere"]["required_field_1"],
                            config_data["newtoolhere"]["required_field_2"],
                            config_data["newtoolhere"]["required_field_3"])
  # NewToolHere data
  all_data = newtoolhere.get_data()
  perf_data["newtoolhere"] = {}
  perf_data["newtoolhere"]["optional_key_here"] = all_data
```

#### Comparison Engine
1. Navigate to the ```cd_perf_promotion/engines/comparisonengine``` file and ```process_data``` function.
2. Add a new section for your module. Here's a template that you can use:

  ```
  # NewToolHere Module
  if (config_data["newtoolhere"]["exists"] == True):
    # Compare NewToolHere metrics
    # Add NewToolHere into the output file
    self.output_json["newtoolhere"] = {"keynamehere": []}

    # NOTE: operator.lt means that the configuration data must be less than the performance data
    # operator.gt means the configuration data must be greater than the performance data
    # Check out https://docs.python.org/3/library/operator.html for information on the list of available operators that you can use

    # Data Item 1
    self.compare_blazemeter("data_1", config_data["promotion_gates"]["data_1"], perf_data["newtoolhere"]["data_1"], index, operator.lt)
    # Data Item 2
    self.compare_blazemeter("data_2", config_data["promotion_gates"]["data_2"], perf_data["newtoolhere"]["data_2"], index, operator.gt)
    # Data Item 3
    self.compare_blazemeter("data_3", config_data["promotion_gates"]["data_3"], perf_data["newtoolhere"]["data_3"], index, operator.lt)
  ```

  If you need to iterate over an array within your JSON data set (like BlazeMeter's transactions), use something like this to handle that instead of just having the straight-up list of data item comparison function calls:

  ```
  # Compare NewToolHere metrics
  # Add NewToolHere into the output file
  self.output_json["newtoolhere"] = {"transactions": []}
  for index, transaction in enumerate(perf_data["toolnamehere"]["transactions"]):
    # Data Item 1
    self.compare_blazemeter("data_1", config_data["promotion_gates"]["data_1], transaction["data_1"], index, operator.lt)
    # Data Item 2
    self.compare_blazemeter("data_2", config_data["promotion_gates"]["data_2"], transaction["data_2"], index, operator.gt)
    # Data Item 3
    self.compare_blazemeter("data_3", config_data["promotion_gates"]["data_3"], transaction["data_3"], index, operator.lt)
  ```

3. Create the function that actually compares the data from the configuration file against the real performance data. Here's an example of what that might look like:

  ```
  def compare_newtoolhere(self, metric_title, target_data, metric_data, transaction_index, operator):
    """
    Performs the comparison between configuration promotion gates and the
    actual newtoolhere test data

    Keyword arguments:
    metric_title      - String title that indicates the data item that is being
                        evaluated
    target_data       - Number that indicates the cutoff point for the specific
                        metric as determined by the user in the config
    metric_data       - The actual performance data number that is compared
                        against
    transaction_index - The index of the transaction in the list of
                        transactions
    operator          - <, >, <=, >, == which is used to compare the real
                        data against the config
    """
    if (target_data > 0):
        # Metric is set in config, begin comparison

        # Add the data to the output file
        self.output_json["newtoolhere"]["transactions"][transaction_index][metric_title] = metric_data

        # Get the "passed" JSON key name ready
        metric_title_passed = metric_title + "_passed"

        # Determine if promotion gate was met
        # Uses the operator module so that the process_performance_data function can determine
        # what operator (<, >, <=, >=, etc.) should be used
        if operator(metric_data, target_data):
            # Success
            if metric_title_passed not in self.output_json["promotion_gates"]:
                # Not mentioned before, add it in
                # Not necessary to make the overall status True again if it's True
                # and if it was False for one transaction the overall status should still be False
                self.output_json["promotion_gates"][metric_title_passed] = True
            # Regardless, add it into the transaction data
            self.output_json["newtoolhere"]["transactions"][transaction_index][metric_title_passed] = True
        else:
            # Failure
            self.output_json["promotion_gates"][metric_title_passed] = False
            self.output_json["newtoolhere"]["transactions"][transaction_index][metric_title_passed] = False
            self.build_status_passed = False
  ```

Unfortunately, it's not that easy to create a catch-all function for comparing data items from tools because the JSON data structure that any one tool uses is completely different from the structure of another tool. As a result, you have to come up with a separate comparison function for each tool. The example in Step 3 was based on the ```compare_blazemeter``` function, but that will not work for all tools. The majority of the BlazeMeter data is located in the ```transactions``` JSON array and the overall structure is a little complex. WebPageTest has two arrays. The point is, all you really need is a function that can be called by the ```process_data``` function, saves the comparison information as a new key in the output JSON file, is fairly modular, and easy to maintain. If you need help, look at the other comparison functions in the file to see how they handle things.

#### ElasticSearch/Kibana
If you're outputting your data to ElasticSearch/Kibana at the end of each run, update your mapping and the JSON template file included in the source code.

You're done!
