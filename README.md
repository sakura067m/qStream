qStream
=======

Show the message you get in slack.


Installation
------------
When this repo is *open*, then
```shell
pip install git+https://github.com/sakura067m/qStream.git
```
Otherwise
```shell
git clone https://<your username>@github.com/sakura067m/qStream.git
```
and then, install from the clone using a command like `pip install qStream`.

Also, please remember to set your *SLACK_LEGACY_TOKEN* when you use.  
This app will access it by calling `os.environ["SLACK_LEGACY_TOKEN"]`.  
LEGACY TOKEN can be found in  [api.slack.com](https://api.slack.com/custom-integrations/legacy-tokens).  
To know more about tokens, see [slack.dev](https://slack.dev/python-slackclient/auth.html#handling-tokens-and-other-sensitive-data).  
In short, you can set the env everytime you run or just save it to the settings.

Requirements
------------
* Python3.6+(perhaps lower also work)
* PyQt5
* slackclinet
