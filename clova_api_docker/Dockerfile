FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일 복사
COPY . .

# 로그 버퍼링 비활성화 (print 즉시 출력)
ENV PYTHONUNBUFFERED=1

# 시간대 설정
ENV TZ=Asia/Seoul

# Flask 실행
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--no-reload", "--without-threads"]

