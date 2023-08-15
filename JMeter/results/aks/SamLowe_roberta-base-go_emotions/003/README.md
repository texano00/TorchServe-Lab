

# Tests using CPU
## 01
pod replicaCount=1
```
number_of_gpu=0
"minWorkers": 5
```
throughput 8.9/s\
avg response time 650ms

<img src=Response-Time-Graph-CPU-5workers-5users.png>
<img src=5workers-1pods-5users.png>


## 02
pod replicaCount=1
```
number_of_gpu=0
"minWorkers": 1
```
throughput 35.4/s\
avg response time 140ms

<img src=Response-Time-Graph-CPU-1workers-5users.png>

## 03
pod replicaCount=5

```
number_of_gpu=0
"minWorkers": 1
```
throughput 22/s\
avg response time 250ms

<img src=Response-Time-Graph-CPU-5pods-1workers-5users.png>
<img src=1workers-5pods-5users.png>

## 04
pod replicaCount=15

```
number_of_gpu=0
"minWorkers": 1
```
throughput 9/s\
avg response time 550ms

<img src=Response-Time-Graph-CPU-15pods-1workers-5users.png>
<img src=1workers-15pods-5users.png>

