from dscl.runtime import *
def test():
  for i in range(1, 100):
    if i == 67:
      print("SIX SEVENNNN")
    elif i == 21:
      print("9+10")
    else:
      print(i)
async def test_but_asynchronous():
  print("hello!")
b = (3 + 2) * 2
while b != 0:
  print(b)
  b = b - 1
def lamdba_1():
  table = Table(50, 70)
  table.append(50)
  print(table)
a = lamdba_1
test()
test_but_asynchronous()
a()
