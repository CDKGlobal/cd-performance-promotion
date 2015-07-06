**Continuous Integration Performance Promotion**
================================================

Overview
--------
This is a Python program that is used to retrieve data from load testing and
server monitoring tools like BlazeMeter and AppDynamics, evaluate the metrics
against predefined promotion gates, and promote builds if they meet the
promotion gates.

Running the Program
-------------------
**Setting up Promotion Gates**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration File
~~~~~~~~~~~~~~~~~~
You can set the promotion gates by altering the config.json file. The following
is an example config file that includes all of the possible data items::

  {
    "blazemeter":
    {
      "api": "09c873d5440a040ae1d2",
      "test_id": "r-im-5589cc68db447"
    },
    "promotion_gates":
    {
      "response_time_avg": 230,
      "response_time_max": 1000000,
      "response_time_stdev": 10000000,
      "response_time_tp90": 590,
      "response_time_tp95": 590,
      "response_time_tp99": 590,
      "transaction_rate": 80
    }
  }

You do not have to use all of the available promotion gate metrics and the order
of the keys does not matter. The only required JSON keys are ``api`` and
``test_id`` in the ``blazemeter`` object. All of the other fields may be removed
as necessary.

Configuration-Specific Data Items
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**blazemeter**
    *Object,* Contains all of the BlazeMeter specific information
**api**
    *String,* BlazeMeter API key
**test_id**
    *String,* BlazeMeter Test ID

Generic Data Items
~~~~~~~~~~~~~~~~~~
**promotion_gates**
    *Object,* Contains all of the promotion gate criteria
**response_time_avg**
    *Number,* Average response time
**response_time_max**
    *Number,* Maximum response time
**response_time_stdev**
    *Number,* Response time standard deviation
**response_time_tp90**
    *Number,* 90% line -- 90% of requests were handled in this amount of time
**response_time_tp95**
    *Number,* 95% line -- 95% of requests were handled in this amount of time
**response_time_tp99**
    *Number,* 99% line -- 99% of requests were handled in this amount of time

**Starting the Program**
~~~~~~~~~~~~~~~~~~~~~~~~
1. Navigate to the directory containing the ``__main__.py`` file
2. Run ``python __main__.py``
3. Open the output JSON file specified by the program for testing results.

**Evaluating the Results**
~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``promotion_gates`` JSON object in the output file contains all of the
high-level data on whether or not the build can move on to the next stage (JSON
key ``passed``) and the pass/fail status for each promotion gate that was
previously defined in ``config.json`` file. All of the detailed information on
a transaction basis can be found in the ``blazemeter`` JSON object, allowing
users to identify which transactions are running into performance issues. If
the ``response_time_avg`` promotion gate criteria is marked as failing in the
``promotion_gate`` object, users can look at the transactions listed in
``blazemeter`` object to find out which one caused the build to fail.

Program Structure
-----------------
**documentation**
    *Folder,* Contains all of the documentation for the tool
**packages**
    *Folder,* Contains all of the libraries
**requests**
    *Folder,* Contains the requests library, which is used to query the various
    APIs
**__init__.py**
    *File,* Used to indicate the packages in the program
**__main__.py**
    *File,* Used to run the program
**appdynamics.py**
    *File,* AppDynamics module that gets all of the necessary metrics from the
    AppDynamics API
**blazemeter.py**
    *File,* BlazeMeter module that gets all of the necessary metrics from the
    BlazeMeter API
**comparisonengine.py**
    *File,* Retrieves the data from all of the performance tool modules and
    compares them against the promotion gate criteria defined in config.json
**config.json**
    *File,* Configuration file that is used to define the promotion gate
    criteria and performance tool information (API keys, test IDs, etc.)
**configengine.py**
    *File,* Retrieves the data from the config.json configuration file
