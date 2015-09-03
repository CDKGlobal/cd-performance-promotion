# Continuous Delivery Performance Promotion Tool
The Continuous Delivery Performance Promotion Tool is a Python program that is used to evaluate whether applications are performing well enough to be moved on to the next stage in the continuous delivery system. This tool allows users to define how their application should be performing via a simple JSON configuration file and then evaluates the application's actual performance against those criteria. Currently, the program supports AppDynamics, BlazeMeter, and WebPageTest but aims to support other load testing tools like SilkPerformer and Visual Studio Test Suite as well in the future.

![Running Program](documentation/screenshots/running.png)

# Getting Started

## Installation (Basic)
1. Run ``pip install cd_perf_promotion``
2. You're done!

## Installation (Advanced)
1. Make sure that you have the latest version of Python and Pip installed and that you can run both via your command-line interface (CLI).
2. Download the source code and navigate to it using your CLI.
3. Inside the cd_perf_promotion downloaded directory, run ``python setup.py install`` to begin installation.
4. The application will download the necessary dependencies via Pip and install itself. You will now be able to run the program from your CLI via the command ``cdperfpromotion``.
5. You're done!

## Defining Your Promotion Criteria
Your ``config.json`` file contains all of the configuration information that the tool needs to retrieve data from your performance tools and evaluate whether your application meets your performance standards. We've provided some sample configuration files (located in ``documentation/sample_configs/input``) to help you get started. A complete list of all of the available data items that can be used to evaluate the performance of your application and information on what they really mean is available in the ``dictionary.md`` file inside the ``documentation`` directory.

We've put a lot of work into making sure that the program is modular and customizable so that you don't have to include all of the data items that exist in the configuration file. Instead, only include the tools that you are using and the data items that you would like to include. Anything not included will not be evaluated against. Please note that you must include configuration information for the tools used to gather the information that is defined. For example, if you wanted to include your application's average response time, you must also include a BlazeMeter section with a BlazeMeter API key and test ID.

## Starting the Program
1. Set up your configuration file. Please see the **Defining Your Promotion Criteria** section for more information.
2. You have two options when it comes to where your configuration file is stored. You can either have it located on your local machine or have it hosted somewhere on the web. If you plan to store the configuration file locally, navigate to the directory containing your configuration file via the CLI. If your configuration file is hosted somewhere on the web, it does not matter where you run the application.
3. Run the Continuous Delivery Performance Promotion Tool from the CLI by entering ``cdperfpromotion`` for local configuration files or ``cdperfpromotion -lr http://urlgoeshere`` for remote configuration files. A full list of arguments is available in the ``arguments.md`` file located in the ``documentation`` directory. If you are a CDK associate, you will most likely have your configuration file located in an Atlassian Stash repository. In that case, your URL will need to look something like this to get past the authentication wall: ``http://username:password@stash.ds.adp.com/projects/PROJECTKEYHERE/repos/REPOSLUGHERE/browse/CONFIGFILEHERE?raw``.
4. The program will output a JSON file in the same directory that it is run with a filename in the format of ``cdperfpromotion_MMDDYY_HHmmss.json`` (the latter half of the filename being a timestamp).

## Evaluating the Results
The ``promotion_gates`` JSON object in the output file contains all of the high-level information about whether each data metric met the configuration file target. If any of the transactions/runs has a data item that does not meet the predefined performance target, the whole data item is marked as failed in the ``promotion_gates`` section. If a data item is failed, you can go up to that respective data item's parent tool and figure out where it failed and what the actual result was.

For example, the sample configuration file ``config_all.json.sample`` defines that there must not be any AppDynamics health rule violations with a severity of warning (``"warning": true``) or critical (``"critical": true``). Unfortunately, the output file, ``cdperfpromodata_timestamp_all.json.sample``, states in the ``promotion_gates`` section that this data item has failed (``"appdynamics_health": false``). Knowing that, we can go up and look at the ``appdynamics`` section which reveals that the application we're evaluating has a health rule violation with a severity of warning that is notifying us that the application is using too much memory.

It's important to note that if any of the data items specified in the configuration file fails, the entire application will fail and will not be promoted to the next stage.
