"""查证 SchemDraw Drawing 的 show 行为：构造签名 + __exit__ 源码。"""
import inspect

import schemdraw

print('[V] schemdraw version:', schemdraw.__version__)
print('[V] Drawing.__init__ signature:')
print('   ', inspect.signature(schemdraw.Drawing.__init__))
try:
    print('[V] Drawing.__exit__ source:')
    print(inspect.getsource(schemdraw.Drawing.__exit__))
except Exception as exc:
    print('[E] cannot get __exit__ source:', exc)