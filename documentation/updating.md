# Updating the CD Performance Promotion Tool

## Adding Additional Data items
#### Config Engine
1. Go into the ```cd_perf_promotion/engines/configengine.py``` and navigate to the tool section your new data item belongs to.
2. If your data item is a required data item used to perform the API calls, add another ```else if``` statement to the required section (usually titled, ```<TOOL NAME HERE> Configuration Information -- Required```).
3. If your data item is an promotion gate (which are always optional), follow the steps below:
  1. Add another ```and``` line specific to your data item to the ``if`` statement directly below the optional section (usually titled, ```# <TOOL NAME HERE> Promotion Gates -- Optional```). This new line should look something like this:

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
1. If your data item is required to perform the API calls, navigate to the ```get_data``` function in ```cd_perf_promotion/engine/dataengine.py```. Otherwise, move on to the next section!
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

## Adding New Performance Testing Tools
Coming soon!
