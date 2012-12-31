Pxblog
======
python blog!!

TODO
--------
 1. 基本文章维护功能
 2. 标签维护
 3. 设置
 4. 上传
 5. 缓存
 6. 上一篇/下一篇
 7. 链接维护
 8. sitemap, rss, robots
 9. 密码访问限制`

使用技术
--------
tornado, memcache, markdown2

文件结构描述
------------
 * templates    	模板目录
 * setting.py		设置(*)
 * webcommon.py     请求处理通用封装: 如Handler基类, 获取页码等...
 * blog.py			前端请求处理
 * admin.py         后端请求处理
 * model.py         model, 数据库访问
 * markdown2.py     markdown语法处理
 * func4temp.py		为模板提供方法: 最新文章, 某标签文章
 * cache.py			缓存
 * file.py			文件读写
 * utils.py			工具: 如当前日期等...(*)
 * saecloud2.py     SAE上传工具修改版本
 * index.wsgi       main 入口

(*)不依赖其他文件

