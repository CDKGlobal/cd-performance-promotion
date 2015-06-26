from setuptools import setup

setup(
      name = "ci-perf-promotion",
      version = "0.1",
      description = "Continuous Integration Performance Promotion Tool",
      author = "Jared Petersen",
      author_email = "Jared.Petersen@cdk.com",
      license = "Copyright 2015 CDK Global, LLC",
      packages = ["ci-perf-promotion"],
      entry_points={
        "console_scripts": [
                "ci-perf-promotion = ci-perf-promotion.__main__:main"
            ]
      },
     )
