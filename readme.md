# **Guardian Data Streaming**

A Python application that retrieves articles from The Guardian API and publishes them to an AWS SQS messenger service for consumption by other applications.

## **Table of Contents**

* Overview  
* Prerequisites  
* Installation  
* Configuration  
* Deployment  
* How to Use  
* Architecture  
* Project Structure  
* Monitoring  
* Testing  
* Troubleshooting

## **Overview**

This project was created for Northcoders, as part of the Tech Returners Skills Bootcamp. It's a data streaming application that searches The Guardian newspaper's API for articles matching specific terms. The results are sent to an AWS message queue (SQS) where they can be processed by other users, such as marketing and careers teams. All code PEP8 compliant, unit tested, and tested for security vulnerabilities.

**What the application does:**

* Builds data pipeline and AWS infrastructure from terminal.  
* Once deployed in AWS it searches articles on The Guardian website using users’ keywords  
* Retrieves the 10 most recent matching articles  
* Sends article details (title, date, URL) to an AWS SQS queue  
* Monitors API usage to stay within daily limits  
* Cloudwatch Logs all activity for troubleshooting

## ---

## **Prerequisites**

Before you begin, you'll need:

1. **Python 3.9** installed on your computer  
   Check if you have it: Open your terminal/command prompt and type `python --version`

