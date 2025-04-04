# Side Project
## Clova-API
Clova Speech & Clova Studio API  
수행 기간 : 2/8 ~ 2/13  
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

## 📦 2025.03.31 Release Note
1. Clova Speech 및 Clova Studio API 변수값 최신화
2. templates 파일 업데이트 (`index.html`, `result.html`)
3. Docker 리소스 업데이트 → `./clova_api_docker`  
   → 이미지 빌드 및 실행 가이드 포함

---

## 🐳 Docker 사용 가이드
