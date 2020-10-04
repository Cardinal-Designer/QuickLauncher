# -*- coding: utf-8 -*-
from markdown import markdown

def ToHtml(md_text):
    content = markdown(md_text)
    Head = '''<html lang="zh-cn">
    	    <head>
    		    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    		    <style>
    			.content {margin:0 auto;width:720px; solid;text-align:left;}
    			</style>
    	    </head>
    	    <body>
    	    	<div class="content"> ''' + content + ''' </div>
    	    </body>
    	</html>'''

    return Head