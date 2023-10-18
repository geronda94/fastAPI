import asyncpg




class DB:

    def __init__(self, user, psw, db, host='localhost', port='5432'):
        self.__user = user
        self.__psw = psw
        self.__host = host
        self.__port = port
        self.__db = db
        self.conn = None


    async def connect(self):
        try:
            self.conn = await asyncpg.connect(f'postgresql://{self.__user}:{self.__psw}@{self.__host}:{self.__port}/{self.__db}')
        except Exception as ex:
            print(ex)




    async def disconnect(self):
        if self.conn:
            try:
                await self.conn.close()
            except Exception as ex:
                print(ex)
        else:
            print('No connection self.conn in class DB')


    async def request(self, request, *args):
        try:
            return await self.conn.fetch(request, *args)
        except Exception as ex:
            print(ex)
            return False
    


    async def request_with(self,  request, *args):
        try:
            await self.connect()
            res = await self.request(request, *args)
            await self.disconnect()
            return res
        
        except Exception as ex:
            print(ex)
            return False


db = DB('geronda', '1994', 'test')

