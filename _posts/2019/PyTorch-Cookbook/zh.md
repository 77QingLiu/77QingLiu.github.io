> 整理自知乎 - 张皓：https://zhuanlan.zhihu.com/p/59205847

# 需要用到的包
```python
import collections
import os
import shutil
import tqdm

import numpy as np
import PIL.Image
import torch
import torchvision
```

# 基础配置

### 检查PyTorch版本

```python
torch.__version__               # PyTorch version
torch.version.cuda              # Corresponding CUDA version
torch.backends.cudnn.version()  # Corresponding cuDNN version
torch.cuda.get_device_name(0)   # GPU type
```

### 更新PyTorch
PyTorch将被安装在anaconda3/lib/python3.7/site-packages/torch/目录下。

```python
conda update pytorch torchvision -c pytorch
```

### 固定随机种子
```python
torch.manual_seed(0)
torch.cuda.manual_seed_all(0)
```

### 指定程序运行在特定GPU卡上
在命令行指定环境变量
```bash
CUDA_VISIBLE_DEVICES=0,1 python train.py
```

或在代码中指定
```python
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'
```

### 判断是否有CUDA支持
```python
torch.cuda.is_available()
```

### 设置为cuDNN benchmark模式
Benchmark模式会提升计算速度，但是由于计算中有随机性，每次网络前馈结果略有差异。

```python
torch.backends.cudnn.benchmark = True
```

如果想要避免这种结果波动，设置

```python
torch.backends.cudnn.deterministic = True
```

### 清除GPU存储
有时Control-C中止运行后GPU存储没有及时释放，需要手动清空。在PyTorch内部可以

```python
torch.cuda.empty_cache()
```

或在命令行可以先使用ps找到程序的PID，再使用kill结束该进程
```bash
ps aux | grep python
kill -9 [pid]
```

或者直接重置没有被清空的GPU
```bash
nvidia-smi --gpu-reset -i [gpu_id]
```

# 张量处理
### 张量基本信息
```python
tensor.type()   # Data type
tensor.size()   # Shape of the tensor. It is a subclass of Python tuple
tensor.dim()    # Number of dimensions.
```

### 数据类型转换
```python
# Set default tensor type. Float in PyTorch is much faster than double.
torch.set_default_tensor_type(torch.FloatTensor)

# Type convertions.
tensor = tensor.cuda()
tensor = tensor.cpu()
tensor = tensor.float()
tensor = tensor.long()
```

##### torch.Tensor与np.ndarray转换
```python
# torch.Tensor -> np.ndarray.
ndarray = tensor.cpu().numpy()

# np.ndarray -> torch.Tensor.
tensor = torch.from_numpy(ndarray).float()
tensor = torch.from_numpy(ndarray.copy()).float()  # If ndarray has negative stride
```

##### torch.Tensor与PIL.Image转换
PyTorch中的张量默认采用N×D×H×W的顺序，并且数据范围在[0, 1]，需要进行转置和规范化。

```python
# torch.Tensor -> PIL.Image.
image = PIL.Image.fromarray(torch.clamp(tensor * 255, min=0, max=255
    ).byte().permute(1, 2, 0).cpu().numpy())
image = torchvision.transforms.functional.to_pil_image(tensor)  # Equivalently way

# PIL.Image -> torch.Tensor.
tensor = torch.from_numpy(np.asarray(PIL.Image.open(path))
    ).permute(2, 0, 1).float() / 255
tensor = torchvision.transforms.functional.to_tensor(PIL.Image.open(path))  # Equivalently way
```

##### np.ndarray与PIL.Image转换
```python
# np.ndarray -> PIL.Image.
image = PIL.Image.fromarray(ndarray.astypde(np.uint8))

# PIL.Image -> np.ndarray.
ndarray = np.asarray(PIL.Image.open(path))
```

### 从只包含一个元素的张量中提取值
这在训练时统计loss的变化过程中特别有用。否则这将累积计算图，使GPU存储占用量越来越大。

