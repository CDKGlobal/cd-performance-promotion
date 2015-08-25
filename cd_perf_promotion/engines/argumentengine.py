import argparse
import sys

class ArgumentEngine:
    """
    Handles all command-line arguments
    """

    def conflicting_arg_error(self):
        print("ERROR: Using conflicting arguments.")
        sys.exit(1)

    def process_arguments(self):
        """
        Handle all of the arguments
        """
        # Store all of our arguments
        arguments = {
            'lr': None,
            'll': None,
            'oc': None,
            'blzkey': None,
            'blztest': None,
            'appduser': None,
            'appdpass': None,
            'appdapp': None,
            'wpgtkey': None
        }

        # Add all of the arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-lr", help="Executes the program with the configuration file located at the provided URL")
        parser.add_argument("-ll", help="Executes the program with the configuration file located at the provided file path")
        parser.add_argument("-oc", help="Prints the output to the console", action="store_true")
        # All of the BlazeMeter API credentials arguments
        parser.add_argument("-blzkey", help="Replaces the BlazeMeter API key in the configuration file")
        parser.add_argument("-blztest", help="Replaces the BlazeMeter test ID in the configuration file")
        # All of the AppDynamics API credentials arguments
        parser.add_argument("-appduser", help="Replaces the AppDynamics username in the configuration file")
        parser.add_argument("-appdpass", help="Replaces the AppDynamics password in the configuration file")
        parser.add_argument("-appdapp", help="Replaces the AppDynamics application name in the configuration file")
        # All of the WebPageTest API credentials arguments
        parser.add_argument("-wpgtkey", help="Replaces the WebPageTest API key in the configuration file")
        args = parser.parse_args()

        # Configuration file is located remotely
        if args.lr:
            arguments['lr'] = args.lr
        if args.ll:
            arguments['ll'] = args.ll
        # Print out data to the console as well
        if args.oc:
            arguments['oc'] = args.oc
        # Use the command line to set the BlazeMeter API Key
        if args.blzkey:
            arguments['blzkey'] = args.blzkey
        # Use the command line to set the BlazeMeter Test ID
        if args.blztest:
            arguments['blztest'] = args.blztest
        # Use the command line to set the AppDynamics username
        if args.appduser:
            arguments['appduser'] = args.appduser
        # Use the command line to set the AppDynamics username
        if args.appdpass:
            arguments['appdpass'] = args.appdpass
        # Use the command line to set the AppDynamics username
        if args.appdapp:
            arguments['appdapp'] = args.appdapp
        # Use the command line to set the WebPageTest Test ID
        if args.wpgtkey:
            arguments['wpgtkey'] = args.wpgtkey

        # Make sure overriding arguments aren't used
        if (args.lr and args.ll):
            self.conflicting_arg_error()

        return arguments;
