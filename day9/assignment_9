from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from pydantic import BaseModel

app = FastAPI()

DATABASE = "people.db"  

class People(BaseModel):
    name : str
    age : int 
    
class PeopleFind(BaseModel):
    name : str
        
def get_db():
    engine = create_engine(f"sqlite:///{DATABASE}")
    return engine
    
@app.get("/all")    
def get_all():
    eng = get_db()
    people_list = []
    with eng.connect() as conn:
        res = conn.execute(text("select name, age from people")).fetchall()
    for row in res:
            people_list.append({"name": row[0], "age": row[1]})
    return people_list
    
@app.post("/helloj")
async def helloj_query( people : People, format = "json"):
    name = people.name
    fformat = format
    age = people.age
    eng = get_db()
    with eng.connect() as conn:
        conn.execute(text("insert into people values(:name, :age)"),
                dict(name = name, age = age))
        conn.commit()
 
@app.get("/helloj")
@app.get("/helloj/{name}/{format}")
@app.get("/helloj/{name}")
@app.get("/helloj")
async def helloj_path( name: str="abc", format:str = "json", people1 : PeopleFind = None):
    name = people1.name if people1 else name 
    fformat = format
    if fformat == "json":
        eng = get_db()
        res = None
        with eng.connect() as conn:
            res = conn.execute(text("select age from people where name=:name"),{"name": name})
            result = res.fetchone()
            if result:
                age = result[0]
                return People(name = name, age = age)
            else:
                return f"{name} is not found in database"
    else :
        return f"provide the correct format to access data"
    
#to run -----> fastapi dev {file-name}  

    
 
    

    
