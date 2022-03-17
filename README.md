# timeseries
about : real-time pandas series dataframe

更换环境：
conda activate pdenv

导出当前环境：
conda env export > pdenv.yaml

会生成一个pdenv.yaml文件，将其复制到目标机上后执行导入环境操作：
conda env create -f pdenv.yaml
