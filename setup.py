from setuptools import setup

setup(
      name = "cd_perf_promotion",
      version = "1.0.0",
      description = "Evaluate and promote builds on a CI/CD platform based on performance",
      author = "Jared Petersen",
      author_email = "Jared.Petersen@cdk.com",
      url = "https://github.com/CDKGlobal/cd-performance-promotion",
      license = "MIT",
      packages = ["cd_perf_promotion",
                  "cd_perf_promotion.engines",
                  "cd_perf_promotion.modules"],
      install_requires = ["requests",
                          "unittest-xml-reporting"],
      entry_points={
        "console_scripts": ["cdperfpromotion=cd_perf_promotion.main:main"]
      },
     )
