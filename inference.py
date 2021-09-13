from transformers import BertTokenizer
import json

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
MAX_SEQ_LEN=100

def input_handler(data, context):
    data_str = data.read().decode()
    text_before_tokenization = json.loads(data_str)

    #create lists for encoded inputs
    def getTokens(sentence):
        encoded_new = tokenizer.encode_plus(
                                            sentence,                      
                                            add_special_tokens = True,  
                                            padding = 'max_length',
                                            max_length = MAX_SEQ_LEN,             
                                            truncation=True,
                                            return_attention_mask = True,     
                                            #return_tensors = 'tf'        
                                            )
        input_token = encoded_new['input_ids']
        masked_token = encoded_new['attention_mask']


        return input_token, masked_token
    
    
    tokenList = []
    for line in text_before_tokenization['instances']:
        #encode training inputs
        input_token, masked_token = getTokens(line['text'])
        transformed_instance = {"input_token": input_token, "masked_token": masked_token}
        tokenList.append(transformed_instance)
        

    transformed_data = {"instances": tokenList}

    return json.dumps(transformed_data)



def output_handler(response, context):
    response_content_type = context.accept_header
    return json.dumps(response.json()), response_content_type
