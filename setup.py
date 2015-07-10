from setuptools import setup

setup(
      name = "cd-perf-promotion",
      version = "0.1",
      description = "Continuous Delivery Performance Promotion Tool",
      author = "Jared Petersen",
      author_email = "Jared.Petersen@cdk.com",
      license = "Copyright 2015 CDK Global, LLC",
      packages = ["cd-perf-promotion"],
      entry_points={
        "console_scripts": [
                "cd-perf-promotion = cd-perf-promotion.__main__:main"
            ]
      },
     )
