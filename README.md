Pxblog
======
python blog!!

使用技术
--------
bottle + Jinja2

文件结构描述
------------
 * templates    	模板目录
 * setting.py		设置(*)
 * blog.py			url处理
 * func4temp.py		为模板提供方法: 最新文章, 随机文章, 某标签文章
 * cache.py			缓存
 * file.py			文件读写
 * utils.py			工具: 当前日期...(*)

(*)不依赖其他文件
