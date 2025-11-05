from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QListWidget,QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageFilter
import os 
app = QApplication([])
window = QWidget()
window.show()

main_layout = QHBoxLayout()
vertical_layout = QVBoxLayout()
second_vertical_layout = QVBoxLayout()
horizantal_layout = QHBoxLayout()
file_button = QPushButton('Папка')
choose_list = QListWidget()
fhoto = QLabel('картинка')
left_button = QPushButton('Лево')
right_button = QPushButton('Право')
mirrow_button = QPushButton('Зеркало')
cutting_button = QPushButton('Резкость')
white_and_black_button = QPushButton('ЧБ')



window.setLayout(main_layout)
main_layout.addLayout(vertical_layout)
main_layout.addLayout(second_vertical_layout)
vertical_layout.addWidget(file_button)
vertical_layout.addWidget(choose_list)
second_vertical_layout.addWidget(fhoto)
second_vertical_layout.addLayout(horizantal_layout)
horizantal_layout.addWidget(left_button)
horizantal_layout.addWidget(right_button)
horizantal_layout.addWidget(mirrow_button)
horizantal_layout.addWidget(cutting_button)
horizantal_layout.addWidget(white_and_black_button)


class ImageProcessor():
    def __init__(self):
        self.image = None 
        self.folder = None
        self.filename = None
    def load_image(self, folder, filename):
        #загружает изображение
        self.folder = folder
        self.filename = filename
        self.image = Image.open(os.path.join(folder,filename))   
    def show_image(self):
        fhoto.hide()
        pixmap = QPixmap(os.path.join(self.folder,self.filename))
        w,h = fhoto.width(),fhoto.height()
        pixmap = pixmap.scaled(w,h,Qt.AspectRatioMode.KeepAspectRatio)
        fhoto.setPixmap(pixmap)
        fhoto.show()
    def save_image(self):
        self.folder = os.path.join(folder,'modified')
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.image.save(os.path.join(self.folder,self.filename))
    def black_and_white_image(self):
        self.image = self.image.convert('L')
        self.save_image()
        self.show_image()        
    def left_go_image(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        self.show_image()
    def right_go_image(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        self.show_image()  
    def mirrow_image(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        self.show_image() 
    def cutting_image(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        self.show_image() 



image_proccessor = ImageProcessor()

def filter(files):
    extentions = ['.jpg', '.jpeg', '.png', '.webp']
    result = []
    for file in files:
        for extention in extentions:
            if file.endswith(extention):
                result.append(file)  
    return result    

def choose_folder():
    global folder
    folder = QFileDialog.getExistingDirectory()
    files = os.listdir(folder)
    files = filter(files)  
    choose_list.addItems(files)

def show_photo():
    file_name = choose_list.selectedItems()[0].text()# получает название файла из виджета списка
    image_proccessor.load_image(folder, file_name)
    image_proccessor.show_image()
    

file_button.clicked.connect(choose_folder)
choose_list.itemClicked.connect(show_photo)
white_and_black_button.clicked.connect(image_proccessor.black_and_white_image)
left_button.clicked.connect(image_proccessor.left_go_image)
right_button.clicked.connect(image_proccessor.right_go_image)
mirrow_button.clicked.connect(image_proccessor.mirrow_image)
cutting_button.clicked.connect(image_proccessor.cutting_image)
print('HI')
app.exec()