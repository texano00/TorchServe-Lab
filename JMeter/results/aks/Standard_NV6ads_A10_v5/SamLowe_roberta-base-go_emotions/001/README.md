# Configuration



```
# config.properties
    "defaultVersion": true,\
    "marName": "SamLowe_roberta-base-go_emotions.mar",\
    "minWorkers": 1,\
    "maxWorkers": 10,\
    "batchSize": 1,\
    "maxBatchDelay": 100,\
    "responseTimeout": 120\
```

Always 1 worker because of not enough GPU Memory
```
/models/SamLowe_roberta-base-go_emotions

[
    {
        "modelName": "SamLowe_roberta-base-go_emotions",
        "modelVersion": "1.0",
        "modelUrl": "SamLowe_roberta-base-go_emotions.mar",
        "runtime": "python",
        "minWorkers": 1,
        "maxWorkers": 10,
        "batchSize": 1,
        "maxBatchDelay": 100,
        "loadedAtStartup": true,
        "workers": [
            {
                "id": "9000",
                "startTime": "2023-08-15T12:59:03.064Z",
                "status": "READY",
                "memoryUsage": 2889723904,
                "pid": 33,
                "gpu": true,
                "gpuUsage": "gpuId::0 utilization.gpu [%]::21 % utilization.memory [%]::1 % memory.used [MiB]::1644 MiB"
            }
        ]
    }
]
```

# Tests replicas=2
## 5
5 parallel users  \
Error 0%\
throughput 51.7/s\
avg response time 105ms\
<img src=./response-time-graph-12.png>

# Tests replicas=1

## 1
1 parallel users  \
Error 0%\
throughput 11/s\
avg response time 90ms\
note: super healthy
<img src=./response-time-graph-06.png>

## 2
2 parallel users  \
Error 0%\
throughput 22/s\
avg response time 90ms\
note: super healthy
<img src=./response-time-graph-07.png>


## 3
3 parallel users  \
Error 0%\
throughput 30/s\
avg response time 100ms\
note: super healthy
<img src=./response-time-graph-08.png>

## 4
4 parallel users  \
Error 0%\
throughput 46.4/s\
avg response time 85ms\
note: super healthy
<img src=./response-time-graph-09.png>

## 5
5 parallel users  \
Error 0%\
throughput 46.6/s\
avg response time 105ms\
note: start degradation
<img src=./response-time-graph-10.png>

## 8
8 parallel users  \
Error 0%\
throughput 45.5/s\
avg response time 170ms\
note: degradated
<img src=./response-time-graph-05.png>

## 10
10 parallel users  \
Error 0%\
throughput 44/s\
avg response time 220ms\
note: degradated
<img src=./response-time-graph-01.png>

## 15
15 parallel users  \
Error 0%\
throughput 44.6/s\
avg response time 330ms\
note: degradated
<img src=./response-time-graph-04.png>

## 20
20 parallel users  \
Error 0%\
throughput 43.5/s\
avg response time >440ms\
note: degradated
<img src=./response-time-graph-03.png>

## 30
30 parallel users  \
Error 0%\
throughput 44.9/s\
avg response time 650ms\
note: degradated
<img src=./response-time-graph-02.png>
s