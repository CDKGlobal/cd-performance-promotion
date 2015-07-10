#Continuous Delivery Performance Promotion (Advanced)

##Program Structure
| Item                           | Type   | Parent   | Description                                                                                                                              |
| :----------------------------- | :----- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| ``documentation``              | Folder | N/A      | Contains all of the documentation for the tool                                                                                           |
| ``engines``                    | Folder | N/A      | Contains all of the data gathering and processing code                                                                                   |
| ``configengine.py``            | File   | engines  | Retrieves the data from the config.json configuration file                                                                               |
| ``dataengine.py``              | File   | engines  | Retrieves the data from the config.json configuration file                                                                               |
| ``comparionsengine.py``        | File   | engines  | Retrieves the data from the config.json configuration file                                                                               |
| ``modules``                    | Folder | N/A      | Contains all of the modules (AppDynamics, BlazeMeter, etc.)                                                                              |
| ``appdynamics.py``             | File   | modules  | AppDynamics module that gets all of the necessary metrics from the AppDynamics API                                                       |
| ``blazemeter.py``              | File   | modules  | BlazeMeter module that gets all of the necessary metrics from the BlazeMeter API                                                         |
| ``output``                     | Folder | N/A      | Contains all of the output JSON files                                                                                                    |
| ``cdperfpromo_DATE_TIME.json`` | File   | output   | Sample output file                                                                                                                       |
| ``packages``                   | Folder | N/A      | Contains all of the libraries                                                                                                            |
| ``requests``                   | Folder | packages | Contains the requests library, which is used to query the various APIs                                                                   |
| ``__init__.py``                | File   | N/A      | Used to indicate the packages in the program                                                                                             |
| ``__main__.py``                | File   | N/A      | Used to run the program                                                                                                                  |
| ``comparisonengine.py``        | File   | N/A      | Retrieves the data from all of the performance tool modules and compares them against the promotion gate criteria defined in config.json |
| ``config.json``                | File   | N/A      | Configuration file that is used to define the promotion gate criteria and performance tool information (API keys, test IDs, etc.)        |
| ``config.json.sample``         | File   | N/A      | Sample/template configuration file                                                                                                       |

##Extending the Program
####Tips for Adding a new Module (Tool)
* Follow the examples of BlazeMeter and AppDynamics
* Make sure that you are modifying the following files. If you aren't modifying these files when you're adding a new module, you're probably doing it wrong:
  * ``config.json``         - Add a new JSON object for the new tool and the necessary data items in the ``promotion_gates`` JSON objects
  * ``config.json.sample``  - Make the same changes that you did in the ``config.json`` file
  * ``configengine.py``
  * ``dataengine.py``       - Only do data gathering and data preperation here
  * ``comparisonengine.py`` - Only do data comparison and output here
  * ``yourtoolnamehere.py``

####Tips for Adding a new Data Item
 * Follow the examples of BlazeMeter and AppDynamics.
 * AppDynamics has an interesting example of a data item that cannot be used when another data item is used that may be worth checking out (``load_test_length_min`` and ``load_test_start_ms``/``load_test_end_ms``)
