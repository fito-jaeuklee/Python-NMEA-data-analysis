# Python-NMEA-data-analysis

### 1) 개발환경 설정

micropyGPS ( https://github.com/inmcm/micropyGPS ) 라는 사이트의 파싱 API를 사용하였기 때문에
관련 설치를 진행해야한다.

또는

폴더 안의 venv/ 를 활용하여 인터프리터를 설정해주면 별도의 설치 없이 진행이 가능하다.

```
python setup.py install
```

### 2) 사용 방법

사용자 기준에서 사용해야할 파일은 NMEA_value_save_main 이다.

실행하게 되면 폴더를 선택하는 창이 팝업.
폴더 안에는 분석할 하나의 .gp 파일만 있어야함. 폴더를 선택하고 오픈하면 NMEA decoding과 graph 파일이 저장됩니다.

![image](https://user-images.githubusercontent.com/66807112/125714538-1a2e4eff-20ab-41c6-8790-bf2fed270a86.png)

정상적으로 실행된다면, 하나의 폴더에 .gp 파일 / filtered.txt 파일 / png 파일이 저장되게 됩니다.

Example )

![image](https://user-images.githubusercontent.com/66807112/125714607-a1723dca-b2aa-4bce-b3ac-e8504974797b.png)

