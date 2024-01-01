from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, name, date_of_birth=None, student_id=None, secondary_email=None, phone_number=None,
                    position='Not a Member', department=None, avatar=None, rs_status=None, facebook_profile=None,
                    linkedin_link=None, robu_start=None, robu_end=None, bracu_start=None, password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth=date_of_birth,
            student_id=student_id,
            secondary_email=secondary_email,
            phone_number=phone_number,
            position=position,
            department=department,
            avatar=avatar,
            rs_status=rs_status,
            facebook_profile=facebook_profile,
            linkedin_link=linkedin_link,
            robu_start=robu_start,
            robu_end=robu_end,
            bracu_start=bracu_start,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, date_of_birth=None, student_id=None, secondary_email=None, phone_number=None,
                         position='Not a Member', department=None, avatar=None, rs_status=None, facebook_profile=None,
                         linkedin_link=None, robu_start=None, robu_end=None, bracu_start=None, password=None):
        user = self.create_user(
            email=email,
            name=name,
            date_of_birth=date_of_birth,
            student_id=student_id,
            secondary_email=secondary_email,
            phone_number=phone_number,
            position=position,
            department=department,
            avatar=avatar,
            rs_status=rs_status,
            facebook_profile=facebook_profile,
            linkedin_link=linkedin_link,
            robu_start=robu_start,
            robu_end=robu_end,
            bracu_start=bracu_start,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    student_id = models.CharField(max_length=10, null=True, blank=True)
    secondary_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    position = models.CharField(max_length=255, default='Not a Member')
    department = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    rs_status = models.CharField(max_length=255, null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    robu_start = models.DateField(null=True, blank=True)
    robu_end = models.DateField(null=True, blank=True)
    bracu_start = models.DateField(null=True, blank=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name', 'is_admin']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def is_admin_or_panel(self):
        permission= False
        if self.position in ['president', 'vp', 'ags', 'gso', 'gsa'] and self.robu_end==None:
            permission= True
        return self.is_admin or permission
    
    @property
    def is_admin_or_president(self):
        permission= False
        if self.position =='president' and self.robu_end==None:
            permission= True
        return self.is_admin or permission
    
    @property
    def is_admin_or_president_or_vp(self):
        permission= False
        if self.position in ['president', 'vp'] and self.robu_end==None:
            permission= True
        return self.is_admin or permission
    
    @property
    def is_admin_or_dads(self):
        permission= False
        if self.position in ['director','ad','secretary'] and self.robu_end==None:
            permission= True
        return self.is_admin or permission
    
    @property
    def is_admin_or_director(self):
        permission= False
        if self.position =='director' and self.robu_end==None:
            permission= True
        return self.is_admin or permission
    
    @property
    def is_admin_or_director_or_ad(self):
        permission= False
        if self.position in ['director','ad'] and self.robu_end==None:
            permission= True
        return self.is_admin or permission
    
    class Meta:
        indexes = [
            models.Index(fields=['position', 'robu_end']),
        ]