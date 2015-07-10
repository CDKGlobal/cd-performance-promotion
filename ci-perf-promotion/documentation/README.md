#Continuous Delivery Performance Promotion

##Overview
This is a Python program that is used to retrieve data from load testing and server monitoring tools like BlazeMeter and AppDynamics, evaluate the metrics against predefined promotion gates, and promote builds if they meet the promotion gates.

##Setting up Promotion Gates
####Configuration File
You can set the promotion gates by altering the config.json file. A sample configuration file can be found at config.json.example. Please note that the .example file extension should be removed from the actual configuration file.

You do not have to use all of the available promotion gate metrics and the order of the keys does not matter. The following table lists the available JSON configuation keys and whether or not they are required.

| Data Item                     | Type   | Parent          | Description                                                                                                 | Required |
| :---------------------------- | :----- | :-------------- | :---------------------------------------------------------------------------------------------------------- | :------: |
| ``appdynamics``               | Object | N/A             | Contains all of the AppDynamics specific information                                                        | Yes      |
| ``username``                  | String | appdynamics     | Appdynamics username in the format of username@account                                                      | Yes      |
| ``password``                  | String | appdynamics     | Appdynamics password                                                                                        | Yes      |
| ``load_test_length_min``      | Number | appdynamics     | Length of the load test period (X number of minutes before current time)                                    | Yes*     |
| ``load_test_length_start_ms`` | Number | appdynamics     | Time that you want to begin monitoring at. Format is milliseconds after Unix epoch time (January 1st, 1970) | Yes*     |
| ``load_test_length_end_ms``   | Number | appdynamics     | Time that you want to monitoring to stop. Format is milliseconds after Unix epoch time (January 1st, 1970)  | Yes*     |
| ``blazemeter``                | Object | N/A             | Contains all of the BlazeMeter specific information                                                         | Yes      |
| ``api``                       | String | blazemeter      | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``test_id``                   | String | blazemeter      | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``promotion_gates``           | Object | N/A             | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``response_time_avg``         | Number | promotion_gates | Average response time                                                                                       | No       |
| ``response_time_max``         | Number | promotion_gates | Maximum response time                                                                                       | No       |
| ``response_time_stdev``       | Number | promotion_gates | Response time standard deviation                                                                            | No       |
| ``response_time_tp90``        | Number | promotion_gates | 90% line -- 90% of requests were handled in this amount of time                                             | No       |
| ``response_time_tp95``        | Number | promotion_gates | 95% line -- 95% of requests were handled in this amount of time                                             | No       |
| ``response_time_tp99``        | Number | promotion_gates | 99% line -- 99% of requests were handled in this amount of time                                             | No       |

\* Either ``load_test_length_min`` or both ``load_test_length_start_ms`` and ``load_test_length_end_ms`` must be declared

##Starting the Program
1. Navigate to the directory containing the ``__main__.py`` file
2. Run ``python __main__.py``
3. Open the output JSON file specified by the program for testing results.

##Evaluating the Results
The ``promotion_gates`` JSON object in the output file contains all of the high-level data on whether or not the build can move on to the next stage (JSON key ``passed``) and the pass/fail status for each promotion gate that was previously defined in ``config.json`` file. All of the detailed information on a transaction basis can be found in the ``blazemeter`` JSON object, allowing users to identify which transactions are running into performance issues. If the ``response_time_avg`` promotion gate criteria is marked as failing in the ``promotion_gate`` object, users can look at the transactions listed in ``blazemeter`` object to find out which one caused the build to fail.

##Program Structure
| Item                       | Type   | Parent          | Description                                                                                                                              |
| :------------------------- | :----- | :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| ``documentation``          | Folder | N/A             | Contains all of the documentation for the tool                                                                                           |
| ``packages``               | Folder | N/A             | Contains all of the libraries                                                                                                            |
| ``requests``               | Folder | packages        | Contains the requests library, which is used to query the various APIs                                                                   |
| ``__init__.py``            | File   | N/A             | Used to indicate the packages in the program                                                                                             |
| ``__main__.py``            | File   | N/A             | Used to run the program                                                                                                                  |
| ``appdynamics.py``         | File   | N/A             | AppDynamics module that gets all of the necessary metrics from the AppDynamics API                                                       |
| ``blazemeter.py``          | File   | N/A             | BlazeMeter module that gets all of the necessary metrics from the BlazeMeter API                                                         |
| ``comparisonengine.py``    | File   | N/A             | Retrieves the data from all of the performance tool modules and compares them against the promotion gate criteria defined in config.json |
| ``config.json``            | File   | N/A             | Configuration file that is used to define the promotion gate criteria and performance tool information (API keys, test IDs, etc.)        |
| ``configengine.py``        | File   | N/A             | Retrieves the data from the config.json configuration file                                                                               |
