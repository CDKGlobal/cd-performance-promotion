from setuptools import setup

setup(
      name = "cd_perf_promotion",
      version = "0.1",
      description = "Continuous Delivery Performance Promotion Tool",
      author = "Jared Petersen",
      author_email = "Jared.Petersen@cdk.com",
      license = "Copyright 2015 CDK Global, LLC",
      packages = ["cd_perf_promotion",
                  "cd_perf_promotion.engines",
                  "cd_perf_promotion.modules"],
      install_requires = ["requests",
                           "xmltodict"],
      entry_points={
        "console_scripts": ["cdperfpromotion=cd_perf_promotion.main:main"]
      },
     )
