# ABOUT

This application uses deep learning to perform sentiment analysis on financial news articles. It uses a BERT model (Bidirectional Encoder Representations from Transformers) fine-tuned on financial text for use in the financial domain. First, it extracts current news data for the specified companies and time window. Next, it processess the text data and feeds it into the BERT model to create sentiment scores. Also, optionally, it extracts and combines stock data with the corresponding news and sentiment data to create an average sentiment score for each time window. Finally, it uses Anychart, a Javascript charting libary, to present the data in a visually appealing and optimal way.  
#### View application at - http://newstest-env.eba-vgkkrtjs.us-west-1.elasticbeanstalk.com/

# Deployment and Technologies
•	Deployed a web application using AWS that pulls news and stock data, uses a deep learning model to perform sentiment analysis on it, and builds insightful visualizations  
•	Used Amazon SageMaker to create, host and deploy an endpoint for a pre-built fine-tuned BERT model  
•	Utilized serverless technology to invoke the model endpoint by creating a REST API and Lambda function using Amazon API Gateway and Amazon Lambda  
•	Built a web application around the model using Amazon Elastic Beanstalk, Flask, JavaScript, and multiple APIs  
