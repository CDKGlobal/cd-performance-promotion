# Program Structure/Index
##### Brief explanation of all of the files

| Item                                          | Type   | Parent            | Description                                                                       |
| :-------------------------------------------- | :----- | :---------------- | :-------------------------------------------------------------------------------- |
| ``cd_perf_promotion``                         | Folder | None              | Contains all of the code                                                          |
| ``documentation``                             | Folder | None              | Contains all of the documentation                                                 |
| ``MANIFEST.in``                               | File   | None              | Used to keep the documentation with the installed program                         |
| ``README.md``                                 | File   | None              | Main introductory/basic documentation                                             |
| ``setup.py``                                  | File   | None              | Used to install the software                                                      |
| ``engines``                                   | Folder | cd_perf_promotion | Contains all of the python code that performs the main functionality (the doers)  |
| ``modules``                                   | Folder | cd_perf_promotion | Contains all of the python code for each performance tool                         |
| ``tests``                                     | Folder | cd_perf_promotion | Contains all of the testing code                                                  |
| ``main.py``                                   | File   | cd_perf_promotion | Main entry point to the program                                                   |
| ``argumentengine.py``                         | File   | engines           | Processes the arguments from the command-line                                     |
| ``comparisonengine.py``                       | File   | engines           | Performs comparisons between the configuration target metrics and actual data     |
| ``configengine.py``                           | File   | engines           | Grabs the target metrics from the configuration file                              |
| ``dataengine.py``                             | File   | engines           | Grabs the data from the tool modules and organizes it for the Comparison Engine   |
| ``outputengine.py``                           | File   | engines           | Handles all of the data output logic                                              |
| ``appdynamics.py``                            | File   | modules           | Grabs data from AppDynamics                                                       |
| ``blazemeter.py``                             | File   | modules           | Grabs data from BlazeMeter                                                        |
| ``webpagetest.py``                            | File   | modules           | Grabs data from WebPageTest                                                       |
| ``test_suite.py``                             | File   | tests             | Holds all of the tests for the application                                        |
| ``test_configs``                              | Folder | tests             | Contains all of the configuration files used in tests                             |
| ``config_test#.json``                         | File   | test_configs      | Configuration file for the tests                                                  |
| ``sample_configs``                            | Folder | documentation     | Contains all of the sample configuration files and respective sample output files |
| ``screenshots``                               | Folder | documentation     | Contains all of the screenshots for the documentation                             |
| ``arguments.md``                              | File   | documentation     | Information on all of the available arguments and how to add new ones             |
| ``bamboo.md``                                 | File   | documentation     | Information on how to integrate the tool with Bamboo                              |
| ``dictionary.md``                             | File   | documentation     | Information on all of the data items that can be used                             |
| ``elastic_kibana.md``                         | File   | documentation     | Information on how to output the data to an ElasticSearch/Kibana dashboard        |
| ``elastic_kibana_template.json``              | File   | documentation     | Mapping template for use in creating an ElasticSearch index                       |
| ``structure.md``                              | File   | documentation     | This file :-)                                                                     |
| ``testing.md``                                | File   | documentation     | Information on the tests and automated testing with Bamboo                        |
| ``updating.md``                               | File   | documentation     | Information on how to update the program with new tools and data items            |
| ``input``                                     | Folder | sample_configs    | Contains all of the sample configuration files                                    |
| ``output``                                    | Folder | sample_configs    | Contains all of the sample output files                                           |
| ``config_all.json.sample``                    | File   | input             | Sample configuration file (includes all data items)                               |
| ``cdperfpromodata_timestamp_all.json.sample`` | File   | output            | Sample output file (tied to all data items configuration file)                    |
| ``__init__.py``                               | File   | Many parents      | Python boilerplate to hook-up all of the files into modules                       |