```python
value = tensor.item()
```

### 张量形变
张量形变常常需要用于将卷积层特征输入全连接层的情形。相比torch.view，torch.reshape可以自动处理输入张量不连续的情况。

```python
tensor = torch.reshape(tensor, shape)
```

### 打乱顺序
```python
tensor = tensor[torch.randperm(tensor.size(0))]  # Shuffle the first dimension
```

### 水平翻转
PyTorch不支持tensor[::-1]这样的负步长操作，水平翻转可以用张量索引实现。
```python
# Assume tensor has shape N*D*H*W.
tensor = tensor[:, :, :, torch.arange(tensor.size(3) - 1, -1, -1).long()]
```

### 复制张量
有三种复制的方式，对应不同的需求。
```python
# Operation                 |  New/Shared memory | Still in computation graph |
tensor.clone()            # |        New         |          Yes               |
tensor.detach()           # |      Shared        |          No                |
tensor.detach.clone()()   # |        New         |          No                |
```

### 拼接张量
注意torch.cat和torch.stack的区别在于torch.cat沿着给定的维度拼接，而torch.stack会新增一维。例如当参数是3个10×5的张量，torch.cat的结果是30×5的张量，而torch.stack的结果是3×10×5的张量。
```python
tensor = torch.cat(list_of_tensors, dim=0)
tensor = torch.stack(list_of_tensors, dim=0)
```

### 将整数标记转换成独热（one-hot）编码
PyTorch中的标记默认从0开始。
```python
N = tensor.size(0)
one_hot = torch.zeros(N, num_classes).long()
one_hot.scatter_(dim=1, index=torch.unsqueeze(tensor, dim=1), src=torch.ones(N, num_classes).long())
```

### 得到非零/零元素
```python
torch.nonzero(tensor)               # Index of non-zero elements
torch.nonzero(tensor == 0)          # Index of zero elements
torch.nonzero(tensor).size(0)       # Number of non-zero elements
torch.nonzero(tensor == 0).size(0)  # Number of zero elements
```

### 张量扩展
```python
# Expand tensor of shape 64*512 to shape 64*512*7*7.
torch.reshape(tensor, (64, 512, 1, 1)).expand(64, 512, 7, 7)
```

### 矩阵乘法
```python
# Matrix multiplication: (m*n) * (n*p) -> (m*p).
result = torch.mm(tensor1, tensor2)

# Batch matrix multiplication: (b*m*n) * (b*n*p) -> (b*m*p).
result = torch.bmm(tensor1, tensor2)

# Element-wise multiplication.
result = tensor1 * tensor2
```

### 计算两组数据之间的两两欧式距离
```python
# X1 is of shape m*d.
X1 = torch.unsqueeze(X1, dim=1).expand(m, n, d)
# X2 is of shape n*d.
X2 = torch.unsqueeze(X2, dim=0).expand(m, n, d)
# dist is of shape m*n, where dist[i][j] = sqrt(|X1[i, :] - X[j, :]|^2)
dist = torch.sqrt(torch.sum((X1 - X2) ** 2, dim=2))
```

