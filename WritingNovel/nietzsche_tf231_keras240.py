from tensorflow import keras
import numpy as np
from tensorflow.python.keras import layers  # MODEL：构建网络-单层LSTM模型
import random  # TEST：生成文本
import sys    # TEST：生成文本

'''
path = keras.utils.get_file(
     'nietzsche.txt',
     origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
text = open(path).read().lower()
'''
text = open('nietzsche.txt').read().lower()
print('Corpus length:', len(text))

# 提取60 个字符组成的序列
maxlen = 60

# 每3个字符采样一个新序列
step = 3

# 保存所提取的序列
sentences = []

# 保存目标（即下一个字符）
next_chars = []
# 就是对文本采样，相当于长度为60，步长为3的滑动窗口
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('Number of sequences:', len(sentences))

# 语料中唯一字符组成的列表
chars = sorted(list(set(text)))
print('Unique characters:', len(chars))
# 一个字典，将唯一字符映射为它在列表chars 中的索引，为了后面的反向引索
char_indices = dict((char, chars.index(char)) for char in chars)

# Next, one-hot encode the characters into binary arrays.
print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1
'''
MODEL：构建网络-单层LSTM模型
from keras import layers
'''
model = keras.models.Sequential()
model.add(layers.LSTM(128, input_shape=(maxlen, len(chars))))
model.add(layers.Dense(len(chars), activation='softmax'))

optimizer = keras.optimizers.RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    # 第一个参量是取得个数，第二个参量是概率分布，第三个参量是生成多少个
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


'''
TEST：生成文本
import random
import sys
'''
for epoch in range(1, 60):
    print('epoch', epoch)
    model.fit(x, y, batch_size=128, epochs=1)
    start_index = random.randint(0, len(text) - maxlen - 1)
    generated_text = text[start_index: start_index + maxlen]
    print('--- Generating with seed: "' + generated_text + '"')
    # # 使用不同的温度来获得生成文本
for temperature in [0.2, 0.5, 1.0, 1.2]:
    print('------ temperature:', temperature)
    sys.stdout.write(generated_text)
    # 从种子文本开始生成400个字符
    for i in range(400):
        # 对生成的字符进行one-hot 编码
        sampled = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(generated_text):
            sampled[0, t, char_indices[char]] = 1.

        preds = model.predict(sampled, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_char = chars[next_index]
        generated_text += next_char
        generated_text = generated_text[1:]
        sys.stdout.write(next_char)
