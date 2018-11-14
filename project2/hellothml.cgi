#!/usr/bin/python3
import cgi,cgitb

form = cgi.FieldStorage()


print("Content-type:text/html")
print()
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print("<title>Hello World</title>")
print("</head>")
print("<body>")
print("<h2> Hello World! </h2>")
print("<form method='get' action='hellothml.cgi'>")
print("<input type = 'text' name='target'/>","<input type='submit'/>")
print("</form>")
argv_data = form.getvalue('target')


print('<H2>Hello',argv_data,'</H2>')
print("</body>")
print("</html>")