# 模型定义
### 卷积层
最常用的卷积层配置是
```python
conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True)
conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=True)
```
如果卷积层配置比较复杂，不方便计算输出大小时，可以利用如下可视化工具辅助
![](http://img.77qingliu.com/post/2019-05-14-124136.jpg)[https://ezyang.github.io/convolution-visualizer/index.html]

### GAP（Global average pooling）层
```python
gap = torch.nn.AdaptiveAvgPool2d(output_size=1)
```

### 双线性汇合（bilinear pooling）
```python
X = torch.reshape(N, D, H * W)                        # Assume X has shape N*D*H*W
X = torch.bmm(X, torch.transpose(X, 1, 2)) / (H * W)  # Bilinear pooling
assert X.size() == (N, D, D)
X = torch.reshape(X, (N, D * D))
X = torch.sign(X) * torch.sqrt(torch.abs(X) + 1e-5)   # Signed-sqrt normalization
X = torch.nn.functional.normalize(X)                  # L2 normalization
```

### 多卡同步BN（Batch normalization）
当使用torch.nn.DataParallel将代码运行在多张GPU卡上时，PyTorch的BN层默认操作是各卡上数据独立地计算均值和标准差，同步BN使用所有卡上的数据一起计算BN层的均值和标准差，缓解了当批量大小（batch size）比较小时对均值和标准差估计不准的情况，是在目标检测等任务中一个有效的提升性能的技巧。[Synchronized-BatchNorm-PyTorch](https://link.zhihu.com/?target=https%3A//github.com/vacancy/Synchronized-BatchNorm-PyTorch)

### 类似BN滑动平均
如果要实现类似BN滑动平均的操作，在forward函数中要使用原地（inplace）操作给滑动平均赋值。
```python
class BN(torch.nn.Module)
    def __init__(self):
        ...
        self.register_buffer('running_mean', torch.zeros(num_features))

    def forward(self, X):
        ...
        self.running_mean += momentum * (current - self.running_mean)
```

### 计算模型整体参数量
```python
num_parameters = sum(torch.numel(parameter) for parameter in model.parameters())
```

### 类似Keras的model.summary()输出模型信息
[pytorch-summary](https://github.com/sksq96/pytorch-summary)

### 模型权值初始化
注意model.modules()和model.children()的区别：model.modules()会迭代地遍历模型的所有子层，而model.children()只会遍历模型下的一层。

```python
# Common practise for initialization.
for layer in model.modules():
    if isinstance(layer, torch.nn.Conv2d):
        torch.nn.init.kaiming_normal_(layer.weight, mode='fan_out',
                                      nonlinearity='relu')
        if layer.bias is not None:
            torch.nn.init.constant_(layer.bias, val=0.0)
    elif isinstance(layer, torch.nn.BatchNorm2d):
        torch.nn.init.constant_(layer.weight, val=1.0)
        torch.nn.init.constant_(layer.bias, val=0.0)
    elif isinstance(layer, torch.nn.Linear):
        torch.nn.init.xavier_normal_(layer.weight)
        if layer.bias is not None:
            torch.nn.init.constant_(layer.bias, val=0.0)

# Initialization with given tensor.
layer.weight = torch.nn.Parameter(tensor)
```

### 部分层使用预训练模型
注意如果保存的模型是torch.nn.DataParallel，则当前的模型也需要是torch.nn.DataParallel。torch.nn.DataParallel(model).module == model。

```python
model.load_state_dict(torch.load('model,pth'), strict=False)
```

### 将在GPU保存的模型加载到CPU
```python
model.load_state_dict(torch.load('model,pth', map_location='cpu'))
```

# 数据准备、特征提取与微调
### 提取ImageNet预训练模型某层的卷积特征
```python
# VGG-16 relu5-3 feature.
model = torchvision.models.vgg16(pretrained=True).features[:-1]
# VGG-16 pool5 feature.
model = torchvision.models.vgg16(pretrained=True).features
# VGG-16 fc7 feature.
model = torchvision.models.vgg16(pretrained=True)
model.classifier = torch.nn.Sequential(*list(model.classifier.children())[:-3])
# ResNet GAP feature.
model = torchvision.models.resnet18(pretrained=True)
model = torch.nn.Sequential(collections.OrderedDict(
    list(model.named_children())[:-1]))

with torch.no_grad():
    model.eval()
    conv_representation = model(image)
```

### 提取ImageNet预训练模型多层的卷积特征
```python
class FeatureExtractor(torch.nn.Module):
    """Helper class to extract several convolution features from the given
    pre-trained model.

    Attributes:
        _model, torch.nn.Module.
        _layers_to_extract, list<str> or set<str>

    Example:
        >>> model = torchvision.models.resnet152(pretrained=True)
        >>> model = torch.nn.Sequential(collections.OrderedDict(
                list(model.named_children())[:-1]))
        >>> conv_representation = FeatureExtractor(
                pretrained_model=model,
                layers_to_extract={'layer1', 'layer2', 'layer3', 'layer4'})(image)
    """
    def __init__(self, pretrained_model, layers_to_extract):
        torch.nn.Module.__init__(self)
        self._model = pretrained_model
        self._model.eval()
        self._layers_to_extract = set(layers_to_extract)
    
    def forward(self, x):
        with torch.no_grad():
            conv_representation = []
            for name, layer in self._model.named_children():
                x = layer(x)
                if name in self._layers_to_extract:
                    conv_representation.append(x)
            return conv_representation
```

### 其他预训练模型
[Pretrained ConvNets for pytorch: NASNet, ResNeXt, ResNet, InceptionV4, InceptionResnetV2, Xception, DPN, etc.
](https://github.com/Cadene/pretrained-models.pytorch)

### 微调全连接层
```python
model = torchvision.models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(512, 100)  # Replace the last fc layer
optimizer = torch.optim.SGD(model.fc.parameters(), lr=1e-2, momentum=0.9, weight_decay=1e-4)
```

### 以较大学习率微调全连接层，较小学习率微调卷积层
```python
model = torchvision.models.resnet18(pretrained=True)
finetuned_parameters = list(map(id, model.fc.parameters()))
conv_parameters = (p for p in model.parameters() if id(p) not in finetuned_parameters)
parameters = [{'params': conv_parameters, 'lr': 1e-3}, 
              {'params': model.fc.parameters()}]
optimizer = torch.optim.SGD(parameters, lr=1e-2, momentum=0.9, weight_decay=1e-4)

```

# 模型训练
### 训练基本代码框架
```python
for t in epoch(80):
    for images, labels in tqdm.tqdm(train_loader, desc='Epoch %3d' % (t + 1)):
        images, labels = images.cuda(), labels.cuda()
        scores = model(images)
        loss = loss_function(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### L1正则化
```python
l1_regularization = torch.nn.L1Loss(reduction='sum')
loss = ...  # Standard cross-entropy loss
for param in model.parameters():
    loss += torch.sum(torch.abs(param))
loss.backward()
```

### 不对偏置项进行L2正则化/权值衰减（weight decay）
```python
bias_list = (param for name, param in model.named_parameters() if name[-4:] == 'bias')
others_list = (param for name, param in model.named_parameters() if name[-4:] != 'bias')
parameters = [{'parameters': bias_list, 'weight_decay': 0},                
              {'parameters': others_list}]
optimizer = torch.optim.SGD(parameters, lr=1e-2, momentum=0.9, weight_decay=1e-4)
```

### 梯度裁剪（gradient clipping）
```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=20)
```

### 计算Softmax输出的准确率
```python
score = model(images)
prediction = torch.argmax(score, dim=1)
num_correct = torch.sum(prediction == labels).item()
accuruacy = num_correct / labels.size(0)
```

### 可视化模型前馈的计算图
[A small package to create visualizations of PyTorch execution graphs](https://github.com/szagoruyko/pytorchviz)

### 可视化学习曲线
* [Visdom](https://link.zhihu.com/?target=https%3A//github.com/facebookresearch/visdom)
* [TensorboardX](https://link.zhihu.com/?target=https%3A//github.com/lanpa/tensorboardX)

### 得到当前学习率
```python
# If there is one global learning rate (which is the common case).
lr = next(iter(optimizer.param_groups))['lr']

# If there are multiple learning rates for different layers.
all_lr = []
for param_group in optimizer.param_groups:
    all_lr.append(param_group['lr'])
```

### 学习率衰减
```python
# Reduce learning rate when validation accuarcy plateau.
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', patience=5, verbose=True)
for t in range(0, 80):
    train(...); val(...)
    scheduler.step(val_acc)

# Cosine annealing learning rate.
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=80)
# Reduce learning rate by 10 at given epochs.
scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[50, 70], gamma=0.1)
for t in range(0, 80):
    scheduler.step()    
    train(...); val(...)

# Learning rate warmup by 10 epochs.
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda t: t / 10)
for t in range(0, 10):
    scheduler.step()
    train(...); val(...)
