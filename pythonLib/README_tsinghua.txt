1.conda源更换为清华 
只需输入如下两行命令：

    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
    conda config --set show_channel_urls yes

2.conda源更换为中科大

只需输入如下两行命令：

conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/

conda config --set show_channel_urls yes

记得删掉c:/usr/usrname里的.condarc原有的清华镜像

3.如果需要换回conda的默认源。查看了conda config的文档后，发现直接删除channels即可。命令如下：

conda config --remove-key channels
————————————————
版权声明：本文为CSDN博主「Arylu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/Arylu/java/article/details/83659221

---------------------
更改目录：暂时只需要配置jupter notbook的默认工作目录。
打开cmd窗口：输入jupyter notebook --generate-config找到配置文件的路径

找到c.NotebookApp.notebook_dir = ''
改为c.NotebookApp.notebook_dir = 'D:\projects'

打开Jupyter Notebook快捷方式的位置
找到文件--右键--属性，将目标的“jupyter-notebook-script.py”后面的去掉后。
