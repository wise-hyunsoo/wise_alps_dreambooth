- 구글에서 제공하는 custom training prebuilt 컨테이너는 conda 환경에서 GPU 관련 코드가 돌아가고 있다.
- 따라서 poetry 파이썬 환경을 주입하지 않고, poetry.lock 으로부터 requirments.txt 을 생성하여 conda 환경에 인스톨한다.