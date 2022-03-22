import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)
print(tf.keras.__version__)
print(tf.__path__)


# conda create --name tensorflow python=3.5.2
# activate tensorflow

# python -m pip install -U pip
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tensorflow
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple keras
# or pip install tensorflow==2.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install keras==2.3.1 -i https://pypi.tuna.tsinghua.edu.cn/simple 
# *************************************************************
#    从 TensorFlow 2.1.0 版开始，此软件包需要 msvcp140_1.dll 文件（旧版可再发行软件包可能不提供此文件）。 该可再发行软件包随附在 Visual Studio 2019 #中，但可以单独安装：
# 转到 Microsoft Visual C++ 下载页面。https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads/
#   $$ vc++ 2015-2019 redistributable x64 14.27.29016
# 在页面中向下滚动到“Visual Studio 2015、2017 和 2019”部分。
# 为您的平台下载并安装适用于 Visual Studio 2015、2017 和 2019 的 Microsoft Visual C++ 可再发行软件包。
# *////**********************************************************