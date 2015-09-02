# Dictionary
##### All of the possible data items that can be used in the configuration file
All fields marked as required are only required if you want to use the tool associated with it

| Data Item                     | Type    | Parent Object          | Associated Tool | Description                                                                                                 | Required |
| :---------------------------- | :-----  | :--------------------- | :-------------- | :---------------------------------------------------------------------------------------------------------- | :------- |
| ``appdynamics``               | Object  | None                   | AppDynamics     | Contains all of the AppDynamics specific information                                                        | Yes      |
| ``username``                  | String  | appdynamics            | AppDynamics     | Appdynamics username in the format of username@account                                                      | Yes      |
| ``password``                  | String  | appdynamics            | AppDynamics     | Appdynamics password                                                                                        | Yes      |
| ``load_test_length_min``      | Number  | appdynamics            | AppDynamics     | Length of the load test period (X number of minutes before current time)                                    | Yes*     |
| ``load_test_length_start_ms`` | Number  | appdynamics            | AppDynamics     | Time that you want to begin monitoring at. Format is milliseconds after Unix epoch time (January 1st, 1970) | Yes*     |
| ``load_test_length_end_ms``   | Number  | appdynamics            | AppDynamics     | Time that you want to monitoring to stop. Format is milliseconds after Unix epoch time (January 1st, 1970)  | Yes*     |
| ``blazemeter``                | Object  | None                   | BlazeMeter      | Contains all of the BlazeMeter specific information                                                         | Yes      |
| ``api``                       | String  | blazemeter             | BlazeMeter      | BlazeMeter API key                                                                                          | Yes      |
| ``test_id``                   | String  | blazemeter             | BlazeMeter      | Unique BlazeMeter test ID -- used to run the BlazeMeter load test and gather data                           | Yes      |
| ``webpagetest``               | Object  | None                   | WebPageTest     | Contains all of the WebPageTest specific information                                                        | Yes      |
| ``url``                       | String  | webpagetest            | WebPageTest     | URL being tested                                                                                            | Yes      |
| ``location``                  | String  | webpagetest            | WebPageTest     | Where the WebPageTest test will be run from. See below for a complete list of locations.                    | Yes      |
| ``runs``                      | Number  | webpagetest            | WebPageTest     | The number of times that WebPageTest will execute the test                                                  | Yes      |
| ``api``                       | String  | webpagetest            | WebPageTest     | WebPageTest API key                                                                                         | Yes      |
| ``promotion_gates``           | Object  | None                   | BlazeMeter      | Contains all of the promotion gate criteria                                                                 | Yes      |
| ``response_time_avg``         | Number  | promotion_gates        | BlazeMeter      | Average response time (under BlazeMeter load)                                                               | No       |
| ``response_time_max``         | Number  | promotion_gates        | BlazeMeter      | Maximum response time (under BlazeMeter load)                                                               | No       |
| ``response_time_stdev``       | Number  | promotion_gates        | BlazeMeter      | Response time standard deviation (under BlazeMeter load)                                                    | No       |
| ``response_time_tp90``        | Number  | promotion_gates        | BlazeMeter      | 90% line -- 90% of requests were handled in this amount of time (under BlazeMeter load)                     | No       |
| ``response_time_tp95``        | Number  | promotion_gates        | BlazeMeter      | 95% line -- 95% of requests were handled in this amount of time (under BlazeMeter load)                     | No       |
| ``response_time_tp99``        | Number  | promotion_gates        | BlazeMeter      | 99% line -- 99% of requests were handled in this amount of time (under BlazeMeter load)                     | No       |
| ``latency_avg``               | Number  | promotion_gates        | BlazeMeter      | Average latency (under BlazeMeter load)                                                                     | No       |
| ``latency_max``               | Number  | promotion_gates        | BlazeMeter      | Maximum latency (under BlazeMeter load)                                                                     | No       |
| ``latency_stdev``             | Number  | promotion_gates        | BlazeMeter      | Latency standard deviation (under BlazeMeter load)                                                          | No       |
| ``bandwidth_avg``             | Number  | promotion_gates        | BlazeMeter      | Average Bandwidth -- Bytes/Second (under BlazeMeter load)                                                   | No       |
| ``transaction_rate``          | Number  | promotion_gates        | BlazeMeter      | Average Throughput (AKA Transaction Rate) -- Hits/Second (under BlazeMeter load)                            | No       |
| ``warning``                   | Boolean | promotion_gates        | AppDynamics     | Indicates if AppDynamics health rule violations with a status of ``WARNING`` matter                         | No       |
| ``critical``                  | Boolean | promotion_gates        | AppDynamics     | Indicates if AppDynamics health rule violations with a status of ``CRITICAL`` matter                        | No       |
| ``first_view``                | Object  | promotion_gates        | WebPageTest     | Container for WebPageTest metrics for the first time a page is loaded                                       | Yes**    |
| ``repeat_view``               | Object  | promotion_gates        | WebPageTest     | Container for WebPageTest metrics for the second time a page is loaded                                      | Yes**    |
| ``speed_index``               | Number  | first_view/repeat_view | WebPageTest     | WebPageTest Speed Index, the average time (ms) at which the visible parts of the page are displayed         | No       |
| ``first_paint``               | Number  | first_view/repeat_view | WebPageTest     | Time to when the page displays something on the screen (ms) (browser reported)                              | No       |
| ``start_render``              | Number  | first_view/repeat_view | WebPageTest     | Time to when the page displays something on the screen (ms) (WebPageTest determined)                        | No       |
| ``first_byte``                | Number  | first_view/repeat_view | WebPageTest     | Time to first byte (ms)                                                                                     | No       |
| ``fully_loaded``              | Number  | first_view/repeat_view | WebPageTest     | Time to page fully loaded (ms)                                                                              | No       |
| ``visual_complete``           | Number  | first_view/repeat_view | WebPageTest     | Time to when the page looks like it has fully loaded (ms)                                                   | No       |
| ``last_visual_change``        | Number  | first_view/repeat_view | WebPageTest     | Time to when the last visual change to the page is made (ms)                                                | No       |
| ``title_time``                | Number  | first_view/repeat_view | WebPageTest     | Time to when the HTML <Title></Title> tags are loaded (ms)                                                  | No       |
| ``page_size``                 | Number  | first_view/repeat_view | WebPageTest     | The amount of data that the browser has to download in order to load the page (bytes)                       | No       |
| ``elastic_kibana``            | Object  | None                   | Elastic/Kibana  | Contains all of the ElasticSearch/Kibana information for outputting the data to a Kibana dashboard          | Yes      |
| ``elastic_server``            | String  | elastic_kibana         | Elastic/Kibana  | The server name (with port) of the ElasticSearch instance used for your Kibana dashboard                    | Yes      |
| ``index``                     | String  | elastic_kibana         | Elastic/Kibana  | The name of the index you are using for your Kibana dashboard                                               | Yes      |

