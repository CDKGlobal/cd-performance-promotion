import argparse

class ArgumentEngine:
    """
    Handles all command-line arguments
    """

    def process_arguments(self):
        """
        Handle all of the arguments
        """
        # Store all of our arguments
        arguments = {
            'lr': None,
            'oc': None,
            'blzkey': None,
            'blztest': None
        }

        # Add all of the arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-lr", help="Executes the program with the configuration file located at the provided URL")
        parser.add_argument("-oc", help="Prints the output to the console", action="store_true")
        # All of the BlazeMeter API credentials arguments
        parser.add_argument("-blzkey", help="Replaces the BlazeMeter API key in the configuration file")
        parser.add_argument("-blztest", help="Replaces the BlazeMeter test ID in the configuration file")
        args = parser.parse_args()

        # Configuration file is located remotely
        if args.lr:
            arguments['lr'] = args.lr
        # Print out data to the console as well
        if args.oc:
            arguments['oc'] = args.oc
        # Use the command line to set the BlazeMeter API Key
        if args.blzkey:
            arguments['blzkey'] = args.blzkey
        # Use the command line to set the BlazeMeter API test ID
        if args.blztest:
            arguments['blztest'] = args.blztest

        return arguments;
