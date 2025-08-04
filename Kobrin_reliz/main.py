import os
from PyQt5.QtWidgets import*
from PyQt5.QtCore import Qt  
from PyQt5.QtGui import QPixmap  

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from PIL import ImageFilter  
from PIL.ImageFilter import*


app = QApplication([])  

with open('style', 'r') as style_file:
    style = style_file.read()
    app.setStyleSheet(style) 

win = QWidget() 
win.resize(700, 700) 
win.setWindowTitle('Easy Editor')  
lb_image = QLabel("Картинка") 
btn_dir = QPushButton("Папка")  
lw_files = QListWidget()  

btn_left = QPushButton("Вліво") 
btn_right = QPushButton("Вправо")  
btn_flip = QPushButton("Відзеркалити") 
btn_sharp = QPushButton("Різкість")  
btn_bw = QPushButton("Ч/Б")  

btn_contrast = QPushButton("Контраст")
btn_brightness = QPushButton("Яскравість")
btn_reset = QPushButton("Скинути")

row = QHBoxLayout()  
col1 = QVBoxLayout()  
col2 = QVBoxLayout() 
col1.addWidget(btn_dir)  
col1.addWidget(lw_files) 
col2.addWidget(lb_image, 95)  
row_tools = QHBoxLayout()  
row_tools.addWidget(btn_left)  
row_tools.addWidget(btn_right)  
row_tools.addWidget(btn_flip) 
row_tools.addWidget(btn_sharp)  
row_tools.addWidget(btn_bw)  
row_tools.addWidget(btn_contrast) 
row_tools.addWidget(btn_brightness) 
row_tools.addWidget(btn_reset) 

col2.addLayout(row_tools) 

row.addLayout(col1, 20)  
row.addLayout(col2, 80)  
win.setLayout(row)  
win.show()  
workdir = '' 
def filter(files, extensions):
   """Функція для фільтрації файлів за розширенням."""
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result

def chooseWorkdir():
   """Функція для вибору робочого каталогу."""
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
   """Функція для відображення списку файлів з обраного каталогу."""
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)

   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    """Клас для обробки зображень."""
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        '''Завантажує зображення та запам'ятовує шлях та ім'я файлу.'''
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        '''Зберігає копію файлу у підпапці.'''
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)

        self.image.save(fullname)

    def do_bw(self):
        """Перетворює зображення у чорно-біле."""
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        """Повертає зображення на 90 градусів вліво."""
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        """Повертає зображення на 90 градусів вправо."""
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        """Відображує зображення відзеркалене."""
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        """Застосовує ефект різкості до зображення."""
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        """Відображає зображення на екрані."""
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    
    def apply_filter(self, filter_function):
        self.image = filter_function(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    def do_contrast(self):
        self.apply_filter(lambda img: ImageEnhance.Contrast(img).enhance(2))

    def do_brightness(self):
        self.apply_filter(lambda img: ImageEnhance.Brightness(img).enhance(1.5))

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.original_image = Image.open(fullname)
        self.image = self.original_image.copy()
        
    def do_reset(self):
        if hasattr(self, 'original_image'):
            self.image = self.original_image.copy()
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)

def showChosenImage():
   """Функція для відображення обраного зображення."""
   if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(filename)
       workimage.showImage(os.path.join(workdir, workimage.filename))
       
       


workimage = ImageProcessor()  
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)

btn_contrast.clicked.connect(workimage.do_contrast)
btn_brightness.clicked.connect(workimage.do_brightness)
btn_reset.clicked.connect(workimage.do_reset)

app.exec()  