# urls-judge 1.0:

本脚本用于批量筛选出布置了相应厂商业务或者说正常存活符合正常逻辑的站点，通过异步协程高并发实现快速判断。可通过 [关于判断网站是否正常存活的一些想法](https://www.jianshu.com/p/ba139eddadf0) 了解判断依据。

## 依存关系:
```
运行环境: python3.8
所需依赖库: lxml,asyncio,aiohttp,difflib
使用pip命令安装即可
```
## 用法:
>Usage: urls-judge.py [options] -i input
>-h, --help            show this help message and exit

## 屏幕截图:
![result.png](https://upload-images.jianshu.io/upload_images/21474770-1f2b9362c911a432.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![result2.png](https://upload-images.jianshu.io/upload_images/21474770-73b08a2b0fbcb8ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)










