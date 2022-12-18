import asyncio
from prisma import Prisma
from graphql import GraphQLError
from datetime import datetime
import json
from rocketry import Rocketry
from rocketry.conds import daily

app = Rocketry(execution='async')
prisma = Prisma()

# schedule.every().day.at("17:00").do(resolve_absent)
app.task(daily.after("17:00"), func_name="resolve_absent")   

async def resolve_user_time_logs(obj, info, user_id:int):
    try:
        await prisma.connect()
            
        logs = await prisma.log.find_many(
            where={
                'user_id': int(user_id)
            },
            order={
                'id': 'asc'
            }
        )
        
        if not logs:
            raise GraphQLError(f'No logs found for user with id {user_id}')
        return logs
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        
async def resolve_add_time_in_logs(obj, info, user_id):
    try:
        await prisma.connect()
        user_id = int(user_id)
        time_in = str(datetime.now())
        indicator = check_lateness(datetime.now().strftime('%H:%M:%S'))
        
        log = await prisma.log.create(
            data ={
                'user_id': user_id,
                'time_in': time_in,
                'indicator': indicator
            }
        )
        return log
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        

async def resolve_add_time_out_logs(obj, info, user_id):
    try:
        await prisma.connect()
        user = await prisma.log.find_first(
            where={
                'user_id' : int(user_id)
            }
        )
        if not user:
            raise GraphQLError(f'User with id {user_id} does not exists')
        elif user.time_in == "":
            return GraphQLError(f'You have to clock in first')
        else:
            user_id = int(user_id)
            time_out = datetime.now()
            
            log = await prisma.log.update(
                data ={
                    'time_out': json.dumps(time_out)
                },
                where = {
                    'user_id': user_id
                }
            )
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        
def check_lateness(time):
    if time >= '06:00:00' and time <= '07:30:00':
        return 'Early'
    elif time >= '07:30:00' and time <= '08:30:00':
        return 'In time'
    else:
        return 'Late'
     
async def resolve_absent(obj, info):
    try:
        await prisma.connect()
        logs = await prisma.log.find_many()
        for log in logs:
            if log.time_in == "":
                await prisma.log.update(
                    where={'id': log.id}, 
                    data={'absent': True})
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        

    
# while True:
#     schedule.run_pending()
#     time.sleep(1)