## AI Agents  #5 CrewAI Content Pipeline Agent

### **[.env 환경 파일 구성]** <br>
이전과 동일 <br>

### **[목표]** <br>
작성된 초안을 분석하여 검색 결과 상위 노출(SEO)과 콘텐츠 확산을 극대화 하도록 최적화 한다. 
최종덕으로 성과 분석 리포트와 함께 바로 게시 가능한 완성본 전달

<img width="496" height="655" alt="image" src="https://github.com/user-attachments/assets/e34c8b07-a406-4e5a-8cbc-66b7ce2a2e2e" />

### **[CrewAI의 Flow]** <br>
기존 프로젝트에서는 yaml 파일을 넣고 우리가 원하는 것을 입력해 넣어야 됐다. 
하지만 Flow는 이러한 에이전트와 그들의 작업을 어떻게, 언제 실행할지 제어하는 역할을 한다.  <br>

#### **plot() 이란?**

`plot()`은 Flow 내부에 정의된 **에이전트와 실행 흐름을 시각화**해주는 함수이다.
각 단계가 어떤 순서로 실행되는지, 어떤 Flow가 다음 단계로 이어지는지를 **그래프 형태로 확인**할 수 있다.

이를 통해
* Flow의 전체 구조를 한눈에 파악할 수 있고
* 실행 순서가 의도한 대로 구성되었는지 검증할 수 있으며
* 디버깅 및 구조 설계에 도움을 준다.
```python
flow = MyFirstFlow()
flow.plot()
```
해당 코드에 plot를 통해 생성한 파일 포함되어있음 브라우저에서 열면 확인가능 


### **[State 란?]** <br>
State는 Flow가 현재 어떤 콘텐츠를 만들고 있는지 알기 위해 사용하는 데이터 저장소이다.
Flow 자체는 데이터를 가지지 않으며, 각 단계(flow)에서 실행된 결과를 State에 저장한다.
이렇게 저장된 State는 다음 Flow로 전달되어 이후 작업에 활용된다.
즉, <br>
- Flow → 작업의 실행 순서와 제어만 담당
- State → 각 Flow에서 생성된 데이터를 저장하고 전달하는 역할

### **[참고_1]** <br>

CrewAI 실행 시 윈도우 환경에서는 일부 코드가 정상 동작하지 않아 **WSL(리눅스 환경)** 에서 실행함.  
해당 GitHub 코드는 WSL 환경에서는 실행 가능하며, 윈도우가 아닌 환경이라면 별도 설정 없이 실행 가능.(uv sync 필수)

### WSL 설치 방법

1. PowerShell 실행 후 WSL 설치
```bash
wsl --install
````

2. 설치 완료 후 재부팅
   (환경에 따라 재부팅이 필요 없을 수도 있음)

3. 프로젝트 경로로 이동

```bash
cd /mnt/c/Users/gkrud/Documents/content-pipeline-agent
```

4. Python 및 pip 확인 / 설치

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

5. 가상 환경 생성 및 활성화

* 가상 환경 생성

```bash
python3 -m venv .venv_wsl
```

* 가상 환경 활성화

```bash
source .venv_wsl/bin/activate
```

6. 라이브러리 설치

* requirements.txt 파일이 있는 경우

```bash
pip install -r requirements.txt
```

* requirements.txt 파일이 없는 경우

```bash
pip install crewai uv
``` 
 




