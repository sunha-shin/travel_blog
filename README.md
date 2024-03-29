# travel_blog
## 소개
  이 여행 블로그는 개인적인 여행 기록과 사진을 저장하기 위한 웹사이트입니다. 이 프로젝트는 Django 웹 프레임워크를 사용하여 구축되었습니다.


## 기능
- 게시글 작성 및 관리: 여행한 나라, 도시, 내용, 날짜, 사진, 댓글을 포함한 게시글을 작성하고 관리할 수 있습니다.
- 댓글 기능: 다른 사용자의 게시글에 댓글을 달아 소통할 수 있습니다.
- 사용자 인증: 사용자 등록, 로그인, 로그아웃 기능을 통해 개인화된 경험을 제공합니다.


## 서비스 URL 정보
- blog github repo: https://github.com/sunha-shin/travel_blog
    
## WBS
```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       프로젝트 일정

    section 리포지토리 생성
    리포지토리 생성         :2024-03-07, 1d

    section WBS 작성
    WBS 작성               :2024-03-07, 1d

    section 프로젝트 아이디어 기획
    프로젝트 아이디어 기획  :2024-03-07, 1d

    section 와이어프레임
    와이어프레임            :2024-03-07, 2024-03-08

    section ERD
    ERD                    :2024-03-08, 1d

    section URL 구현
    URL 구현               :2024-03-08, 1d

    section 모델 구현
    모델 구현              :2024-03-09, 3d

    section CRUD 구현
    CRUD 구현              :2024-03-09, 3d

    section 인증 구현
    인증 구현              :2024-03-09, 3d


```

## URL 구조
```mermaid
graph TD;  
    A[홈페이지] -->|accounts/register/| D[회원가입]
    A -->|accounts/login/| B[로그인]
    A -->|accounts/logout/| C[로그아웃]    
    A -->|blog/| E[블로그 목록 화면]
    E -->|blog/create/| F[블로그 작성]
    E -->|blog/<int:pk>/| G[블로그 세부]
    G -->|blog/<int:pk>/edit/| H[블로그 수정]
    G -->|blog/<int:pk>/delete/| I[블로그 삭제]
    E -->|blog/search/| J[블로그 검색]
    E -->|blog/comment/<int:pk>/delete/| K[댓글 삭제]

    style C fill:#f99,stroke:#333,stroke-width:2px;
    style K fill:#f99,stroke:#333,stroke-width:2px;
    style H fill:#f99,stroke:#333,stroke-width:2px;
    style I fill:#f99,stroke:#333,stroke-width:2px;
    style F fill:#f99,stroke:#333,stroke-width:2px;
```

## DB 테이블 구조도
```mermaid
erDiagram
    USER {
        id INT[PK]
        username VARCHAR
        password VARCHAR
        email VARCHAR
        first_name VARCHAR
        last_name VARCHAR
        date_joined DATETIME
        last_login DATETIME
        is_superuser BOOLEAN
        is_staff BOOLEAN
        is_active BOOLEAN
        nickname VARCHAR
    }
    COMMENT {
        id INT[PK]
        author_id INT[FK]
        post_id INT[FK]
        content TEXT
        created_at DATETIME
    }

    POST {
        id INT[PK]
        title VARCHAR
        contents TEXT
        main_image VARCHAR
        author_id INT[FK]
        country VARCHAR
        city VARCHAR
        date_of_visit DATE
        created_at DATETIME
        updated_at DATETIME
    }

    IMAGE {
        id INT[PK]
        post_id INT[FK]
        image VARCHAR
    }

    USER ||--o{ COMMENT : "authored"
    POST ||--o{ COMMENT : "has"
    USER ||--o{ POST : "authored"
    POST ||--o{ IMAGE : "has"
```
## 화면 정의서
| 메인화면|특징|
|---------------------------------|--------------------------------------------------|
|![이미지1](img/01_Main.jpg) |검색, 블로그 리스트, 로그인/회원가입 기능이 한페이지에 보임|

| 나라검색|도시검색|
|---------------------------------|--------------------------------------------------|
|![이미지2](img/02_나라%20검색.jpg) |![이미지3](img/03_도시%20검색.jpg) |

| 로그인|로그인 후|
|---------------------------------|--------------------------------------------------|
|![이미지4](img/04_로그인.jpg) |![이미지5](img/05_로그인%20후.jpg) |

| 로그인 후 글쓰기|블로그 디테일|
|---------------------------------|--------------------------------------------------|
|![이미지6](img/06_로그인%20후%20글쓰기.jpg) |![이미지7](img/07_블로그%20디테일.jpg) |

| 로그인 후 댓글란|로그아웃 후 메인화면|
|---------------------------------|--------------------------------------------------|
|![이미지8](img/08_Copy%20of%20블로그%20디테일.jpg) |![이미지9](img/09_Copy%20of%20Main.jpg) |

| 로그아웃 후 댓글창|로그아웃 후 댓글창|
|---------------------------------|--------------------------------------------------
|![이미지10](img/12_로그아웃%20후%20블로그%20디테일.jpg) |![이미지11](img/11_로그아웃%20후%20댓글창.jpg)|



## 트러블슈팅 히스토리
1. field의 유효성 검사를 통과하지 못하는 경우
      * form에서 '__all__'을 사용하기 X
```
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2', 'field3']  # 필요한 필드만 지정

# 사용 X
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = '__all__'
        exclude = ['field4', 'field5', 'field6']  # 제외할 필드 지정

보통 author 기본적으로 user의 이름X, id 정수 값.
post = Post(title='제목', content='내용', author_id=request.user.id)
post.save()
```

2. 저장한 이미지를 불러오지 못할 때: 
    * settings.py확인하고, urlpatterns 확인. 이미지의 URL로 바로 접속할 수 있는지 admin에서 확인
  
3. User 필드를 건드리다가 DB가 엉켰을 경우
    * migrations폴더에 0001 이렇게 넘버링 된 것을 다 지우고
    * sqlite3 파일을 지운 후
    * 다시 makemigrations와 migrate 실행