# Hidden Flag

YARA是一款旨在帮助恶意软件研究人员识别和分类恶意软件样本的开源工具，使用YARA可以基于文本或二进制模式创建恶意软件家族描述信息。简而言之就是一个索引了机器内文件的数据库，可以使用类似下面的语法进行查询：

```yara
rule TextExample
{
    strings:
        $text_string = "p4{"

    condition:
       $text_string
}
```

这个规则可以匹配到 `/opt/bin/getflag`，说明可以用这种方式猜解出flag。同时，字符串还可以通过十六进制来表示，如`$text_string = {70 34 7B}`，这种表示方式支持分支匹配，如`$text_string = {70 34 (7B | 7C)}`，所以一次可以测试多个字符（应该也支持正则，不过好像用不了）。

写脚本，二分查找跑flag，网站有点难连接所以等得有点久。

`p4{ind3x1ng-l3ak5}`
