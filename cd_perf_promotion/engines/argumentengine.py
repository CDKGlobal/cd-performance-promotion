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
            'oc': None
        }

        parser = argparse.ArgumentParser()
        parser.add_argument("-lr", help="Executes the program with the configuration file located at the provided URL")
        parser.add_argument("-oc", help="Prints the output to the console (ALPHA)", action="store_true")
        args = parser.parse_args()

        # Configuration file is located remotely
        if args.lr:
            arguments['lr'] = args.lr
        # Print out data to the console as well
        if args.oc:
            arguments['oc'] = args.oc

        return arguments;
