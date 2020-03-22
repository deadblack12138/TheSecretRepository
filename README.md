# The Secret Repository

图片像素大小：360*270，可换。



###  生成可执行文件

首先要确保已安装代码有需要的所有库。



这里使用pyinstaller:

`pip install pyinstaller`



然后打开命令行，在代码所在文件夹下执行如下命令：

```
pyinstaller main.py
```

可选参数：-i piction.ico（可执行文件图标，需保存在代码所在文件夹下）

如果出现找不到模块的报错可以通过参数-p说明python包所在位置：如：-p C:\Users\90446\AppData\Local\Programs\Python\Python38-32\Lib\site-packages
