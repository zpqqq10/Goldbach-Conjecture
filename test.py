import rarfile
import os

z = rarfile.RarFile(os.path.join(os.getcwd(), 'Reuters.rar'))
z.extractall()
z.close()