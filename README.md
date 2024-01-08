# anjuke小区_spider
安居客小区数据爬虫，结果保存mongodb

1.请求使用`requests`，解析使用`pyquery`，存储数据使用`openpyxl`


2.需要自己更改的地方，cookie，还有urls_1 = 部分，因为安居客小区数据最多显示50页，所以根据价格爬取。

比如成都武侯区小区分为（8000元以下m3101,8000-1万m3102....等等）

还有页数：比如8000元以下只有2页那么range(1,3)首页一般不用改，快速看多少页的方法是，打开第2页，在链接P2后面改为p50，然后滑到最下面看有多少页。

3.一般出错都是出来验证码了，本代码有验证码处理模块，需要手动。

（1）如果出现：
正在爬取：......

进程已结束，退出代码为 0
说明Cookie过期了重新获取Cookie

（2）如果出现某页没爬完就跳下一页验证码，这个需要手动结束后重新开始那一页，然后数据库删除那一页的数据，比如第2页没爬完，那么我结束后去看网站第二页的数据第一个，在数据库找到后删除后面的，然后在代码处更改range（1，总页数+1）为range（2，总页数+1）.这个总页数是你那个价格分区的页数，不要直接复制我的。

4.获取Cookie简单说明：
打开某个小区页面，按住F12打开调试，找到网络选项（network）输入小区价格，然后刷新那个小区页面，再搜索，出来后点击标头，往下拉找到Cookie。具体看图片。
![1](https://github.com/HSDyz/2024Anjuke-xiaoqu--Python/assets/80035767/89470a47-d481-42a0-9511-883a36ee00b4)
![2](https://github.com/HSDyz/2024Anjuke-xiaoqu--Python/assets/80035767/f354d461-d37d-4295-96dd-8e5a9a7cc18b)


5.爬取的数据部分展示
![3](https://github.com/HSDyz/2024Anjuke-xiaoqu--Python/assets/80035767/17dbb751-15f1-4b98-a76b-17d1078b0d66)


6.有更好的完善点子，提issue。






