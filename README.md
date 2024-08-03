## 配置环境
```
pip install requirement.txt -r
```

## 进行测试
运行main.py文件，在浏览器上打开http://127.0.0.1:8181
进行访问，如果想更改地址可以在main.py中的18行进行更改。通过访问
http://127.0.0.1:8181/docs
可以对接口进行测试

## 接口传入参数
现成的测试传入参数在moonapi.py中65-82行，测试的模型为moonshot所以需要更改的地方是model_api，
https://platform.moonshot.cn/console/api-keys
在此链接申请自己的api key。

## 传入参数的参考格式
![1722661500866](https://github.com/user-attachments/assets/e23a8ec7-bacc-4a01-881f-e1e458d70b23)
