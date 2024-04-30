from flask import Flask, request, render_template
import os
import requests
import http.client
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clova Speech API 정보
CLOVA_SPEECH_SECRET_KEY = ''
CLOVA_SPEECH_INVOKE_URL = ''

# Clova Studio 요약 API 정보
CLOVA_STUDIO_HOST = ''
CLOVA_STUDIO_API_KEY = ''
CLOVA_STUDIO_API_KEY_PRIMARY_VAL = ''
CLOVA_STUDIO_REQUEST_ID = ''

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/summarization/v2/', json.dumps(completion_request), headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        
        # Check if the response body is not empty
        if not data:
            return {'error': 'Empty response from Clova Studio API'}

        result = json.loads(data)
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)

        # Check if 'status' key exists in the response and if the code is '20000'
        if 'status' in res and res['status'].get('code') == '20000':
            return res['result']['text']
        elif 'error' in res:
            return f"Error: {res['error']}"
        else:
            return 'Error: Unexpected response structure from Clova Studio API'

def convert_speech_to_text(file_url):
    headers = {'X-CLOVASPEECH-API-KEY': CLOVA_SPEECH_SECRET_KEY}
    data = {
        'url': file_url,
        'language': 'ko-KR',
        'completion': 'sync'
    }
    response = requests.post(f'{CLOVA_SPEECH_INVOKE_URL}/recognizer/url', headers=headers, json=data)
    return response.json().get('text', '')

def convert_speech_to_file(file_path):
    files = {'media': open(file_path, 'rb')}
    params = {
        'language': 'ko-KR',
        'completion': 'sync',
        'wordAlignment': True,
        'fullText': True
    }
    headers = {'X-CLOVASPEECH-API-KEY': CLOVA_SPEECH_SECRET_KEY}
    response = requests.post(f'{CLOVA_SPEECH_INVOKE_URL}/recognizer/upload', headers=headers, files=files, data={'params': json.dumps(params)})
    return response.json().get('text', '')

def _send_request(self, completion_request):
    ...
    result = json.loads(data)
    print("API Response:", result)  # 응답 출력
    ...


@app.template_filter('newline_list')
def newline_list(summary):
    # Replace ' -' with '<br> -' to create a line break before each list item, except for the first
    return summary.replace(' -', '<br> -')

# Apply the custom filter to the summary in the template with {{ summary|newline_list }}
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file_url = request.form.get('file_url')
        voice_file = request.files.get('voice_file')

        if voice_file and voice_file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], voice_file.filename)
            voice_file.save(filepath)
            speech_to_text_response = convert_speech_to_file(filepath)

        elif file_url:
            speech_to_text_response = convert_speech_to_text(file_url)

        else:
            return 'URL이나 파일이 제공되지 않았습니다.', 400

        summarization_executor = CompletionExecutor(
            host=CLOVA_STUDIO_HOST,
            api_key=CLOVA_STUDIO_API_KEY,
            api_key_primary_val=CLOVA_STUDIO_API_KEY_PRIMARY_VAL,
            request_id=CLOVA_STUDIO_REQUEST_ID
        )

        request_data = {
            "texts": [speech_to_text_response],
            "segMinSize": 300,
            "includeAiFilters": True,
            "autoSentenceSplitter": True,
            "segCount": -1,
            "segMaxSize": 1000
        }
        response_text = summarization_executor.execute(request_data)

        if response_text != 'Error':
            return render_template('result.html', text=speech_to_text_response, summary=response_text)
        else:
            return '요약 과정에서 오류가 발생했습니다.', 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
