import os
from super_resolution import super_resolve
from super_resolution import model


for root, dirs, files in os.walk('images/others/'):
    for f in files:
        if f.endswith(".jpeg") or f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpg2"):
            super_resolve.resolve(root + f, root + f)
