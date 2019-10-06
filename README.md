# bballreport_lambdas
Collection of **FaaS Python scripts to be used with AWS lambda** to put/get/update items in DynamoDB

### Contents
* Data creation functions
  * All scripts with filename postfix handler are for accessing information from the MySportsFeeds website and creating a data model more tenable to my data access patterns.
  * These functions require you to have an active subscriptions to MySportsFeeds
  * To create your own DynamoDB table and wire it up to work with these, create a table of your choice and change the tablename within the script of your choosing
    * If you plan to use indexes for alternate access patterns, consult the AWS documentation on Global Secondary Indexes in DynamoDB to become more comfortable with them
  * All data creation lambdas will need BatchWriteItem, PutItem, and UpdateItem permissions on the DynamoDB service

* Data access functions
  * All scripts pre-fixed with get are for accessing information within DynamoDB
  * All data access lambdas will need Query permissions on the DynamoDB service

###  Wiring Lambdas to API Gateway
1. Create an instance of the API Gateway service using either the AWS CLI or Console
2. Create resources for the following suggested topics:
    * player
    * games
    * team
3. Create methods on those resources and for each:
  1. Specify the lambda functions to hook up
  2. Force the requried QueryString parameters and select whicever authorizer you plan to use for validation
  3. Create a mapping within the integration to map QueryString -> {name of event parameter(s) within the functions}
4. Optionally secure your API by referencing the various methods found in the API Gateway documentation 
