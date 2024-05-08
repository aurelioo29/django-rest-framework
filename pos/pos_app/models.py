import sys
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

# /**
#  * Function convert_to_roman
#  ! Mengonversi bilangan bulat dari 1 hingga 12 menjadi representasi angka Romawi.
#  @Parameters:
#  * `number`: String yang mewakili bilangan bulat dari 1 hingga 12.
#  @Returns:
#  * Representasi angka Romawi dari bilangan bulat yang diberikan.
#  */
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

# /**
#  * Function convert_to_number
#  ! Mengonversi representasi angka Romawi menjadi bilangan bulat dari 1 hingga 12.
#  @Parameters:
#  * `roman`: String yang mewakili angka Romawi dari I hingga XII.
#  @Returns:
#  * Bilangan bulat yang sesuai dengan representasi angka Romawi yang diberikan.
#  */
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

# /**
#  * Function compress_image
#  ! Mengompresi gambar dan mengembalikan objek InMemoryUploadedFile yang berisi gambar yang telah dikompresi.
#  @Parameters:
#  * `image`: Gambar yang akan dikompresi.
#  * `filename`: Nama file untuk gambar yang dikompresi.
#  @Returns:
#  * Objek InMemoryUploadedFile yang berisi gambar yang telah dikompresi.
#  */
def compress_image(image, filename):
  curr_datetime = datetime.now().strftime("%Y%m%d %H%M%S")
  im = Image.open(image)

  if im.mode != 'RGB':
    im = im.convert('RGB')

  im_io = BytesIO()
  im.save(im_io, 'jpeg', quality=50, optimize=True)
  im.seek(0) 
  
  new_image = InMemoryUploadedFile(im_io, 'ImageField', '%' + str(filename) + '-' + str(curr_datetime) + '.jpg', 'image/jpeg', sys.getsizeof(im_io), None)
  return new_image

# /**
#  * Class User
#  ! Merepresentasikan pengguna dalam sistem.
#  @Attributes:
#  * `is_waitress`: BooleanField, menunjukkan apakah pengguna adalah pelayan. Defaultnya adalah `False`.
#  * `is_cashier`: BooleanField, menunjukkan apakah pengguna adalah kasir. Defaultnya adalah `False`.
#  * `is_kitchen`: BooleanField, menunjukkan apakah pengguna adalah bagian dari dapur. Defaultnya adalah `False`.
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan kombinasi nama pengguna, nama depan, dan nama belakang pengguna.
#  */
class User(AbstractUser):
  is_waitress = models.BooleanField(default = False)
  is_cashier = models.BooleanField(default = False)
  is_kitchen = models.BooleanField(default = False)

  def __str__(self):
    return str(self.username) + ' ' + str(self.first_name) + ' ' + str(self.last_name)

# /**
#  * Class StatusModel
#  ! Merepresentasikan status dalam sistem.
#  @Attributes:
#  * `status_choices`: Tuple yang berisi pilihan status.
#  * `name`: CharField, nama unik dari status.
#  * `description`: TextField, deskripsi opsional untuk status. Defaultnya adalah string kosong (`''`).
#  * `status`: CharField, menunjukkan status. Pilihan status adalah "Aktif" atau "Tidak Aktif". Defaultnya adalah "Aktif".
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan nilai nama status.
#  */
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

