#Continuous Delivery Performance Promotion

##Overview
This is a Python program that is used to retrieve data from load testing and server monitoring tools like BlazeMeter and AppDynamics, evaluate the metrics against predefined promotion gates, and promote builds if they meet the promotion gates.

##Setting up Promotion Gates
####Configuration File
You can set the promotion gates by altering the ``config.json`` file. A sample configuration file can be found at ``config.json.sample``. Please note that the .sample file extension should be removed from the actual configuration file in order to actually use it.

You do not have to use all of the available promotion gate metrics and the order of the keys does not matter. The following table lists the available JSON configuation keys and whether or not they are required.

| Data Item                     | Type    | Parent                 | Description                                                                                                 | Required |
| :---------------------------- | :-----  | :--------------------- | :---------------------------------------------------------------------------------------------------------- | :------: |
| ``appdynamics``               | Object  | N/A                    | Contains all of the AppDynamics specific information                                                        | Yes*     |
| ``username``                  | String  | appdynamics            | Appdynamics username in the format of username@account                                                      | Yes      |
| ``password``                  | String  | appdynamics            | Appdynamics password                                                                                        | Yes      |
| ``load_test_length_min``      | Number  | appdynamics            | Length of the load test period (X number of minutes before current time)                                    | Yes**    |
| ``load_test_length_start_ms`` | Number  | appdynamics            | Time that you want to begin monitoring at. Format is milliseconds after Unix epoch time (January 1st, 1970) | Yes**    |
| ``load_test_length_end_ms``   | Number  | appdynamics            | Time that you want to monitoring to stop. Format is milliseconds after Unix epoch time (January 1st, 1970)  | Yes**    |
| ``blazemeter``                | Object  | N/A                    | Contains all of the BlazeMeter specific information                                                         | Yes*     |
| ``api``                       | String  | blazemeter             | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``test_id``                   | String  | blazemeter             | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``webpagetest``               | Object  | N/A                    | Contains all of the WebPageTest specific information                                                        | Yes*     |
| ``promotion_gates``           | Object  | N/A                    | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``response_time_avg``         | Number  | promotion_gates        | Average response time (under BlazeMeter load)                                                               | No       |
| ``response_time_max``         | Number  | promotion_gates        | Maximum response time (under BlazeMeter load)                                                               | No       |
| ``response_time_stdev``       | Number  | promotion_gates        | Response time standard deviation (under BlazeMeter load)                                                    | No       |
| ``response_time_tp90``        | Number  | promotion_gates        | 90% line -- 90% of requests were handled in this amount of time (under BlazeMeter load)                     | No       |
| ``response_time_tp95``        | Number  | promotion_gates        | 95% line -- 95% of requests were handled in this amount of time (under BlazeMeter load)                     | No       |
| ``response_time_tp99``        | Number  | promotion_gates        | 99% line -- 99% of requests were handled in this amount of time (under BlazeMeter load)                     | No       |
| ``latency_avg``               | Number  | promotion_gates        | Average latency (under BlazeMeter load)                                                                     | No       |
| ``latency_max``               | Number  | promotion_gates        | Maximum latency (under BlazeMeter load)                                                                     | No       |
| ``latency_stdev``             | Number  | promotion_gates        | Latency standard deviation (under BlazeMeter load)                                                          | No       |
| ``bandwidth_avg``             | Number  | promotion_gates        | Average Bandwidth -- Bytes/Second (under BlazeMeter load)                                                   | No       |
| ``transaction_rate``          | Number  | promotion_gates        | Average Throughput (AKA Transaction Rate) -- Hits/Second (under BlazeMeter load)                            | No       |
| ``warning``                   | Boolean | promotion_gates        | Indicates if AppDynamics health rule violations with a status of ``WARNING`` matter                         | No       |
| ``critical``                  | Boolean | promotion_gates        | Indicates if AppDynamics health rule violations with a status of ``CRITICAL`` matter                        | No       |
| ``first_view``                | Object  | promotion_gates        | Container for WebPageTest metrics for the first time a page is loaded                                       | Yes***   |
| ``repeat_view``               | Object  | promotion_gates        | Container for WebPageTest metrics for the second time a page is loaded                                      | Yes***   |
| ``speed_index``               | Number  | first_view/repeat_view | WebPageTest Speed Index, the average time (ms) at which the visible parts of the page are displayed         | No       |
| ``first_paint``               | Number  | first_view/repeat_view | Time to first paint (ms)                                                                                    | No       |
| ``first_byte``                | Number  | first_view/repeat_view | Time to first byte (ms)                                                                                     | No       |
| ``fully_loaded``              | Number  | first_view/repeat_view | Time to page fully loaded (ms)                                                                              | No       |
| ``visual_complete``           | Number  | first_view/repeat_view | Time to when the page looks like it has fully loaded (ms)                                                   | No       |

\*Required if you would like to gather data from the tool, otherwise not required
\*\*Either ``load_test_length_min`` or both ``load_test_length_start_ms`` and ``load_test_length_end_ms`` must be declared
\*\*\*Required if you want to use any WebPageTest data

