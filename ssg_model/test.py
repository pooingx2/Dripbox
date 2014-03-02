#-*- coding: utf-8 -*-
#!/usr/bin/env python
import interface


if __name__ == "__main__":
    file_path = "./로고포인트준것.png"
    des_path = "./로고.png"

    test = interface.SSGInterface()
    # test.upload(file_path)
    # test.download(des_path, file_path)
    buf = test.download(file_path)

    print type(buf)
    with open(des_path, 'wb') as f:
        f.write(buf)