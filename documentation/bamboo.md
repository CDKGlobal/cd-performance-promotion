# Atlasssian Bamboo Integration

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
  cdperfpromotion
  [[ ! $(grep '"passed": false' cdperfpromodata*.json) ]]
  ```
