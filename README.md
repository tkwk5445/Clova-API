## Clova-API
Clova Speech & Clova Studio API  
NCP Clova 에서 제공되는 API 를 통해 음성파일을 텍스트로 변환 후 요약하는 API 서비스 구축

- **Develop Tools** : VSCode  
- **Language** : Python 3.11.7, (HTML)  
- **Web Framework** : Flask 3.0.2  
- **Open API** : NCP Clova Speech, Clova Studio (summary)  
- **참조 가이드** :  
  [Clova Speech Guide](https://api.ncloud-docs.com/docs/ai-application-service-clovaspeech-longsentence)  
  [Clova Studio Guide](https://guide.ncloud-docs.com/docs/clovastudio-playground01#테스트앱생성)

---

## 작업 과정
1. 각 API 동작 확인
2. Clova Speech & Studio 요약 API 통합 사용
3. Flask 애플리케이션 구성 및 템플릿(index/result.html) 제작
4. 파일 업로드 기능 추가 및 최종 테스트

---

## 📆 2025.03.31 Release Note
1. Clova Speech 및 Clova Studio API 변수값 최신화
2. templates 파일 업데이트 (`index.html`, `result.html`)
3. Docker 리소스 업데이트 → `./clova_api_docker`  
   → 이미지 빌드 및 실행 가이드 포함

---

## 🐋 Docker 사용 가이드

```bash
# 1. 도커 이미지 빌드
docker build -t clova-api .

# 2. 컨테이너 실행 (포트 5000 사용)
docker run -d -p 5000:5000 --name clova-api-app clova-api

# 3. 브라우저에서 접속
http://localhost:5000
```

> 📌 실시간 로그 확인
```bash
docker logs -f clova-api-app
```

> 🧼 컨테이너 중지 및 삭제
```bash
docker stop clova-api-app && docker rm clova-api-app
```

---

## 🔧 기술 참고사항

- **실시간 로그 출력 지원**  
  → Dockerfile 내 `ENV PYTHONUNBUFFERED=1` 설정  
  → Python 코드 내 `print(..., flush=True)` 적용

- **Flask 서버 실행 안정성 강화**  
  → `app.run(debug=True, threaded=False, use_reloader=False)`  
  → 멀티스레드로 인한 로그 중복, 재시작 방지

---

## 📋 실행 로그 예시 (Console Output)

애플리케이션이 정상 동작할 경우 아래와 같은 로그가 출력됩니다:

```
Clova Speech API Response: {
  'result': 'COMPLETED',
  'message': 'Succeeded',
  ...
}

Executing summarization request...
Sending request to Clova Studio API with data: { ... }

Clova Studio API Response: {
  'status': {'code': '20000', 'message': 'OK'},
  'result': {'text': '- 심사를 할 때 가장 중요하게 보는 부분은 창의성임 ...'}
}

Final summary to render: - 심사를 할 때 가장 중요하게 보는 부분은 창의성임 ...
```

> 위 로그는 Flask 내부 `print(..., flush=True)` 출력이며, `docker logs` 명령어로 실시간 확인 가능

---

## 서비스 화면 (index.html)
![image](https://github.com/user-attachments/assets/46c6c22d-31d3-4175-b922-40737efc1202)

---

## 결과 화면 (result.html)
![image](https://github.com/user-attachments/assets/9ac930ef-b72c-4ce8-b48f-6059af3794c4)


---

## 👨‍💻 제작자
정욱진 (Jung Wookjin)
