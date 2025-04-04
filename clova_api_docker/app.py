from flask import Flask, request, render_template
import os
import requests
import http.client
import json

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'  # 임시 폴더로 변경
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clova Speech API 정보
CLOVA_SPEECH_SECRET_KEY = ''
CLOVA_SPEECH_INVOKE_URL = 'https://clovaspeech-gw.ncloud.com/external/v1/'

# Clova Studio 요약 API 정보
CLOVA_STUDIO_HOST = 'clovastudio.stream.ntruss.com'
CLOVA_STUDIO_API_KEY = ''
CLOVA_STUDIO_REQUEST_ID = ''

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def _send_request(self, completion_request):
        print("Sending request to Clova Studio API with data:", completion_request, flush=True)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/summarization/v2', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        print("Clova Studio API Response:", result, flush=True)
        return result

    def execute(self, completion_request):
        print("Executing summarization request...", flush=True)
        res = self._send_request(completion_request)
        if res.get('status', {}).get('code') == '20000':
            return res['result']['text']
        else:
            return f"Error: {res}"

def convert_speech_to_text(file_url):
    headers = {'X-CLOVASPEECH-API-KEY': CLOVA_SPEECH_SECRET_KEY}
    data = {
        'url': file_url,
        'language': 'ko-KR',
        'completion': 'sync'
    }
    response = requests.post(f'{CLOVA_SPEECH_INVOKE_URL}/recognizer/url', headers=headers, json=data)
    response_json = response.json()
    print("Clova Speech API Response:", response_json, flush=True)
    return response_json.get('text', '')

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
    response_json = response.json()
    print("Clova Speech API Response:", response_json, flush=True)
    return response_json.get('text', '')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file_url = request.form.get('file_url')
        voice_file = request.files.get('voice_file')

        if voice_file and voice_file.filename != '':
            filepath = os.path.join('/tmp', voice_file.filename)  # 파일을 임시 디렉토리에 저장
            voice_file.save(filepath)
            speech_to_text_response = convert_speech_to_file(filepath)
            os.remove(filepath)  # 파일 변환 후 삭제
        elif file_url:
            speech_to_text_response = convert_speech_to_text(file_url)
        else:
            return 'URL이나 파일이 제공되지 않았습니다.', 400

        summarization_executor = CompletionExecutor(
            host=CLOVA_STUDIO_HOST,
            api_key=CLOVA_STUDIO_API_KEY,
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

        if not response_text.startswith('Error'):
            print("Final summary to render:", response_text, flush=True)
            return render_template('result.html', text=speech_to_text_response, summary=response_text)
        else:
            return '요약 과정에서 오류가 발생했습니다.', 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=False, use_reloader=False)

