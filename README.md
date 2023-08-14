# TorchServe Lab
**Inference** **stress tests** tests using [TorchServe](https://pytorch.org/serve/) (most models from **HuggingFace**).\
The intent of this repo is to report some test with very different configurations, ex:
* using CPU instead of GPU
* TorchServe settings
* GPU time slicing
* GPU sharing
* Scaling on Kubernetes

to understand what could be the best perfomance setup for an inference enterprise environment at scale.

For the load I used [JMeter tool](https://jmeter.apache.org/).

First of all, from the official TorchServe they declare that TorchServe is production ready.
> TorchServe can be used for many types of inference in production settings.

# Tests
## Local development
Even if could not give an interesting contribution for running inference at scale, this was my starting point.\
I tested the serving of [SamLowe/roberta-base-go_emotions](SamLowe_roberta-base-go_emotions) model from HuggingFace running incresing the parallel users as below:
* 15
* 30
* 60

I did exactly the same test using both devices of my PC:
* Intel(R) Core(TM) i7-4710HQ CPU @ 2.50GHz
* NVIDIA GeForce GTX 850M

### Using CPU
Avarage response time
#### 15 users
![alt text](JMeter/results/local/SamLowe_roberta-base-go_emotions/CPU/Response%20Time%20Graph-15users.png)
#### 30 users
![alt text](JMeter/results/local/SamLowe_roberta-base-go_emotions/CPU/Response%20Time%20Graph-30users.png)
#### 60 users
![alt text](JMeter/results/local/SamLowe_roberta-base-go_emotions/CPU/Response%20Time%20Graph-60users.png)

### Using GPU
Avarage response time
#### 15 users
![alt text](JMeter/results/local/SamLowe_roberta-base-go_emotions/GPU/Response%20Time%20Graph-15users.png)
#### 30 users
![alt text](JMeter/results/local/SamLowe_roberta-base-go_emotions/GPU/Response%20Time%20Graph-30users.png)
#### 60 users
![alt text](JMeter/results/local/SamLowe_roberta-base-go_emotions/GPU/Response%20Time%20Graph-60users.png)

## Kubernetes

# Useful links
* TorchServe configurations
https://pytorch.org/serve/configuration.html
* hp official Doc https://pytorch.org/serve/
* `nvtop` like `htop` but for Nvidia GPU