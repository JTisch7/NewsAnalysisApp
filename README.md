# NewsAnalysisApp

This application uses
deep learning to perform sentiment analysis on financial news articles.  It uses a BERT model 
(Bidirectional Encoder Representations from Transformers) fine-tuned on financial text
for use in the financial domain.  First, it extracts current news data for the specified companies and time window.
Next, it processess the text data and feeds it into the BERT model to create sentiment scores. 
Optionally, it extracts and combines stock data with the corresponding news and sentiment data
to create an average sentiment score for each time window. Finally, it uses Anychart, a Javascript charting libary, 
to present the data in a visually appealing and optimal way.
