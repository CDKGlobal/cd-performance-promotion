# CDK Atlasssian Bamboo Integration

CDK uses Atlassian Bamboo as its continuous integration/delivery/deployment platform. To use this program with Bamboo, please add the following tasks:

1. Source Code Checkout of ```CD Performance Promotion``` (this tool)
2. Source Code Checkout of ```INSERT YOUR CONFIG.JSON REPO HERE``` with a Checkout Directory of ```./config```
3. Script:

  ```
  /opt/python3.4.3/bin/pyvenv ${bamboo.build.working.directory}/py3env
  source ${bamboo.build.working.directory}/py3env/bin/activate
  python3 -W ignore setup.py -q install
  cd config
  sed -i s/apikeygoeshere/Cnzw3p7YIwdCvuz578YR/g config.json
  sed -i s/testidgoeshere/5078402/g config.json
  ${bamboo.build.working.directory}/py3env/bin/cdperfpromotion
  ```

  * The ```sed``` commands replace part of the downloaded configuration file so that critical credentials (usernames/password, API keys, etc.) are not stored in source control. The ```sed``` commands in the above script are only replacing the BlazeMeter API key and and test ID since the configuration file only includes data from BlazeMeter.

  * The call to ```${bamboo.build.working.directory}/py3env/bin/cdperfpromotion``` is actually running the program.
