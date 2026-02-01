from pydantic import BaseModel, ConfigDict

# 모든 Pydantic 모델이 외부 타입을 허용하도록 설정
BaseModel.model_config = ConfigDict(arbitrary_types_allowed=True)
def main():
    print("Hello from email-refiner-agent!")


if __name__ == "__main__":
    main()