```

### 保存与加载断点
注意为了能够恢复训练，我们需要同时保存模型和优化器的状态，以及当前的训练轮数。

```python
# Save checkpoint.
is_best = current_acc > best_acc
best_acc = max(best_acc, current_acc)
checkpoint = {
    'best_acc': best_acc,    
    'epoch': t + 1,
    'model': model.state_dict(),
    'optimizer': optimizer.state_dict(),
}
model_path = os.path.join('model', 'checkpoint.pth.tar')
torch.save(checkpoint, model_path)
if is_best:
    shutil.copy('checkpoint.pth.tar', model_path)

# Load checkpoint.
if resume:
    model_path = os.path.join('model', 'checkpoint.pth.tar')
    assert os.path.isfile(model_path)
    checkpoint = torch.load(model_path)
    best_acc = checkpoint['best_acc']
    start_epoch = checkpoint['epoch']
    model.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    print('Load checkpoint at epoch %d.' % start_epoch)
```

# PyTorch其他注意事项

### 模型定义
* 建议有参数的层和汇合（pooling）层使用torch.nn模块定义，激活函数直接使用torch.nn.functional。torch.nn模块和torch.nn.functional的区别在于，torch.nn模块在计算时底层调用了torch.nn.functional，但torch.nn模块包括该层参数，还可以应对训练和测试两种网络状态。使用torch.nn.functional时要注意网络状态，如
```python
   def forward(self, x):
    ...
    x = torch.nn.functional.dropout(x, p=0.5, training=self.training)
