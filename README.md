# KBCNN_KBC
## 개요
주어진 지식그래프를 바탕으로 [카이스트 전산학과](https://cs.kaist.ac.kr/) 김지호 석사학위논문 (2018) 에 기술된 지식베이스 완성 모델인 KBCNN 모델을 학습하고, 학습된 모델을 바탕으로 지식을 검증할 수 있는 모듈입니다.
크게 두 가지 모듈로 구성되어 있습니다.
* 모델 학습 모듈
  * 지식그래프, 모델 종류, 하이퍼매개변수를 입력으로 받아 해당 지식그래프를 전처리 합니다.
  * 전처리된 지식그래프를 바탕으로 지식베이스 완성 모델을 학습합니다.
  * 완성 모델에 대한 각 관계별 threshold를 계산합니다.
* 지식 검증 모듈
  * 모델 학습 모듈에서 학습된 모델을 기반으로 입력된 지식들의 참/거짓을 검증합니다.

## 환경설정
* 본 모듈은 python 3 기반으로 구현되었습니다.
* 다음 명령어를 통해 필요한 python 라이브러리들을 설치해 주세요.
  * 'pip install -r requirements.txt'

* SWRC kbox.kaist.ac.kr 서버에서 실행할 경우
```
cd /home/iterative/
python3 run.py
python3 validate.py
```


## 모델 학습 모듈

### 모델 학습 환경설정
모델 학습 환경은 [run_config.json](run_config.json) 파일에서 설정합니다.
```
{
  "input":{
    "training_data": "data/raw_KG/result_changed_only.tsv",
    "model": "KBCNN",
    "hyperparam":{
      "embedding_dimensions": 75,
      "dropout": 0.2,
      "epochs": 50,
      "batch_size": 256,
      "learning_rate": 0.001,
      "number_of_filters": 50,
      "negative_sample_ratio": 5
    }
  },
  
  "output":{
    "data_dir": "data/KG/KBOX-iterative-T1/",
    "model_output":"models/KBOX-iterative-T1.h5",
    "thresholds_output":"thresholds/T1_thresholds.txt"
  }
}
```
* input
  * training_dir: 학습을 진행할 지식그래프 파일의 경로
  * model: 학습을 진행할 모델 종류 (ConvKB, KBCNN 중 택 1)
  * hyperparam: 학습에 사용할 하이퍼매개변수들
    * embedding_dimensions: 개체 및 관계의 임베딩 차원 (주로 50, 75, 100, 200 중 택 1)
    * dropout: Dropout 수치 (주로 0.1 ~ 0.3)
    * epochs: 학습이 진행되는 횟수. 학습 데이터의 모든 삼항관계과 그에 대응하는 거짓 삼항관계들에 대해서 한 번씩 학습한 것이 1 epoch (주로 30 ~ 100)
    * batch_size: 한 배치에 포함되는 참 삼항관계의 개수 (주로 125, 256 중 택 1)
    * learning_rate: 학습 속도 (주로 0.0005, 0.001 중 택 1)
    * number_of_filters: 컨볼루션 레이어의 필터 개수 (주로 50, 75, 100 중 택 1)
    * negative_sample_ratio: 학습용 참 삼항관계 하나당 같이 학습되는 거짓 삼항관계의 개수 (주로 1 ~ 10 사이의 자연수)
* output
  * data_dir: 전처리된 지식그래프가 저장될 경로 (폴더명)
  * model_output: 학습된 모델이 저장될 파일명. 확장자는 반드시 '.h5' 로 지정해 주세요.
  * thresholds_output: 각 관계별 threshold가 저장될 파일명. (txt 혹은 tsv 중 택 1)

### 실행
다음과 같이 [run.py](run.py) 파일을 실행하여 결과를 추출할 수 있습니다.
```
python run.py
```

### 출력 파일
* 환경설정 파일 [run_config.json](run_config.json)의 output/data_dir 경로에 다음과 같은 파일들이 저장됩니다.
지식그래프의 개체별 ID: [data/KG/KBOX-iterative-T1/ent2id.txt](data/KG/KBOX-iterative-T1/ent2id.txt)
```
수륜중학교 0
마키타_가즈히사  1
J.G._허츨러  2
한국뮤지컬대상 3
무티아_오르키아  4
```
지식그래프의 관계별 ID: [data/KG/KBOX-iterative-T1/rel2id.txt](data/KG/KBOX-iterative-T1/rel2id.txt)
```
routeStart  0
combatant 1
restingPlace  2
influencedBy  3
artist  4
```
지식그래프의 트리플 중 학습용 데이터: [data/KG/KBOX-iterative-T1/train.txt](data/KG/KBOX-iterative-T1/train.txt)
```
주찬권 genre 포크_록
윌리엄_라이언_매켄지_킹 occupation  언론인
마치다_고지로 position  외야수
친일인명사전  developer 민족문제연구소
천천고등학교  type  공립
```
지식그래프의 트리플 중 평가용 데이터: [data/KG/KBOX-iterative-T1/test.txt](data/KG/KBOX-iterative-T1/test.txt)
```
돌궐어 country 회흘
일본잎갈나무  order 구과목
효익태후  successor 효장예황후
사이킥_러버  bandMember  YOFFY
다나카_가쿠에이  predecessor 사토_에이사쿠
```

* 환경설정 파일 [run_config.json](run_config.json)의 output/model_output 파일명에 학습된 지식그래프 완성 모델이 저장됩니다.
* 환경설정 파일 [run_config.json](run_config.json)의 output/thresholds_output 파일명에 관계별 threshold가 저장됩니다.
학습된 모델의 각 관계별 threshold: [thresholds/T1_thresholds.txt](thresholds/T1_thresholds.txt)
```
routeStart  0.5003
combatant 0.4840
restingPlace  0.4650
influencedBy  0.4905
```


## 지식 검증 모듈
### Input
지식 검증 환경은 [validate_config.json](validate_config.json) 파일에서 다음과 같이 설정합니다.
```
{
  "input":{
    "KG": "data/KBOX-iterative-T1/",
    "validate_file": "data/validation/filtered_pa_DRcheck.tsv",
    "model": "models/KBOX-iterative-T1.h5_epochs_30.h5",
    "thresholds": "thresholds/T1_thresholds.txt"
  },
  
  "output":{
    "classified_file": "results/KBOX-iterative-T1/pa_labeled.tsv",
    "no_ent_or_rel_file": "results/KBOX-iterative-T1/pa_unlabeled.tsv"
  }
}
```
* input
  * KG: 사용할 모델이 학습된 전처리된 지식그래프의 경로. 모델 학습 모듈에서 output/data_dir에 해당하는 폴더명을 기입하세요.
  * validate_file: 검증할 지식 파일.
  * model: 지식 검증에 사용할 학습된 모델. (.h5 확장자) 모델 학습 모듈에서 output/model_output 파일명을 기입하세요.
  * thresholds: 각 관계별 thresholds 파일. 모델 학습 모듈에서 output/thresholds_output 파일명을 기입하세요.
* output
  * classified_file: 입력된 지식에 대한 검증 결과 파일. 지식의 개체 및 관계가 input/KG에 정상적으로 포함되어 있는 경우가 저장될 파일명.
  * no_ent_or_rel_file: 입력된 지식 중 개체 혹은 관계가 input/KG에 포함되어 있지 않아 검증이 불가능한 경우가 저장될 파일명.
반드시 사용하는 모델에 맞는 KG, thresholds를 사용하세요.

input/validate_file 파일 형식: [data/validation/filtered_pa_DRcheck.tsv](data/validation/filtered_pa_DRcheck.tsv)
```
새누리당  headquarter 진도_(섬)
세타트 largestCity 마라케시
세르비아인 populationPlace 크로아티아
```

### 실행
다음과 같이 [validate.py](validate.py) 파일을 실행하여 결과를 추출할 수 있습니다.
```
python validate.py
```

### Output
output/classified_file: [results/KBOX-iterative-T1/pa_labeled.tsv](results/KBOX-iterative-T1/pa_labeled.tsv)
```
새누리당  headquarter 진도_(섬)  x 0.3598
세타트 largestCity 마라케시  o 0.5037
라바트 largestCity 세타트 o 0.5037
박병호_(1986년) birthPlace  미네소타_주  x 0.28
조선로동당 headquarter 평창군 x 0.1926
```
각 지식의 sbj, rel, obj, label, score가 탭으로 구분되어 출력됩니다.
label은 영어 소문자 o, x중 하나. score는 0에서 1사이의 범위입니다.

output/no_ent_or_rel_file: [results/KBOX-iterative-T1/pa_unlabeled.tsv](results/KBOX-iterative-T1/pa_unlabeled.tsv)
```
세르비아인 populationPlace 크로아티아
전라남도  leaderName  박원순
미국인 populationPlace 영국
유대인 populationPlace 솜보르
박영효 nationality 조선
```
각 지식의 sbj, rel, obj가 탭으로 구분되어 출력됩니다.


## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST

## Contact
Jiho Kim. `hogajiho@kaist.ac.kr`, `hogajiho@gmail.com`

## Acknowledgement
This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2013-0-00109, WiseKB: Big data based self-evolving knowledge base and reasoning platform)