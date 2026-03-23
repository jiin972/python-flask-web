
### Python과 Flask Framework을 이용한 웹사이트 구축 연습

#### 개요
Python과 Flask를 활용해 웹 스크래퍼 서버를 구축하는 실습 프로젝트.
Wanted 채용공고를 키워드로 검색하고, 결과를 CSV로 다운로드할 수 있다.

#### 상세

- 키워드로 Wanted 채용공고 검색
- 검색 결과 서버 메모리에 캐싱 (동일 키워드 재요청 시 DB 조회 없이 반환)
- 검색 결과 CSV 파일로 Export 및 다운로드

#### 사용된 기술 스택

| 분류 | 기술 |
|---|---|
| Language | Python 3.11 |
| Framework | Flask |
| 스크래핑 | Playwright, BeautifulSoup4 |
| 템플릿 | Jinja2 (HTML) |
| 기타 | CSV 파일 생성, 인메모리 캐싱 |

