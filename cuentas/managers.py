from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, correo, password, **kwargs):
        if not correo:
            raise ValueError('The given correo must be set')
        
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, correo, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        
        return self.create_user(correo, password, **kwargs)