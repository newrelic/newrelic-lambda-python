<a href="https://opensource.newrelic.com/oss-category/#community-project"><picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/newrelic/opensource-website/raw/main/src/images/categories/dark/Community_Project.png"><source media="(prefers-color-scheme: light)" srcset="https://github.com/newrelic/opensource-website/raw/main/src/images/categories/Community_Project.png"><img alt="New Relic Open Source community project banner." src="https://github.com/newrelic/opensource-website/raw/main/src/images/categories/Community_Project.png"></picture></a>

# New Relic Lambda Python [build badges go here when available]


This module provides a decorator, `@lambda_handler` that enables New Relic instrumentation
of an AWS Lambda function.

New Relic recommends using its [Lambda Layer](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/instrument-lambda-function/configure-serverless-aws-monitoring/) for seamless instrumentation. For the manual instrumentation process, check out this [guide](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/instrument-lambda-function/sdk-based-instrumentation/) or follow the [Usage](#usage) steps below.

## Usage

To manually apply the lambda_handler decorator to code, see our [full SDK example](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/instrument-lambda-function/sdk-based-instrumentation/) on our docs website, or reference the same quickstart below.

1. Download both the Python agent and Python lambda wrapper packages and place them in the same directory as your function code. To do this, use pip:

    ```bash
    pip install -t . newrelic newrelic-lambda
    ```

2. In your Lambda code, import both the Python agent module and the Python lambda wrapper module.

3. Decorate the handler function using the New Relic decorator. The New Relic package must be imported first in your code. Here's an example:

    ```python
    import newrelic.agent
    from newrelic_lambda.lambda_handler import lambda_handler

    newrelic.agent.initialize()

    @lambda_handler()
    def handler(event, context):
    ...
    ```

4. **Optional:** You can also add custom events to your Lambda using the record_custom_event API. Here's an example:

    ```python
    @lambda_handler()
    def handler(event, context):
    newrelic.agent.record_custom_event('CustomEvent', {'foo': 'bar'})
    ...
    ```

5. Zip your `lambda_function.py`, `newrelic/` and `newrelic_lambda/` folders together using these guidelines:

    * The New Relic files outside the newrelic/ folder don't need to be included.
    
    * If your Lambda function file name is, for example, lambda_function.py, name your zip file lambda_function.zip. Do not use a tarball.
    
    * Your Lambda and its associated modules must all be in the zip file's root directory. This means that if you zip a folder that contains the files, it won't work.

6. Upload the zipped file to your AWS Lambda account.

7. To enable distributed tracing and configure environmental variables, refer environment variables documentation.

8. Invoke the Lambda at least once. This creates a CloudWatch log group, which must be present for the next step to work.

    The New Relic decorator gathers data about the Lambda execution, generates a JSON message, and logs it to CloudWatch Logs. Next, configure CloudWatch to send those logs to New Relic.

## Building

To build this project for local testing, use pip to create an editable install with the following command.

```bash
pip install -e .
```

## Testing

For testing we use `tox` to handle generating virtual environments for each supported python version. If you have multiple Python versions available on your system, you can run the appropriate tests with the following command, using Python 3.12 as an example:

```bash
tox run -e py312
```

## Support

New Relic hosts and moderates an online forum where you can interact with New Relic employees as well as other customers to get help and share best practices. Like all official New Relic open source projects, there's a related Community topic in the New Relic Explorers Hub. You can find this project's topic/threads here:

>Add the url for the support thread here: discuss.newrelic.com

## Contribute

We encourage your contributions to improve New Relic Lambda Python! Keep in mind that when you submit your pull request, you'll need to sign the CLA via the click-through using CLA-Assistant. You only have to sign the CLA one time per project.

If you have any questions, or to execute our corporate CLA (which is required if your contribution is on behalf of a company), drop us an email at opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed to the privacy and security of our customers and their data. We believe that providing coordinated disclosure by security researchers and engaging with the security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of New Relic's products or websites, we welcome and greatly appreciate you reporting it to New Relic through [our bug bounty program](https://docs.newrelic.com/docs/security/security-privacy/information-security/report-security-vulnerabilities/).

If you would like to contribute to this project, review [these guidelines](./CONTRIBUTING.md).

To all contributors, we thank you!  Without your contribution, this project would not be what it is today.  We also host a community project page dedicated to New Relic Lambda Python(<LINK TO https://opensource.newrelic.com/projects/... PAGE>).

## License
New Relic Lambda Python is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.
