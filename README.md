# urls-judge 1.0:

本脚本用于批量筛选出布置了相应厂商业务或者说正常存活符合正常逻辑的站点，通过异步协程高并发实现快速判断。各位师傅可通过我的博客 [关于判断网站是否正常存活的一些想法](https://www.jianshu.com/p/ba139eddadf0) 了解判断依据。
## 说明:
此脚本会生成5个txt文件:
- A类表示首页正常且站点符合逻辑的类别
- B类表示首页异常但站点符合逻辑的类别
- C类表示首页异常且站点也不符合逻辑的类别
- D类表示服务端方面异常的站点，可以多次访问测试的类别
- E类表示极少见的状态码及异常，多半不存在的url的类别
## 依存关系:
```
运行环境: python3.8
所需依赖库: lxml,asyncio,aiohttp,difflib,argparse
使用pip命令安装即可
```
## 用法:
>Usage: urls-judge.py [-h] [-o OUTPUT] -i INPUT  
optional arguments:  
-h,　--help　　　　　　　show program's version number and exit  
-o,　--output　　　　　　The dirname where the files are located  
-i,　--input　　　　　　　The path to the file that holds the url or IP

## 举例:
- domain.txt中的url格式为:xxx.xxx.com,不需要添加http或者https
- 判断c:\domain.txt里的url是否正常，然后在urls-judge.py的目录上生成一个domain目录，在此目录下生成a,b,c,d,e共5个txt文件，-o参数默认为py文件的绝对路径
>python　urls-judge.py　-i=c:\domain.txt　-o=domain
## 屏幕截图:
![result.png](https://upload-images.jianshu.io/upload_images/21474770-1f2b9362c911a432.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![result2.png](https://upload-images.jianshu.io/upload_images/21474770-73b08a2b0fbcb8ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)










