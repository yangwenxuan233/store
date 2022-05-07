## DemoAPI
本文主要介绍ui测试框架开发，环境使用python3+selenium3+unittest测试框架及ddt数据驱动，使用HTMLTestRunner来生成测试报告。
存在以下需要单独说明的问题：
* 因接口测试的接触较少，所以退而其次只选择了实现基本的功能测试；
* 在ui测试框架编写中，由于二级页面点击功能button无响应或无跳转，没有实现结果断言和测试结果收集，只在逻辑基础上做框架模拟；
* 对于英文注释，作为首次尝试应用，时间局促只能做到简单注释。

## 测试框架处理流程
测试框架处理过程如下：
* 首先在Test*类中初始化webdriver，创建新的浏览器访问；
* 调用InitPage，使用ddt参数驱动，获取testdata；
* 将testdata传入PageOptions类，实现页面操作逻辑；
* 操作执行完毕后将result数据返回Test*，加以断言，得到结果并获取异常截图，以base64编码形式存储；
* 通过unittest框架加载Test*测试用例类，并用HTMLTestRunner生成测试报告。

## 测试框架结构目录介绍
目录结构介绍如下：
* main:                     执行测试用例并生成测试报告
* InitPage:                 用例数据存储
* Test*:                    测试用例类
* PageOptions:              页面操作逻辑方法
* HTMLTestRunner:           第三方扩展库，用于生成HTML格式测试报告