```
* model(x)前用model.train()和model.eval()切换网络状态。
* 不需要计算梯度的代码块用with torch.no_grad()包含起来。model.eval()和torch.no_grad()的区别在于，model.eval()是将网络切换为测试状态，例如BN和随机失活（dropout）在训练和测试阶段使用不同的计算方法。torch.no_grad()是关闭PyTorch张量的自动求导机制，以减少存储使用和加速计算，得到的结果无法进行loss.backward()。
* torch.nn.CrossEntropyLoss的输入不需要经过Softmax。torch.nn.CrossEntropyLoss等价于torch.nn.functional.log_softmax + torch.nn.NLLLoss。
* loss.backward()前用optimizer.zero_grad()清除累积梯度。optimizer.zero_grad()和model.zero_grad()效果一样。

### PyTorch性能与调试
* torch.utils.data.DataLoader中尽量设置pin_memory=True，对特别小的数据集如MNIST设置pin_memory=False反而更快一些。num_workers的设置需要在实验中找到最快的取值。
* 用del及时删除不用的中间变量，节约GPU存储。
* 使用inplace操作可节约GPU存储，如
```python
x = torch.nn.functional.relu(x, inplace=True)
```
* 减少CPU和GPU之间的数据传输。例如如果你想知道一个epoch中每个mini-batch的loss和准确率，先将它们累积在GPU中等一个epoch结束之后一起传输回CPU会比每个mini-batch都进行一次GPU到CPU的传输更快。
* 使用半精度浮点数half()会有一定的速度提升，具体效率依赖于GPU型号。需要小心数值精度过低带来的稳定性问题。
* 时常使用assert tensor.size() == (N, D, H, W)作为调试手段，确保张量维度和你设想中一致。
* 除了标记y外，尽量少使用一维张量，使用n*1的二维张量代替，可以避免一些意想不到的一维张量计算结果。
* 统计代码各部分耗时
```python
with torch.autograd.profiler.profile(enabled=True, use_cuda=False) as profile:
    ...
print(profile)
```
