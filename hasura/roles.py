class HasuraRoles:
    USER = 'user'
    ANONYMOUS = 'anonymous'
    ADMIN = 'admin'

    @classmethod
    def role(cls, user):
        if user.is_authenticated:
            if user.is_staff:
                return cls.ADMIN
            else:
                return cls.USER
        else:
            return cls.ANONYMOUS
