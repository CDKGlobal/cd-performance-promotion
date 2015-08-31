# Kibana Integration
You have the option of outputting the performance data retrieved during the performance evaluation to a Kibana dashboard.

### Create an ElasticSearch index
Make a POST request to your ElasticSearch server at the desired index location with a payload of the JSON data located in the ``elktemplate.json`` file. This is what such a request would look like in cURL:

  ```
  curl -xput http://urlgoeshere:9200/indexnamehere -d "elktemplatejsonstuffgoeshere"
  ```
Please note that if you use cURL from the Windows command prompt, you may need to take the JSON in the ``elktemplate.json`` file and escape all of the double-quotation marks with a backslash. Depending on the network environment that you have set up, you may also need to include the ``--noproxy`` tag in the cURL request as well. If your index creation request was successful, you should recieve the following response:

  ```
  {"acknowledged":true}
  ```

### Create a Kibana Dashboard
Coming soon

### Enable Kibana Output
Coming soon
