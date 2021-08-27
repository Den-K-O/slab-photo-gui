from postgres import Postgres
import datetime

connstring = "host=192.168.1.72 user=bot password=rpibot dbname=postgres"
db = Postgres(connstring)

def add_quotes_to_strings(input):
    if isinstance(input,str):
        output=f"'{input}'"
    else:
        output=str(input)
    return output  

def create_entry(row):

    next_id=db.all("""select
    last_value
    from
    slabs_id_seq
    """)[0]+1
    
    row["photo_raw"]= f"{next_id}.jpg"
    row["date"]=datetime.date.today().strftime("%m/%d/%Y")
    row["available"]="True"
    row["processed"]="False"
    
    sorted_dict=[(k,v) for k,v in row.items()]
    unzipped =list(zip(*sorted_dict))
    header=unzipped[0]
    values=map(add_quotes_to_strings,unzipped[1])
     
    sql=f"""
            insert
            into slabs ({','.join(header)})
            values ({','.join(values)})
            """
    #print (sql)
    db.run(sql)
    
    return next_id
    
if __name__ == "__main__" :
    import pprint  

    row={
    "wood" : "горіх",
    "thickness": 60,
    }
    id=create_entry(row)
    print("Slab added to DB, id: ",id)