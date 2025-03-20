import azure.functions as func
import logging, json
from datetime import datetime
from sentiment_analysis import detect_text_language, analyse_sentiment

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="serverlessSentimentAnalysisAPI")
def serverlessSentimentAnalysisAPI(req: func.HttpRequest) -> func.HttpResponse:
    start_time = datetime.now()
    logging.info('Azure function invoked for sentiment analysis request!!!')

    name = req.params.get('name')
    analyze_text = req.params.get('analyzeText')
    if not name or analyze_text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            analyze_text = req_body.get('analyzeText')

    if name and analyze_text:

        text_language, remark, status_code = detect_text_language(analyze_text)

        if status_code == 200:
            sentiment, scores, remark, status_code = analyse_sentiment(analyze_text)
                
        json_format = {"requested_user" : name,
                       "input_text" : analyze_text,
                       "text_language" : text_language,
                       "text_sentiment" : sentiment,
                       "text_scores" : {
                           "positive" : scores['pos'],
                           "neutral" : scores['neu'],
                           "negative" : scores['neg'],
                           "overall" : scores['compound']
                       },
                       "remarks" : remark
                       }
        final_response = func.HttpResponse(json.dumps(json_format),
                                           status_code=status_code,
                                           mimetype="application/json")
        
        end_time = datetime.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        logging.info(f"Sentiment analysis request successfully processed in {duration_ms:.2f}ms. Response JSON -> {final_response.get_body()}")
        return final_response
    else:
        return func.HttpResponse(
             json.dumps({"error": "Invalid request: 'name' and 'analyzeText' parameters are required either in the query string or the request body to perform sentiment analysis."}),
             status_code=400,
             mimetype="application/json"
        )