2. **An AWS Account**  
   Sign up at: [https://aws.amazon.com/](https://aws.amazon.com/)  
   You can use AWS Free Tier access or paid subscription tiers.

3. **A Guardian API Key** (Free)

Register at: [https://open-platform.theguardian.com/access/](https://open-platform.theguardian.com/access/)  
	This gives you 500 free searches per day

4. **Terraform** (for deployment to AWS)  
   Download from: [https://www.terraform.io/downloads](https://www.terraform.io/downloads)  
   Install \- https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli  
5. **Git** (to download the project)  
   Download from: https://git-scm.com/downloads  
     
   ---

## **Installation**

### **Step 1: Download the Project**

**Option A: Using Git (if installed)**

`git clone https://github.com/TheVelvetShadow/guardian_data_streaming.git`

`cd guardian_data_streaming`

**Option B: Manual Download**

1. Go to the GitHub repository page  
2. Click the green "Code" button  
3. Select "Download ZIP"  
4. Extract the ZIP file to a folder on your computer  
5. Open your terminal/command prompt and navigate to that folder

### **Step 2: Set Up Python Environment**

**On Windows:**

`python -m venv venv`

`venv\Scripts\activate`

**On Mac/Linux:**

`python3 -m venv venv`

`source venv/bin/activate`

You should see `(venv)` appear at the start of your terminal line.

### **Step 3: Install Required Packages**

`pip install -r requirements.txt`

This installs all the Python libraries the project needs.

## 

## 

## 

## ---

## **Configuration**

### **1\. Set Up Your API Key**

Create a file called `terraform.tfvars` in the `terraform` folder:

`guardian_api_key = "your-actual-api-key-here"`

`sns_subscription_email = "your-email@example.com"`

There is a .tfvars.example file in the repo if you are unsure what this file should look like.  
It is located here: [guardian\_data\_streaming](https://github.com/TheVelvetShadow/guardian_data_streaming/tree/main)/terraform/terraform.tfvars.example

**Important:** Never share the .tfvars file or commit it to GitHub. It contains your private API key. (This file is already included in the .gitgnore).

### **2\. Configure AWS Credentials**

You need to tell Terraform how to access your AWS account.

**On Windows (Command Prompt):**

`set AWS_ACCESS_KEY_ID=your_access_key`

`set AWS_SECRET_ACCESS_KEY=your_secret_key`

`set AWS_DEFAULT_REGION=eu-west-2`

**On Mac/Linux:**

`export AWS_ACCESS_KEY_ID=your_access_key`

`export AWS_SECRET_ACCESS_KEY=your_secret_key`

`export AWS_DEFAULT_REGION=eu-west-2`

To get your AWS keys:

1. Log into AWS Console  
2. Go to IAM (Identity and Access Management)  
3. Create a new user with "AdministratorAccess" policy  
4. Create access keys for that user

## ---

 

## **Deployment**

Terraform will build our infrastructure on AWS. The terraform code in the repo takes care of setting up SQS messenger, the lambda function to extract & process our API data, error logging, IAM user roles and policy documents. 

### **Step 1: Initialize Terraform**

Navigate to the terraform folder:

`cd terraform`

Then initiate terraform, type in terminal:

`terraform init`

### **Step 2: Review What Will Be Created**

When we plan terraform it shows us what is to be created in AWS. Type in the terminal:

`terraform plan`

This has not been deployed to the cloud yet. To do that we need to apply or plan.

### **Step 3: Deploy to AWS**

To apply our plan, type:

`terraform apply`

Type `yes` when prompted. This creates:

* An SQS queue to hold article data  
* A Lambda function to fetch articles  
* CloudWatch alarms to monitor the system  
* IAM roles for security permissions

**This typically takes 2-3 minutes.**

### **Step 4: Note the Outputs**

After deployment, Terraform will display important information like your SQS queue URL. Save this for later use.

## 

## ---

## **How to Use**

Our applications code is now stored in AWS as a Lambda function. This means we need to call our lambda function with the terms we wish to search for. You can do this either via your profile on the AWS website, or via the terminal.

**Running the Lambda Function (our API search)**

**From AWS Website / Console:**

1. Go to AWS   
2. Search for the AWS Lambda in your browser  
3. Find the function named `guardian-streaming`  
4. Click the "Test" tab  
5. Create a new test event with this JSON:

`{`

  `"search_term": "technology"`

`}`

5. Click "Test"  
6. Check [https://docs.aws.amazon.com/lambda/latest/dg/testing-functions.html](https://docs.aws.amazon.com/lambda/latest/dg/testing-functions.html) if you struggle.

**From Command Line (using AWS CLI):**

aws lambda invoke \\  
  \--function-name guardian-streaming \\  
  \--payload '{"search\_term": "artificial intelligence"}' \\  
  response.json

### **Viewing Results**

**Check the SQS Queue:**

1. Go to AWS SQS in your browser  
2. Find the queue named `guardian-streaming_articles`  
3. Click "Send and receive messages"  
4. Click "Poll for messages"  
5. You'll see the articles that were found

**Check CloudWatch Logs:**

1. Go to CloudWatch in your browser  
2. Click "Log groups"  
3. Find `/aws/lambda/guardian-streaming`  
4. Click on the most recent log stream

---

 

**Architecture![][image1]**

See Architecture.png 

**Flow:**

1. Users build AWS architecture from console using Terraform. Once deployed in AWS:  
2. Lambda function is triggered (manually or on schedule)  
3. Lambda calls Guardian API with search term  
4. Guardian returns up to 10 matching articles  
5. Lambda formats each article as JSON  
6. Lambda sends each article to SQS queue  
7. SQS Message is sent to user  
8. CloudWatch logs all activity and monitors for errors

## ---

## **Project Structure**

[guardian\_data\_streaming](https://github.com/TheVelvetShadow/guardian_data_streaming/tree/main)/

├── src/  
│   └── extract.py             		\# Main Lambda function and API client  
├── tests/  
│   └── test\_extract.py        		\# Unit tests  
├── terraform/  
│   ├── main.tf                 		\# AWS provider configuration  
│   ├── lambda.tf               		\# Lambda function setup  
│   ├── SQS.tf                  		\# SQS queue configuration  
│   ├── iam.tf                  		\# Security permissions  
│   ├── cloudwatch.tf           		\# Monitoring and alerts  
│   ├── vars.tf                 		\# Variable definitions  
│   └── terraform.tfvars.example 	\# Template for your config  
│  
├── requirements.txt            		\# Python dependencies  
├── .gitignore                 		\# Files to exclude from Git  
├── .flake8				\# PEP8 Compliance settings  
├── README.md                  	\# This file  
└── Streaming Data Project DE.pdf	\# Project Brief

## ---

## **Monitoring**

### **CloudWatch Alarms**

The system automatically monitors:

1. **Lambda Errors** \- Alerts when the function fails  
2. **API Call Limit** \- Warns when approaching 500 calls/day  
3. **SQS Message Age** \- Alerts if messages aren't being processed  
4. **SQS Queue Depth** \- Warns if queue has \>100 messages

You'll receive email alerts (to the email address you added to .tfvars) when these thresholds are reached.

### **Checking Logs**

**View recent Lambda executions:**

`aws logs tail /aws/lambda/guardian-streaming --follow`

**Or in AWS Console:** CloudWatch → Log groups → /aws/lambda/guardian-streaming

---

## **Testing**

All the python code has been unit tested. You can run and check the test as follows:

### **Run All Tests**

`pytest tests/` 

### **Run Security Scan**

`bandit -r src/`

---

## **Troubleshooting**

### **"Invalid API Key" Error**

* Check your Guardian API key in `terraform.tfvars`  
* Verify your API is active at https://open-platform.theguardian.com/explore/ \- The Guardian have an API search portal that you can manually test your key in. See  GuardianExploreAPI.png


### **"Access Denied" AWS Error**

* Confirm your AWS credentials are set correctly  
* Check the IAM user has sufficient permissions

### **Lambda Timeout**

* Default timeout is 300 seconds (5 minutes)  
* Check CloudWatch logs for the specific error

### **No Articles Found**

* Try a different search term  
* Check Guardian API is working: https://content.guardianapis.com/search?api-key=YOUR\_KEY


### **API Rate Limit Reached**

* The free tier allows 500 calls/day  
* CloudWatch alarm will notify you at SNS email provided.   
* Wait until the next day for the limit to reset

## ---

## **Cleanup**

To remove all AWS resources and avoid charges type the following in the terminal:

`cd terraform`

`terraform destroy`

Type `yes` when prompted. This deletes everything created by this project.

---

**Project completed:** October 2025  
**Bootcamp:** Data Engineering / Northcoders  
**Author:** Matt Temperley  
**Web:** https://www.matttemperley.com