# /**
#  * Class Profile
#  ! Merepresentasikan profil pengguna dalam sistem.
#  @Attributes:
#  * `user`: ForeignKey ke model `User`, menunjukkan pengguna terkait dengan profil ini.
#  * `avatar`: ImageField, menunjukkan gambar profil pengguna. Defaultnya adalah `None`.
#  * `bio`: TextField, deskripsi singkat tentang pengguna.
#  * `status`: ForeignKey ke model `StatusModel`, menunjukkan status keseluruhan dari profil. Defaultnya adalah status pertama yang tersedia dalam model `StatusModel`.
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan kombinasi nama depan, nama belakang, dan ID pengguna.
#  */
class Profile(models.Model):
  user = models.OneToOneField(User, related_name='user_profile', on_delete=models.PROTECT)
  avatar = models.ImageField(default=None, upload_to='profile_images/', blank=True, null=True)
  bio = models.TextField()
  status = models.ForeignKey(StatusModel, related_name='status_profile', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_profile', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_profile', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

#   def __str__(self):
#     return f'{self.user.first_name} {self.user.last_name} {self.user.id}'

# /**
#  * Class TableResto
#  ! Merepresentasikan meja di restoran dalam sistem.
#  @Attributes:
#  * `status_table_choices`: Tuple yang berisi pilihan status meja.
#  * `code`: CharField, kode unik untuk meja.
#  * `name`: CharField, nama meja.
#  * `capacity`: IntegerField, kapasitas meja.
#  * `table_status`: CharField, menunjukkan status meja. Pilihan status adalah "Kosong" atau "Terisi". Defaultnya adalah "Kosong".
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan nilai nama meja.
#  */
class TableResto(models.Model):
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

# /**
#  * Method save
#  ! Metode untuk menyimpan atau memperbarui objek Profile.
#  @Parameters:
#  * `force_insert`: Boolean, menunjukkan apakah harus memaksa operasi insert.
#  * `force_update`: Boolean, menunjukkan apakah harus memaksa operasi update.
#  * `using`: String, nama basis data yang akan digunakan.
#  * `update_fields`: List, daftar bidang yang akan diperbarui.
#  * `*args, **kwargs`: Argumen tambahan yang diteruskan ke metode save.
#  @Description:
#  Metode ini digunakan untuk menyimpan atau memperbarui objek Profile dalam database. Jika objek sudah memiliki ID (artinya objek sudah ada dalam database), maka metode akan mencoba memperbarui objek Profile. 
#  Jika avatar baru diunggah (berbeda dari avatar sebelumnya), maka avatar akan dikompresi menggunakan fungsi `compress_image` dan avatar lama akan dihapus. Jika objek belum memiliki ID, maka metode akan   
#  membuat objek Profile baru dan mengompresi avatar jika avatar diunggah.
#  */
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

# /**
#  * Class Category
#  ! Merepresentasikan kategori dalam sistem.
#  @Attributes:
#  * `name`: CharField, nama kategori.
#  * `status`: ForeignKey ke model `StatusModel`, menunjukkan status keseluruhan dari kategori. Defaultnya adalah status pertama yang tersedia dalam model `StatusModel`.
#  * `user_create`: ForeignKey ke model `User`, menunjukkan pengguna yang membuat kategori ini. Defaultnya adalah `None`.
#  * `user_update`: ForeignKey ke model `User`, menunjukkan pengguna yang terakhir memperbarui kategori ini. Defaultnya adalah `None`.
#  * `created_on`: DateTimeField, menunjukkan waktu saat kategori ini dibuat. Nilainya akan diatur secara otomatis saat objek dibuat.
#  * `last_modified`: DateTimeField, menunjukkan waktu saat kategori ini terakhir diubah. Nilainya akan diatur secara otomatis saat objek diperbarui.
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan nilai nama kategori.
#  */
class Category(models.Model):
  name = models.CharField(max_length=100)
  status = models.ForeignKey(StatusModel, related_name='status_category', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_category', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_category', blank=True, null=True, on_delete=models.SET_NULL)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

# /**
#  * Function increment_menu_resto_code
#  ! Fungsi untuk menghasilkan kode unik untuk menu restoran baru.
#  @Parameters:
#  * Tidak ada parameter yang diperlukan.
#  @Returns:
#  * Kode unik untuk menu restoran baru.
#  */
def increment_menu_resto_code():
  last_code = MenuResto.objects.all().order_by('id').last()
  if not last_code:
    return 'MN-0001'
  code = last_code.code
  code_int = int(code[3:7])
  new_code_int = code_int + 1
  return 'MN-' + str(new_code_int).zfill(4)

# /**
#  * Class MenuResto
#  ! Merepresentasikan menu restoran dalam sistem.
#  @Attributes:
#  * `status_menu_choices`: Tuple yang berisi pilihan status menu.
#  * `code`: CharField, kode unik untuk menu restoran. Nilainya dihasilkan menggunakan fungsi `increment_menu_resto_code` dan tidak dapat diedit setelah objek dibuat.
#  * `name`: CharField, nama menu restoran.
#  * `price`: DecimalField, harga menu restoran.
#  * `decription`: CharField, deskripsi singkat tentang menu.
#  * `image_menu`: ImageField, gambar yang menunjukkan menu restoran. Defaultnya adalah `None`.
#  * `category`: ForeignKey ke model `Category`, menunjukkan kategori menu restoran. Defaultnya adalah `None`.
#  * `menu_status`: CharField, menunjukkan status menu. Pilihan status adalah "Ada" atau "Habis". Defaultnya adalah "Ada".
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan nilai nama menu restoran.
#  */
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

# /**
#  * Method save
#  ! Metode untuk menyimpan atau memperbarui objek MenuResto.
#  @Parameters:
#  * `force_insert`: Boolean, menunjukkan apakah harus memaksa operasi insert.
#  * `force_update`: Boolean, menunjukkan apakah harus memaksa operasi update.
#  * `using`: String, nama basis data yang akan digunakan.
#  * `update_fields`: List, daftar bidang yang akan diperbarui.
#  * `*args, **kwargs`: Argumen tambahan yang diteruskan ke metode save.
#  @Description:
#  Metode ini digunakan untuk menyimpan atau memperbarui objek MenuResto dalam database. Jika objek sudah memiliki ID (artinya objek sudah ada dalam database), maka metode akan mencoba memperbarui objek     
#  MenuResto. Jika gambar menu baru diunggah (berbeda dari gambar sebelumnya), maka gambar akan dikompresi menggunakan fungsi `compress_image` dan gambar lama akan dihapus. Jika objek belum memiliki ID, maka  
#  metode akan membuat objek MenuResto baru dan mengompresi gambar jika gambar diunggah.
#  */

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

# /**
#  * Function increment_order_menu_code
#  ! Fungsi untuk menghasilkan kode unik untuk pesanan baru dalam format tertentu.
#  @Returns:
#  * Kode unik untuk pesanan baru.
#  @Description:
#  Fungsi ini menghasilkan kode unik untuk pesanan baru dalam format 'XXXX-OM-MMMM-YYYY', di mana:
#  - 'XXXX' adalah angka yang menggambarkan urutan pesanan dalam bulan dan tahun saat ini.
#  - 'OM' adalah bagian tetap dari kode untuk menandakan bahwa itu adalah pesanan.
#  - 'MMMM' adalah representasi bulan dalam angka Romawi.
#  - 'YYYY' adalah tahun saat ini.
#  Fungsi ini mengambil pesanan terakhir dari database dan memeriksa apakah pesanan tersebut dibuat pada bulan dan tahun yang sama dengan bulan dan tahun saat ini. 
#  Jika ya, maka kode pesanan terakhir akan diubah sedemikian rupa sehingga nomor urutannya bertambah satu.
#  Jika tidak, maka fungsi akan mengembalikan kode unik untuk pesanan baru dengan nomor urutan dimulai dari 0001.
# */

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
    
# /**
#  * Class OrderMenu
#  ! Merepresentasikan sebuah pesanan dalam sistem.
#  @Attributes:
#  * `status_order_status_choices`: Tuple yang berisi pilihan status pesanan.
#  * `code`: CharField dengan panjang maksimum 20 karakter, merupakan kode unik untuk pesanan. Nilai defaultnya berasal dari fungsi `increment_order_menu_code` dan tidak dapat diedit setelah objek dibuat.
#  * `table_resto`: ForeignKey ke model `TableResto`, menunjukkan meja restoran yang terkait dengan pesanan. Defaultnya adalah `None`.
#  * `cashier`: ForeignKey ke model `User`, menunjukkan kasir yang melakukan pesanan ini. Defaultnya adalah `None`.
#  * `waitress`: ForeignKey ke model `User`, menunjukkan pelayan yang melayani pesanan ini. Defaultnya adalah `None`.
#  * `order_status`: CharField dengan panjang maksimum 15 karakter, menunjukkan status pesanan. Pilihan status termasuk "Belum Dibayar", "Sudah Dibayar", dan "Selesai". Defaultnya adalah "Belum Dibayar".
#  * `total_order`: DecimalField, menunjukkan total biaya pesanan sebelum pajak. Defaultnya adalah `0.00`.
#  * `tax_order`: FloatField, menunjukkan jumlah pajak yang dikenakan pada pesanan. Defaultnya adalah `0`.
#  * `total_payment`: DecimalField, menunjukkan total pembayaran yang harus dibayar, termasuk pajak. Defaultnya adalah `0.00`.
#  * `payment`: DecimalField, menunjukkan jumlah pembayaran yang diberikan oleh pelanggan. Defaultnya adalah `0.00`.
#  * `changed`: DecimalField, menunjukkan jumlah kembalian dari transaksi pembayaran. Defaultnya adalah `0.00`.
#  * `status`: ForeignKey ke model `StatusModel`, menunjukkan status keseluruhan dari pesanan. Defaultnya adalah status pertama yang tersedia dalam model `StatusModel`.
#  * `user_create`: ForeignKey ke model `User`, menunjukkan pengguna yang membuat pesanan ini. Defaultnya adalah `None`.
#  * `user_update`: ForeignKey ke model `User`, menunjukkan pengguna yang terakhir memperbarui pesanan ini. Defaultnya adalah `None`.
#  * `created_on`: DateTimeField, menunjukkan waktu saat pesanan ini dibuat. Nilainya akan diatur secara otomatis saat objek dibuat.
#  * `last_modified`: DateTimeField, menunjukkan waktu saat pesanan ini terakhir diubah. Nilainya akan diatur secara otomatis saat objek diperbarui.
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan nilai kode pesanan sebagai string.
# */

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
  
# /**
#  * Class OrderMenuDetail
#  ! representasikan detail dari sebuah item yang dipesan dalam suatu pesanan.
#  @Attributes:
#  * `order_menu`: ForeignKey ke model `OrderMenu`, terkait dengan pesanan yang berisi item ini. Defaultnya adalah `None`.
#  * `menu_resto`: ForeignKey ke model `MenuResto`, terkait dengan menu restoran yang dipesan. Defaultnya adalah `None`.
#  * `quantity`: IntegerField, menunjukkan jumlah item yang dipesan. Defaultnya adalah `0`.
#  * `subtotal`: DecimalField, menunjukkan subtotal dari item ini dalam pesanan. Defaultnya adalah `0.00`.
#  * `description`: TextField, deskripsi opsional untuk item ini. Defaultnya adalah string kosong (`''`).
#  * `order_menu_detail_status`: CharField, menunjukkan status dari detail pesanan. Pilihan status adalah "Sedang disiapkan" atau "Sudah disajikan". Defaultnya adalah "Sedang disiapkan".
#  * `status`: ForeignKey ke model `StatusModel`, menunjukkan status keseluruhan dari detail pesanan. Defaultnya adalah status pertama yang tersedia dalam model `StatusModel`.
#  * `user_create`: ForeignKey ke model `User`, menunjukkan pengguna yang membuat detail pesanan ini. Defaultnya adalah `None`.
#  * `user_update`: ForeignKey ke model `User`, menunjukkan pengguna yang terakhir memperbarui detail pesanan ini. Defaultnya adalah `None`.
#  * `created_on`: DateTimeField, menunjukkan waktu saat detail pesanan ini dibuat. Nilainya akan diatur secara otomatis saat objek dibuat.
#  * `last_modified`: DateTimeField, menunjukkan waktu saat detail pesanan ini terakhir diubah. Nilainya akan diatur secara otomatis saat objek diperbarui.
#  @Methods:
#  * `__str__()`: Metode untuk mendapatkan representasi string dari objek. Mengembalikan string yang terdiri dari kode pesanan (`order_menu.code`) dan nama menu restoran (`menu_resto`).
# */

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
    return str(self.order_menu.code) + '-' + str(self.menu_resto)