# Check AWS RDS tfstate Files

Check AWS RDS tfstate files is a tool that can be used to query Terraform tfstate files stored remotely in a S3 bucket versus existing AWS RDS infrastructure to determine if there are instances not managed by Terraform IaC.

This tool was initially created specific to checking AWS RDS infrastructure but could easily be modified to check other AWS resources.

## Technology Utilized

This tool is written in Python v3 and utilizes the [AWS CDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for interaction with AWS services.

## Usage Prerequisites

* Set up environment for using AWS, Okta and Python3. Additionally install boto3, `pip install boto3`
* Authenticate into target AWS environment.

## Usage

* Clone the repo and cd into the repo directory.
* Help
```
  usage: check_aws_rds_tfstates.py [-h] -b BUCKET -p PATH [-f FOLDER] -a APPPREFIX

  optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET, --bucket BUCKET
                          AWS S3 bucket
  -p PATH, --path PATH  AWS S3 bucket folder path to tfstate files
  -f FOLDER, --folder FOLDER
                        Local folder to write tfstate file to (default ./s3-bucket-tfstate-files)
  -a APPPREFIX, --appprefix APPPREFIX
                          Application prefix on RDS IDs
```
* Command line example execution:
```
  python3 check_aws_rds_tfstates.py -b cicd-myenv-tfstate-eu-west-1 -p myapp/rds/ -a myapp- -f myenv-rds-bucket-tfstate`
```

## Development and Testing

Simply setup a Python v3.6 and install the AWS CDK package boto3.

### Testing

Unit tests for functions can be found in the `./test` directory with sample test files in the `./test-files` directory. The tests can be executed by executing the following command:

```
python3 -m unittest -v
```

**Note:** Ignore the ResourceWarning in regards to unclosed SSLSock, this is a known issue in boto3 unit testing.