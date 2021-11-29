# README
This file is a list of all blocks and variables in a template 
Hope this may make back-end programmers' work easier 
## base/base.html
- [ ] reminder: hrefs in navbar aren't set yet(only with # as a placeholder)
blocks 
+   metas 
+   title: notice the block is inside `<title>`  
+   navbar 
+   footer
+   script: for js files 
+   style: for css files and other links 
+   content: contents in `<body>` aside from footer and navbar
+   navbar_elements 

variables 
+   user 
## home.html 
extends: base.html 
blocks
+   contents: things inside a container("div class=container")

## index.html 
extends: home.html 
blocks

variables
+   tags: 
+   page_data
    +   items 