# CDK Atlasssian Bamboo Integration

CDK uses Atlassian Bamboo as its continuous integration/delivery/deployment platform. To use this program with Bamboo, please add the following tasks:

1. Source Code Checkout of ```CD Performance Promotion``` (this tool)
2. Script:

  ```
  /opt/python3.4.3/bin/pyvenv ${bamboo.build.working.directory}/py3env
  source ${bamboo.build.working.directory}/py3env/bin/activate
  python3 setup.py install
  ```
3. Source Code Checkout of ```INSERT YOUR CONFIG.JSON REPO HERE```
4. Script:

  ```
  sed -i s/apikeygoeshere/${bamboo.blazemeter.apiKey}/g config.json
  sed -i s/testidgoeshere/${bamboo.blazemeter.testId}/g config.json
  ${bamboo.build.working.directory}/py3env/bin/cdperfpromotion
  [[ ! $(grep '"passed": false' cdperfpromodata*.json) ]]
  ```
  The ```sed``` commands replace part of the downloaded configuration file so that critical credentials (usernames/password, API keys, etc.) are not stored in source control. The ```sed``` commands in the above script are only replacing the BlazeMeter API key and and test ID since the configuration file only includes data from BlazeMeter.

  The call to ```${bamboo.build.working.directory}/py3env/bin/cdperfpromotion``` is actually running the program.

  Please note that this is a prototype tool and that while the setup in the CDK environment is currently a little bit complicated, the wrinkles will be ironed out in future releases.
