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

class StatusModel(models.Model):
  status_choices = (
    ('Aktif', 'Aktif'),
    ('Tidak Aktif', 'Tidak Aktif'),
  )
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True, null=True)
  status = models.CharField(max_length=15, choices=status_choices, default='Aktif')
  user_create = models.ForeignKey(User, related_name='user_create_status_model', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_status_model', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.name)

class Profile(models.Model):
  user = models.OneToOneField(User, related_name='user_profile', on_delete=models.PROTECT)
  avatar = models.ImageField(default=None, upload_to='profile_images/', blank=True, null=True)
  bio = models.TextField()
  status = models.ForeignKey(StatusModel, related_name='status_profile', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_profile', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_profile', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.user.first_name} {self.user.last_name} {self.user.id}'

class TableResto(models.Model):
  # status_choices = (
  #   ('Aktif', 'Aktif'),
  #   ('Tidak Aktif', 'Tidak Aktif'),
  # )
  status_table_choices = (
    ('Kosong', 'Kosong'),
    ('Terisi', 'Terisi'),
  )
  code = models.CharField(max_length=20)
  name = models.CharField(max_length=100)
  capacity = models.IntegerField(default=0)
  table_status = models.CharField(max_length=15, choices=status_table_choices, default='Kosong')
  status = models.ForeignKey(StatusModel, related_name='status_table_resto', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_table_resto', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_table_resto', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
  if self.id: 
    # update profile
    try: 
      this = Profile.objects.get(id=self.id)
      if this.avatar != self.avatar:
        var_avatar = self.avatar
        self.avatar = compress_image(var_avatar, 'profile')
        this.avatar.delete()
    except: pass
    super(Profile, self).save(*args, **kwargs)
  
  else:
    # create profile
    if self.avatar:
      var_avatar = self.avatar
      self.avatar = compress_image(var_avatar, 'profile')
    super(Profile, self).save(*args, **kwargs)

class Category(models.Model):
  name = models.CharField(max_length=100)
  status = models.ForeignKey(StatusModel, related_name='status_category', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_category', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_category', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
def increment_menu_resto_code():
  last_code = MenuResto.objects.all().order_by('id').last()
  if not last_code:
    return 'MN-0001'
  code = last_code.code
  code_int = int(code[3:7])
  new_code_int = code_int + 1
  return 'MN-' + str(new_code_int).zfill(4)
class MenuResto(models.Model):
  status_menu_choices = (
    ('Ada', 'Ada'),
    ('Habis', 'Habis'),
  )
  code = models.CharField(max_length=20, default=increment_menu_resto_code, editable=False)
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  decription = models.CharField(max_length=200)
  image_menu = models.ImageField(default=None, upload_to='menu_images/', blank=True, null=True)
  category = models.ForeignKey(Category, related_name='category_menu', blank=True, null=True, on_delete=models.SET_NULL)
  menu_status = models.CharField(max_length=15, choices=status_menu_choices, default='Ada')
  status = models.ForeignKey(StatusModel, related_name='status_menu', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_menu', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_menu', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
  if self.id:
    # update menuResto
    try:
      this = MenuResto.objects.get(id=self.id)
      if this.image_menu != self.image_menu:
        var_image_menu = self.image_menu
        self.image_menu = compress_image(var_image_menu, 'menu')
        this.image_menu.delete()

    except: pass
    super(MenuResto, self).save(*args, **kwargs)
  
  else:
    # create menuResto
    if self.image_menu:
      var_image_menu = self.image_menu
      self.image_menu = compress_image(var_image_menu, 'menu')
    super(MenuResto, self).save(*args, **kwargs)

def increment_order_menu_code():
  last_id = OrderMenu.objects.all().last()
  m = convert_to_roman(str(datetime.date.today().month))

  if not last_id:
    return '0001' + '-OM-' + m + '-' + str(datetime.date.today().year)
  else:
    code = last_id.code
    code_first, code_middle_1, code_middle_2, code_last = code.split('-')
    y = int(code_last[0:4])
    M = convert_to_number(code_middle_2)

    if ((M == datetime.date.today().month) & (y == datetime.date.today().year)):
      code_int = int(code_first[0:4])
      new_code_int = code_int + 1
      return str(new_code_int).zfill(4)+ '-OM-' + m + '-' + str(datetime.date.today().year)
    elif ((M != datetime.date.toda().month) | (y != datetime.date.today().year)):
      return '0001' + '-OM-' + m + '-' + str(datetime.date.today().year)
    
class OrderMenu(models.Model):
  status_order_status_choices = (
    ('Belum Dibayar', 'Belum Dibayar'),
    ('Sudah Dibayar', 'Sudah Dibayar'),
    ('Selesai', 'Selesai'),
  )

  code = models.CharField(max_length=20, default=increment_order_menu_code, editable=False)
  table_resto = models.ForeignKey(TableResto, related_name='table_resto_order_menu', blank=True, null=True, on_delete=models.SET_NULL)
  cashier = models.ForeignKey(User, related_name='cashier_order_menu', blank=True, null=True, on_delete=models.SET_NULL)
  waitress = models.ForeignKey(User, related_name='waitress_order_menu', blank=True, null=True, on_delete=models.SET_NULL)
  order_status = models.CharField(max_length=15, choices=status_order_status_choices, default='Belum Dibayar')
  total_order = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True)
  tax_order = models.FloatField(default=0, blank=True, null=True)
  total_payment = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True)
  payment = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True)
  changed = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True)
  status = models.ForeignKey(StatusModel, related_name='status_order_menu', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_order_menu', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_order_menu', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.code 
  
class OrderMenuDetail(models.Model):
  status_order_menu_detail_choices = (
    ('Sedang disiapkan', 'Sedang disiapkan'),
    ('Sudah disajikan', 'Sudah disajikan'),
  )

  order_menu = models.ForeignKey(OrderMenu, related_name='order_menu_order_menu_detail', blank=True, null=True, on_delete=models.SET_NULL)
  menu_resto = models.ForeignKey(MenuResto, related_name='menu_resto_order_menu_detail', blank=True, null=True, on_delete=models.SET_NULL)
  quantity = models.IntegerField(default=0)
  subtotal = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True)
  description = models.TextField(blank=True, null=True, max_length=200)
  order_menu_detail_status = models.CharField(max_length=20, choices=status_order_menu_detail_choices, default='Sedang disiapkan')
  status = models.ForeignKey(StatusModel, related_name='status_order_menu_detail', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_order_menu_detail', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_order_menu_detail', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.order_menu.code) + '-' + str(self.menu_resto.name)