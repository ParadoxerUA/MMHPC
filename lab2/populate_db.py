from aiopg.sa import create_engine
import sqlalchemy as sa
import asyncio


metadata = sa.MetaData()

forecast = sa.Table('forecast', metadata,
                   sa.Column('id', sa.Integer, primary_key=True),
                   sa.Column('forecast_text', sa.String(150)))


async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS forecast')
        await conn.execute('''CREATE TABLE forecast (
                                  id serial PRIMARY KEY,
                                  forecast_text varchar(150))''')


async def populate():
    async with create_engine(user='student',
                             database='mmhpc',
                             host='127.0.0.1',
                             password='passwd') as engine:

        await create_table(engine)
        async with engine.acquire() as conn:
            with open('divinations', 'r') as f:
                for line in f.readlines():
                    await conn.execute(forecast.insert().values(forecast_text=line))

            async for row in conn.execute(forecast.select()):
                print(row.id, row.val)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(populate())
