# Payhere 과제
## 사용기술
---
FastAPI, JWT, MySQL

## 요구사항
---
- [x] 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다. 
- [x] 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다. 
- [x] 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다. 
- [x] 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
- [x] 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다. 
- [x] 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
- [x] 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
- [x] 가계부의 세부 내역을 복제할 수 있습니다.
- [x] 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.

## API_list
---

<img width="1831" alt="스크린샷 2023-01-09 오후 11 40 47" src="https://user-images.githubusercontent.com/70617238/211334176-1930e0eb-6b38-4041-8d2f-b439a9c562c4.png">


## 기능 구현 방식
---
* 로그인과 로그아웃은 JWT를 활용하여 진행했습니다.
* 로그아웃의 경우 refresh token을 활용했습니다.
  * 로그인이 필요한 모든 API에는 사용자의 expire time을 deps.get_current_user_authorizer()를 활용해 검사합니다.
  * 로그인시 access token 과 refresh token을 발행합니다.
  * 로그인시 user.expire_time에 refresh token expire time 주입합니다.
  * 로그인시 user.refresh_token에 refresh token을 주입합니다.
  * 로그아웃시 user.expire_time을 현재 시간으로 변경합니다.
  * access token의 만료 시간은 60 * 24 * 8 즉 8일, refresh token은 30일 입니다.
  * access token 만료시 refresh token으로 access token을 재발급 받을 수 있습니다.
  (Redis를 활용하지 않고 구현할 수 있는 방식)
* spring의 filter를 모방한 get_current_user_authorizer()를 구현해 사용했습니다.
* 가계부 삭제는 완전히 db에서 삭제하지 않고 is_deleted 필드를 True로 변경해 삭제된 것처럼 보이게 했습니다.
* 단축 URL의 만료 시간은 10분 입니다.
* 단축 URL 생성시 특정 그 가계부 내역은 접근 권한 없이 접근이 가능합니다.
* 세부 내역 복제는 pyperclip을 활용했습니다.
* 익숙한 MVC방식으로 먼저 코드를 작성한 후 fastAPI 디렉터리 형식으로 리팩터링을 진행했습니다.

## DB 연관관계
---
![histories](https://user-images.githubusercontent.com/70617238/211337004-c11b9d2f-536a-463d-a6d0-4c1b3b6eb4fc.png)


## 사용방법
---
저장된 .env 파일에 MYSQL dbname, user, pw 등을 입력후 실행



  