\*Either ``load_test_length_min`` or both ``load_test_length_start_ms`` and ``load_test_length_end_ms`` must be declared

\*\*Required if you want to use any WebPageTest data

#### Available WebPageTest Locations
* Dulles_IE9
* Dulles_IE10
* Dulles_IE11
* Dulles:Chrome
* Dulles:Canary
* Dulles:Firefox
* Dulles:Firefox Nightly
* Dulles:Safari
* Dulles_MotoG:Motorola G - Chrome
* Dulles_MotoG:Motorola G - Chrome Beta
* Dulles_MotoG:Motorola G - Chrome Dev
* ec2-us-east-1:Chrome
* ec2-us-east-1:IE 11
* ec2-us-east-1:Firefox
* ec2-us-east-1:Safari
* ec2-us-west-1:Chrome
* ec2-us-west-1:IE 11
* ec2-us-west-1:Firefox
* ec2-us-west-1:Safari
* ec2-us-west-2:Chrome
* ec2-us-west-2:IE 11
* ec2-us-west-2:Firefox
* ec2-us-west-2:Safari
* ec2-eu-west-1:Chrome
* ec2-eu-west-1:IE 11
* ec2-eu-west-1:Firefox
* ec2-eu-west-1:Safari
* ec2-eu-central-1:Chrome
* ec2-eu-central-1:IE 11
* ec2-eu-central-1:Firefox
* ec2-eu-central-1:Safari
* ec2-ap-northeast-1:Chrome
* ec2-ap-northeast-1:IE 11
* ec2-ap-northeast-1:Firefox
* ec2-ap-northeast-1:Safari
* ec2-ap-southeast-1:Chrome
* ec2-ap-southeast-1:IE 11
* ec2-ap-southeast-1:Firefox
* ec2-ap-southeast-1:Safari
* ec2-ap-southeast-2:Chrome
* ec2-ap-southeast-2:IE 11
* ec2-ap-southeast-2:Firefox
* ec2-ap-southeast-2:Safari
* ec2-sa-east-1:Chrome
* ec2-sa-east-1:IE 11
* ec2-sa-east-1:Firefox
* ec2-sa-east-1:Safari
