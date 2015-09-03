# CDK Atlasssian Bamboo Integration

CDK uses Atlassian Bamboo as its continuous integration/delivery/deployment platform. To use this program with Bamboo, please add the following tasks:

1. Source Code Checkout of ```CD Performance Promotion``` (this tool) with ``Force Clean Build`` checked
2. Source Code Checkout of ```INSERT YOUR CONFIG.JSON REPO HERE``` with a Checkout Directory of ```./config``` and with ``Force Clean Build`` checked
3. Script:

  ```
  /opt/python3.4.3/bin/pyvenv ${bamboo.build.working.directory}/py3env
  source ${bamboo.build.working.directory}/py3env/bin/activate
  python3 setup.py install
  ${bamboo.build.working.directory}/py3env/bin/cdperfpromotion -ll ./config/config.json -blzkey ${bamboo.blazemeter.apiKey} -blztest ${bamboo.blazemeter.testId} -oc
  ```
