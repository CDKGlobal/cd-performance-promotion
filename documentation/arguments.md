# Arguments

## Dictionary
| Argument      | Value                        | Explanation                                                                        |
| :------------ | :--------------------------- | :--------------------------------------------------------------------------------- |
| ``-h``        | N/A                          | Help -- Lists all of the arguments and information about them                      |
| ``-lr``       | Configuration file URL       | Executes the program with the configuration file located at the provided URL       |
| ``-ll``       | Configuration file file path | Executes the program with the configuration file located at the provided file path |
| ``-blzkey``   | BlazeMeter API key           | Replaces the BlazeMeter API key in the configuration file                          |
| ``-blztest``  | BlazeMeter Test ID           | Replaces the BlazeMeter Test ID in the configuration file                          |
| ``-appduser`` | AppDynamics Username         | Replaces the AppDynamics username in the configuration file                        |
| ``-addppass`` | AppDynamics Password         | Replaces the AppDynamics password in the configuration file                        |
| ``-appdapp``  | AppDynamics Application Name | Replaces the AppDynamics application name in the configuration file                |
| ``-wpgtkey``  | WebPageTest API key          | Replaces the WebPageTest API key in the configuration file                         |
| ``-oc``       | N/A                          | Prints the the output to the console (in addition to the normal output to file)    |

## Adding New Arguments
1. Navigate to the ```cd_perf_promotion/engines/argumentengine.py``` file.
2. Add your argument to the ```arguments``` dictionary:

    ```
    # Store all of our arguments
    arguments = {
        'lr': None,
        'oc': None,
        'newarg': None
    }
    ```
3. Add an ```add_argument()``` call for your new argument with an appropriate ```--help```/```-h``` description. If you do not want your argument to take in a data parameter (e.g. ```cdperfpromotion -newarg``` instead of ```cdperfpromotion -newarg "data parameter"```), specify include the action="store_true" tag to the ```add_argument()``` method. This will make the value of your argument equal to ```True``` if it is included.

   ```
   parser = argparse.ArgumentParser()
   parser.add_argument("-lr", help="Executes the program with the configuration file located at the provided URL")
   parser.add_argument("-oc", help="Prints the output to the console", action="store_true")
   parser.add_argument("-newarg", help="NewArgument Help Description")
   parser.add_argument("-newarg2", help="NewArgument2 Help Description", action="store_true")
   args = parser.parse_args()
   ```
4. Add an additional ```if``` statement for your argument:

   ```
   # Configuration file is located remotely
   if args.lr:
       arguments['lr'] = args.lr
   # Print out data to the console as well
   if args.oc:
       arguments['oc'] = args.oc
   # NewArgument Comment
   if args.newarg:
       arguments['newarg'] = args.newarg
   ```
5. Navigate to the ```cd_perf_promotion/main.py``` file. Pass the argument data (```arguments['newarg']```) to the necessary module as a parameter where necessary.
