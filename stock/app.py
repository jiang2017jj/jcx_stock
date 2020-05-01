import re

from stock import app

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    # app.run()
    data = '${任意字符}'
    data1 = r'1c\\'
    # variables = re.findall(r'\$\{(.+?)\}', data)
    variables = re.findall(r'\\$', data1)
    print(variables)
