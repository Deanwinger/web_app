import asyncio, logging

import aiomysql

def log(aql, args=())
    logging.info('SQL: %s' % sql)


async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 10086),
        user=kw["user"],
        password=kw["password"],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit= kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
        )

#要执行SELECT语句，用select函数执行
async def select(sql, args, size=None):
    log(sql, args)
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?', '%s'), args, args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows return: %s' % len(rs))
        return rs

#执行INSERT、UPDATE、DELETE语句，用通用的execute()函数
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not commit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                conn.rollback()
            raise
        return affected

def create_args_string(num):
    l=[]
    for n in range(num):
        L.append('?')
        return ','join(L)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default()) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value


class  Field(object):
    """docstring for  field"""
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' %(self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    """docstring for StringField"""
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super(StringField, self).__init__(name, ddl, primary_key, defalt)

class BooleanField(Field):
    """docstring for ooleanField"""
    def __init__(self, name=None, default=False):
        super(BooleanField, self).__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(IntegerField, self).__init__(name, 'bigint', primary_key, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super(FloatField, self).__init__(name, 'real', primary_key, default)

class TextField(Field):
    """docstring for TextField"""
    def __init__(self, name=None, default=None):
        super(TextField, self).__init__(name, 'text', False, default)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))

        mappings =dict()
        fields =[]
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    field.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields =list


     
        









































