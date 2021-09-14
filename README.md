# ABOUT

#### Visit application at - http://newstest-env.eba-vgkkrtjs.us-west-1.elasticbeanstalk.com/

This application uses deep learning to perform sentiment analysis on financial news articles. It uses a BERT model (Bidirectional Encoder Representations from Transformers) fine-tuned on financial text for use in the financial domain. First, it extracts current news data for the specified companies and time window. Next, it processess the text data and feeds it into the BERT model to create sentiment scores. Also, optionally, it extracts and combines stock data with the corresponding news and sentiment data to create an average sentiment score for each time window. Finally, it uses Anychart, a Javascript charting libary, to present the data in a visually appealing and optimal way.  

# Deployment and Technologies
•	Deployed using various Amazon Web Services  
•	Used Amazon SageMaker to create, host and deploy an endpoint for a pre-built fine-tuned BERT model  
•	Utilized serverless technology to invoke the model endpoint by creating a REST API and Lambda function using Amazon API Gateway and Amazon Lambda  
•	Built the web application around the model using Amazon Elastic Beanstalk, Python, Flask, JavaScript, and across multiple APIs  

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Files

#### AWS_ebextensions_platform -  
- EB config files for NGINX

#### CreatingTheModel -  
- Contains data used to fine-tune the BERT model (Financial Phrasebank)
- Contains scripts showing how to freeze and unfreeze layers for fine-tuning, how to save the fine-tuned model, and how to load and use saved model for inference
- Contains a few different model files with slightly different archictectures
- Creating_A_FinBert_Saveable_Deeper.py contains the script to fine-tune final model  

#### defaultChartData -  
- Contains default chart data used to populate charts for landing page   

#### sageMakerSripts -  
- Contains files used within Amazon SageMaker
- Contains notebook with scripts showing how to load pre-trained TensorFlow model, create SageMaker endpoint for the model, and invoke the model endpoint to get predictions
- Contains an inference.py file used to process and tokenize the text data
- Contains a requirements.txt file for the inference.py file  

#### templates -  
- Contains main HTML template

#### application.py -  
- Main application file

#### combNewsPull.py -  
- Script used to pull and process data for both charts

#### inference.py -  
- Script containing tokenizer and processing func for SageMaker

#### lambdaFunction.py -  
- Amazon Lambda function used to invoke the Sagemaker endpoint

#### secondChartFuncs.py -  
- Contains funcs used to pull and process data for the individual charts only

#### requirements.txt -  
- requirements.txt file for application and Amazon Elastic Beanstalk

