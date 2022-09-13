import requests

my_script = requests.get('https://raw.githubusercontent.com/corlick98/cmput404-labs/master/Lab1/lab1.py')
print(my_script.text)
