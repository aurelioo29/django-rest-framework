import sys
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
def convert_to_roman(number):
  if number == str(1):
    roman = "I"
  elif number == str(2):
    roman = "II"
  elif number == str(3):
    roman = "III"
  elif number == str(4):
    roman = "IV"
  elif number == str(5):
    roman = "V"
  elif number == str(6):
    roman = "VI"
  elif number == str(7):
    roman = "VII"
  elif number == str(8):
    roman = "VIII"
  elif number == str(9):
    roman = "IX"
  elif number == str(10):
    roman = "X"
  elif number == str(11):
    roman = "XI"
  elif number == str(12):
    roman = "XII"
  return roman

def convert_to_number(roman):
  if roman == 'I':
    number = int(1)
  elif roman == 'II':
    number = int(2)
  elif roman == 'III':
    number = int(3)
  elif roman == 'IV':
    number = int(4)
  elif roman == 'V':
    number = int(5)
  elif roman == 'VI':
    number = int(6)
  elif roman == 'VII':
    number = int(7)
  elif roman == 'VIII':
    number = int(8)
  elif roman == 'IX':
    number = int(9)
  elif roman == 'X':
    number = int(10)
  elif roman == 'XI':
    number = int(11)
  elif roman == 'XII':
    number = int(12)
  return number

def compress_image(image, filename):
  curr_datetime = datetime.now().strftime("%Y%m%d %H%M%S")    # Dapatkan tanggal dan waktu saat ini dan formatkan sebagai 'YYYYMMDD HHMMSS'
  im = Image.open(image)  # Buka file gambar

  # Periksa jika mode gambar bukan RGB, konversi ke RGB
  if im.mode != 'RGB':
    im = im.convert('RGB')

  im_io = BytesIO()   # Buat aliran biner di dalam memori untuk menyimpan gambar yang telah dikompresi
  im.save(im_io, 'jpeg', quality=50, optimize=True)   # Simpan gambar ke dalam aliran di memori sebagai file JPEG dengan kualitas=50 dan optimasi diaktifkan
  im.seek(0)  # Setel posisi aliran kembali ke awal
  
  # Buat objek InMemoryUploadedFile baru dengan data gambar yang telah dikompresi
  new_image = InMemoryUploadedFile(im_io,  # Teruskan aliran biner di memori
                                      'ImageField',  # Tentukan nama field ( diasumsikan 'ImageField')
                                      '%' + str(filename) + '-' + str(curr_datetime) + '.jpg',  # Tetapkan nama file
                                      'image/jpeg',  # Tetapkan tipe konten
                                      sys.getsizeof(im_io),  # Dapatkan ukuran aliran di memori
                                      None)  # Atur charset menjadi None
  return new_image

class User(AbstractUser):
  is_waitress = models.BooleanField(default = False)
  is_cashier = models.BooleanField(default = False)
  is_kitchen = models.BooleanField(default = False)

  def __str__(self):
    return str(self.username) + ' ' + str(self.first_name) + ' ' + str(self.last_name)

class TableResto(models.Model):
  status_choices = (
    ('Aktif', 'Aktif'),
    ('Tidak Aktif', 'Tidak Aktif'),
  )
  status_table_choices = (
    ('Kosong', 'Kosong'),
    ('Terisi', 'Terisi'),
  )
  code = models.CharField(max_length=20)
  name = models.CharField(max_length=100)
  capacity = models.IntegerField(default=0)
  table_status = models.CharField(max_length=15, choices=status_table_choices, default='Kosong')
  status = models.CharField(max_length=15, choices=status_choices, default='Aktif')
  user_create = models.ForeignKey(User, related_name='user_create_table_resto', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_table_resto', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name