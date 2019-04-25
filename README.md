# KBCNN_KBC
## 개요
주어진 지식그래프를 바탕으로 [카이스트 전산학과](https://cs.kaist.ac.kr/) 김지호 석사학위논문 (2018) 에 기술된 지식베이스 완성 모델인 KBCNN 모델을 학습하고, 학습된 모델을 바탕으로 지식을 검증할 수 있는 모듈입니다.
크게 세 가지 모듈로 구성되어 있습니다.
* 모델 학습 모듈
  * 지식그래프, 모델 종류, 하이퍼매개변수를 입력으로 받아 해당 지식그래프를 전처리 합니다.
  * 전처리된 지식그래프를 바탕으로 지식베이스 완성 모델을 학습합니다.
  * 완성 모델에 대한 각 관계별 threshold를 계산합니다.
* 지식 검증 모듈
  * 모델 학습 모듈에서 학습된 모델을 기반으로 입력된 지식들의 참/거짓을 검증합니다.
* 지식 검증 서비스 모듈
  * REST API를 이용한 실시간 서비스를 제공합니다.

## 환경설정
* 본 모듈은 python 3 기반으로 구현되었습니다.
* 다음 명령어를 통해 필요한 python 라이브러리들을 설치해 주세요.
  * 'pip install -r requirements.txt'

* SWRC kbox.kaist.ac.kr 서버에서 실행할 경우 실행 명령 앞에 다음과 같이 sudo 명령어를 붙여 주세요.
```
cd /home/iterative/KV
sudo python3 run.py
sudo python3 validate.py
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
    * batch_size: 한 배치에 포함되는 참 삼항관계의 개수 (주로 128, 256 중 택 1)
    * learning_rate: 학습 속도 (주로 0.0005, 0.001 중 택 1)
    * number_of_filters: 컨볼루션 레이어의 필터 개수 (주로 50, 75, 100 중 택 1)
    * negative_sample_ratio: 학습용 참 삼항관계 하나당 같이 학습되는 거짓 삼항관계의 개수 (주로 1 ~ 10 사이의 자연수)
* output
  * data_dir: 전처리된 지식그래프가 저장될 경로 (폴더명)
  * model_output: 학습된 모델이 저장될 파일명. 확장자는 반드시 '.h5' 로 지정해 주세요.
  * thresholds_output: 각 관계별 threshold가 저장될 파일명. (txt 혹은 tsv 중 택 1)

모델 별 KDB2016-137 데이터셋에 대한 최적의 hyperparameter는 아래 표와 같습니다.

모델 | KBCNN | ConvKB
embedding_dimensions | 75 | 100
dropout | 0.2 | 0.2
epochs | 50 | 75
batch_size | 256 | 256
learning_rate | 0.001 | 0.001
number_of_filters | 50 | 75
negative_sample_ratio | 5 | 5

### 실행
다음과 같이 [run.py](run.py) 파일을 실행하여 결과를 추출할 수 있습니다.
```
python3 run.py
```
run.py는 다음과 같은 세 가지 프로세스를 실행하게끔 되어 있습니다.
1. 전처리 단계
```
python3 preprocess.py
```
2. 학습 단계
```
python3 train.py
```
3. Threshold 계산 단계
```
python3 threshold.py
```
각 단계는 개별적으로 실행해도 상관이 없으며, [run_config.json](run_config.json) 파일의 설정에 따라 각 단계가 실행됩니다.
예를 들어, 동일한 지식그래프를 사용하여 학습 단계만 진행하고 싶을 경우 전처리 단계와 Threshold 계산 단계를 같이 진행할 필요가 없기 때문에 학습 단계에 해당하는 [train.py](train.py) 파일만 실행시키면 됩니다.

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
    "KG": "data/KG/KBOX-iterative-T1/",
    "validate_file": "data/validation/filtered_pa_DRcheck.tsv",
    "model": "models/KBOX-iterative-T1.h5",
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


## 지식 검증 서비스 모듈

### Input
지식 검증 서비스 모듈은 지식 검증을 실시간으로 REST API로 제공하는 역할을 합니다.
[service_config.json](service_config.json) 에서 다음과 같은 항목들을 설정하고 서비스를 실행하세요.
```
{
  "KG": "data/KG/KBOX-iterative-T1/",
  "model": "models/KBOX-iterative-T1.h5",
  "thresholds": "thresholds/T1_thresholds.txt"
}
```
* KG: 사용할 모델이 학습된 전처리된 지식그래프의 경로. 모델 학습 모듈에서 output/data_dir에 해당하는 폴더명을 기입하세요.
* model: 지식 검증에 사용할 학습된 모델. (.h5 확장자) 모델 학습 모듈에서 output/model_output 파일명을 기입하세요.
* thresholds: 각 관계별 thresholds 파일. 모델 학습 모듈에서 output/thresholds_output 파일명을 기입하세요.

### 실행
다음과 같이 [service.py](service.py) 파일을 실행하여 서비스를 실행해 주세요.
```
python3 service.py
```

service.py의 line 6,7에 다음 변수들을 바꾸어 서비스 실행 host 및 port를 변경할 수 있습니다.
```
host_addr = '143.248.135.20'
port_num = 2848
```

## Ranked List 함수 사용 방법
[eval.py](eval.py)의 Ranking 클래스를 import해서 사용한다.
사용 예시는 다음과 같다.

```
import sys
sys.path.insert(0, "/Users/jiho/Desktop/KV")

from KV import eval

if __name__ == "__main__":

    dataset = "KV/data/KG/KBOX-iterative-T1/"
    model_name = "KV/models/KBOX-iterative-T1.h5"
    Rank = eval.Ranking(dataset, model_name)

    sample1 = [u'친일인명사전', u'developer', u'민족문제연구소']
    sample2 = [u'그_남자가_아내에게', u'language', u'일본어']

    print(Rank.ranked_list(sample1))
    print(Rank.ranked_list(sample2))
```
위 코드의 결과는 다음과 같다.
```
([(['친일인명사전', 'developer', '경기도의회'], 0.98301320075988774), (['친일인명사전', 'developer', '정치평론'], 0.89146239757537837), (['친일인명사전', 'developer', '야힘_토폴'], 0.86009025573730469), (['친일인명사전', 'developer', '가족오락관'], 0.84637665748596191), (['친일인명사전', 'developer', '롄윈강_시'], 0.81618168354034426), (['친일인명사전', 'developer', '네덜란드_상원'], 0.80956287384033199), (['친일인명사전', 'developer', '슬픈_발걸음_(구두_II)'], 0.7865900993347168), (['친일인명사전', 'developer', '쇼핑왕_루이'], 0.78351573944091801), (['친일인명사전', 'developer', '베르나르_퐁트넬'], 0.77177839279174809), (['친일인명사전', 'developer', 'CUPID'], 0.77089915275573728)], 2376)
([(['무서운_영화_4', 'language', '네덜란드_상원'], 1), (['무서운_영화_4', 'language', '베르나르_퐁트넬'], 1), (['무서운_영화_4', 'language', '야힘_토폴'], 1), (['무서운_영화_4', 'language', '롄윈강_시'], 0.88902096748352055), (['무서운_영화_4', 'language', '슬픈_발걸음_(구두_II)'], 0.83662319183349609), (['무서운_영화_4', 'language', '이철승'], 0.82566900253295894), (['무서운_영화_4', 'language', '하늘이_부를_때까지'], 0.810185718536377), (['무서운_영화_4', 'language', '경기도의회'], 0.8000763416290283), (['무서운_영화_4', 'language', '의창군'], 0.79908056259155269), (['무서운_영화_4', 'language', '정치평론'], 0.796247410774231)], 198952)
```
각 트리플에 대해서 Filtered ranking list를 생성한 뒤 상위 10개의 트리플과 각각의 점수가 담긴 list, 그리고 input 트리플의 ranking을 출력한다.

Ranking class의 ranked_list 함수를 사용하면 되는데, 해당 함수의 선언은 다음과 같다.
```
def ranked_list(self, triple, left_flag=True, filtered_flag=True, listlen=10):
```
* triple: utf-8 으로 encoding된 길이 3의 list/tuple.
* left_flag: True면 obj 자리에 구멍을 뚫는 ranked_list, False 면 sbj 자리에 구멍을 뚫는 ranked list가 출력된다. Default == True
* filtered_flag: True면 Filtered Setting을 사용하여 ranked list를 생성
* listlen: 반환할 ranked list의 길이. Default == 10
  * listlen을 -1로 설정할 경우 ranked list 전체를 반환하게 된다.


## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST

## Contact
Jiho Kim. `hogajiho@kaist.ac.kr`, `hogajiho@gmail.com`

## Acknowledgement
This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2013-0-00109, WiseKB: Big data based self-evolving knowledge base and reasoning platform)