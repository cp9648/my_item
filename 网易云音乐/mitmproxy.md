## 官方
* [mitmproxy - an interactive HTTPS proxy](https://mitmproxy.org/)
* [Download Windows Installer: v4.0.4](https://snapshots.mitmproxy.org/4.0.4/mitmproxy-4.0.4-windows-installer.exe)
* [GitHub: mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy)

## 参数
* `-s <Python文件>` 应用某个Python文件
   - 示例: `mitmdump -s F:\modify-mitm.py`
* `--listen-port <PORT>` 代理监听端口
   - 示例: `mitmweb --listen-port 8989`
* `--set mode=upstream:<协议>://<代理IP>:<代理端口>` 使用代理
   - 示例: `mitmweb --set mode=upstream:https://119.101.112.119:9999`

## 博文参考
* [MitmProxy的安装](https://germey.gitbooks.io/python3webspider/1.7.2-MitmProxy的安装.html)
* [App爬虫神器mitmproxy和mitmdump的使用](https://juejin.im/post/5ac9ea6d518825364001b5b9)
* [如何使用mitmproxy来读取和修改HTTPS内容](https://zhuanlan.zhihu.com/p/29466524)
* [mitmproxy安装与使用 （抓包，中间人代理工具、支持SSL）](https://www.jianshu.com/p/0cc558a8d6a2)
* [mitmproxy 使用指南](https://foofish.net/mitmproxy-toturial.html)