##Installation
1. Download the program and navigate to the download directory using the CLI
2. Navigate into the ``cd_perf_promotion`` directory
3. run ``python setup.py install``. The program is installed.

##Starting the Program
1. Copy and paste the ``config.json.sample`` file that ships with the program into your desired directory.
2. Rename it ``config.json`` and modify its contents to fit your continuous delivery needs.
3. Open the CLI and run ``cdperfpromotion`` in the same directory as your ``config.json`` file. You also have the option of running ``cdperfpromotion -lr www.URLGOESHERE.com`` to have the program look for a config file at the inputted address. For example, to get your configuration file from Atlassian Stash, use something like ``cdperfpromotion -lr http://username:password@stash.ds.adp.com/projects/PROJECTKEYHERE/repos/REPOSLUGHERE/browse/CONFIGFILEHERE?raw``.
4. A JSON output file will be created in the same directory. The name of the file is specified by the program at the end of its operation. Open it to learn more about how your build performed.

##Evaluating the Results
The ``promotion_gates`` JSON object in the output file contains all of the high-level data on whether or not the build can move on to the next stage (JSON key ``passed``) and the pass/fail status for each promotion gate that was previously defined in ``config.json`` file. All of the detailed load testing information (on a transaction basis) can be found in the ``blazemeter`` JSON object, all of the server information (during the load testing timeframe) can be found in the ``appdynamics`` JSON object, and all of the front-end performance data can be found in the ``webpagetest`` JSON object. This structure helps users quickly identify where their application isn't performing well.

##Program Structure
| Item                                  | Type   | Parent   | Description                                                                                                                              |
| :------------------------------------ | :----- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| ``documentation``                     | Folder | N/A      | Contains all of the documentation for the tool                                                                                           |
| ``engines``                           | Folder | N/A      | Contains all of the data gathering and processing code                                                                                   |
| ``configengine.py``                   | File   | engines  | Retrieves the data from the config.json configuration file                                                                               |
| ``dataengine.py``                     | File   | engines  | Retrieves the data from the config.json configuration file                                                                               |
| ``comparionsengine.py``               | File   | engines  | Retrieves the data from the config.json configuration file                                                                               |
| ``modules``                           | Folder | N/A      | Contains all of the modules (AppDynamics, BlazeMeter, etc.)                                                                              |
| ``appdynamics.py``                    | File   | modules  | AppDynamics module that gets all of the necessary metrics from the AppDynamics API                                                       |
| ``blazemeter.py``                     | File   | modules  | BlazeMeter module that gets all of the necessary metrics from the BlazeMeter API                                                         |
| ``webpagetest.py``                    | File   | modules  | WebPageTest module that gets all of the necessary metrics form the WebPageTest API                                                       |
| ``output``                            | Folder | N/A      | Contains all of the output JSON files                                                                                                    |
| ``cdperfpromo_DATE_TIME.json.sample`` | File   | output   | Sample output file                                                                                                                       |
| ``packages``                          | Folder | N/A      | Contains all of the libraries                                                                                                            |
| ``requests``                          | Folder | packages | Contains the requests library, which is used to query the various APIs                                                                   |
| ``xmltodict``                         | Folder | packages | Contains the xmltodict library, which is used to convert XML to JSON (silly WebPageTest...)                                              |
| ``__init__.py``                       | File   | N/A      | Used to indicate the packages in the program                                                                                             |
| ``__main__.py``                       | File   | N/A      | Used to run the program                                                                                                                  |
| ``comparisonengine.py``               | File   | N/A      | Retrieves the data from all of the performance tool modules and compares them against the promotion gate criteria defined in config.json |
| ``config.json``                       | File   | N/A      | Configuration file that is used to define the promotion gate criteria and performance tool information (API keys, test IDs, etc.)        |
| ``config.json.sample``                | File   | N/A      | Sample/template configuration file                                                                                                       |

##Extending the Program
####Tips for Adding a new Data Source
 * Follow the examples of BlazeMeter and AppDynamics
 * ``config.json``         - Add a new JSON object for the new tool and the necessary data items in the ``promotion_gates`` JSON objects
 * ``config.json.sample``  - Make the same changes that you did in the ``config.json`` file
 * ``configengine.py``     - Add checks and save the data item to the ``config_output`` file
 * ``yourtoolnamehere.py`` - Implement the actual API querying here
 * ``dataengine.py``       - Only do data gathering and data preparation here
 * ``comparisonengine.py`` - Only do data comparison and output here

####Tips for Adding a new Data Item
 * Follow the examples of BlazeMeter and AppDynamics
 * Basically go through the same steps as adding a new data source, but just add additional checks and other statements instead of creating whole new files
 * AppDynamics has an interesting example of a data item that cannot be used when another data item is in use that may be worth checking out (``load_test_length_min`` and ``load_test_start_ms``/``load_test_end_ms``)
