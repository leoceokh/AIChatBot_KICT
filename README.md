# 오은영 박사 AI 상담소
이 프로젝트는 오은영 박사의 상담 AI 챗봇 서비스입니다. Flask를 사용하여 백엔드를 구현하고, HTML, CSS, JavaScript를 사용하여 프론트엔드를 구현했습니다.

## 주요 기능
- AI 챗봇을 통한 상담 서비스
- 오은영 박사의 YouTube 영상 추천
- 새로운 대화 시작 기능

## 프로젝트 구조
```
├── app.py
├── templates
│ └── index.html
├── .env
├── .gitignore
├── requirements.txt
└── README.md
 ```

## 설치 및 실행 방법
1. 저장소를 클론합니다:
   ```
   git clone [저장소 URL]
   cd [프로젝트 디렉토리]
   ```
   
2. 가상 환경을 생성하고 활성화합니다:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

4. `.env` 파일을 생성하고 필요한 API 키를 설정합니다:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

5. 애플리케이션을 실행합니다:
   ```
   python app.py
   ```

6. 웹 브라우저에서 `http://localhost:5000`으로 접속합니다.

7. ## 주의사항

- `.env` 파일에 있는 API 키를 공개하지 않도록 주의해주세요.
- `requirements.txt` 파일을 최신 상태로 유지해주세요.

![image](https://github.com/user-attachments/assets/1540502b-3b12-47b2-9f75-86f11136f89c)


