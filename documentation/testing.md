# Testing

#### Run Manual Tests
Navigate to the ```tests/``` directory via the command line and run ```python test_suite.py```. This will kick off all of the tests and output the testing results as JUnit XML.

#### Automated Tests with Atlassian Bamboo

The following tasks are used to perform the Continuous Delivery Performance Promotion Tool's automated tests on Bamboo:

1. Source Code Checkout of ```CD Performance Promotion``` (this tool)
2. Script:

  ```
  /opt/python3.4.3/bin/pyvenv ${bamboo.build.working.directory}/py3env
  source ${bamboo.build.working.directory}/py3env/bin/activate
  python3 setup.py install
  cd tests && python3 test_suite.py
  ```
3. JUnit Parser with a custom directory of ```**/test-reports/*.xml```
