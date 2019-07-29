# BLOG_CMS
基于Django1.9完成的在线博客管理系统

## 记录一下部署djnago是遇到的坑
在配置nginx时候，由于没有设置好nginx的启动权限，导致在sites-available中定义的配置文件不起作用，因此需要在nginx的安装位置基于root权限,另外还一小坑就是在配置文件中将proxy_下划线漏掉，花了很近一天的时间..
