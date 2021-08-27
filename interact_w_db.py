from postgres import Postgres
import datetime
import csv


# connstring = "host=localhost user=postgres password=postgres dbname=postgres"
connstring = "host=192.168.1.190 user=bot password=1234 dbname=kochut_wood_orders"
#db = Postgres(connstring)


dict_structure={
  'TTN': None,
  'additional_furniture_price': None,
  'adress': None,
  'brand': 'випалене',
  'changed_at': datetime.datetime(2021, 8, 23, 11, 27, 2, 488289), # now
  'city': None,
  'country': None,
  'customer': 'Кочут',
  'date': datetime.date(2021, 8, 23), # now
  'deadline_date': datetime.date(2021, 9, 6), # now + d
  'downpayment': None,
  'dummy_2': None,
  'dummy_3': None,
  'dummy_4': None,
  'dummy_5': None,
  'e_mail': None,
  'epoxy_color': 'Смарагдовий',  # ask for color
  'epoxy_finish': 'Натуральний', # ask for staining
  'epoxy_type': 'перламутрова',  # ask for epoxy_type
  'faska': None,
  'finish': 'OSMO 3032',         # ask for finish
  'finished_date': None,
  'height': None,
  'id': 1458,                    # id - default
  'legs': None,
  'legs_color': None,
  'legs_mat': None,
  'legs_price': None,
  'legs_stage': None,
  'manager': 'Йосип',            # ask for manager
  'media': 'Ужгород шоурум',     # Ужгород шоурум
  'note': 'Дощечки Песто 10шт',  # ask for item name and description (select from list)
  'payment_option': None,
  'phone_number': None,
  'pocket_routing': None,
  'price': 780.0,                # price - get from standars table
  'product_type': 'Дощечка',     # ask for item type
  'quantity': 1,                 # ask for quantity
  'resin_volume': 11.5,          # volume - get from standarts table
  'rounding': None,
  'shape': 'Прямокутна',         # irrevelant
  'size_x': 1400,                # size - get from standarts table
  'size_y': 780,                 # size - get from standarts table
  'thickness': 22.0,             # size - get from standarts table
  'user': 'yosyp',               # default
  'username': None,
  'wood': "В'яз",                # ask for wood species
  'wood_price': 30.0,            # get wood price from standars table
  'work_progress': None          # none
  }

def get_fieldname_translations(list_to_translate):
    values=db.all(
    f"""
    SELECT
    name,
    translation
    FROM
    translations
    where name IN ('{"','".join(list_to_translate)}')
    ;
    """)
    translated_dict = {r.name:r.translation for r in values}
    # print (order_id_record[0])
    return translated_dict

def record_to_dict(record):
    data={k:record.__getattribute__(k) for k in record._fields}
    return data

    # 'article' str ask - dropdown - choices in DB, 1
    # 'size' str ask - dropdown (S,M,L,XL) - choices in DB, 2

def get_all_articles(): #article,size):
    values=db.all(
    f"""
    SELECT
    *
    FROM
    standart_items
    ;
    """)

    values_sizes=db.all(
    f"""
    SELECT
    *
    FROM
    standart_items_sizes
    )
    ;
    """)
    out=[record_to_dict(r)  for r in values]
    out_sizes=[record_to_dict(r)  for r in values_sizes]
    return out,out_sizes #"DB_table as dict"

def get_articles(articles): #article,size):
    if  articles:
        values_article=db.all(
        f"""
        SELECT
        *
        FROM
        standart_items
        WHERE
        article IN ('{"','".join(articles)}')
        ;
        """)
        values_sizes=db.all(
        f"""
        SELECT
        *
        FROM
        standart_items_sizes
        WHERE
        article IN ('{"','".join(articles)}')
        ;
        """)
        out=[record_to_dict(r)  for r in values_article]
        out_sizes=[record_to_dict(r)  for r in values_sizes]
        return out,out_sizes #"DB_table as dict"
    else:
        return get_all_articles()

def export_csv(articles=None):
    if articles:
        data,sizes=get_articles(articles)
    headers, records = write_csv(data,"out.csv")
    s_headers, s_records =write_csv(sizes,"out_sizes.csv")
    return headers, records,s_headers, s_records

def import_csv(filename,filename_sizes):
    if articles:
        data,sizes=get_articles(articles)
    headers, records = write_csv(data,"out.csv")
    s_headers, s_records =write_csv(sizes,"out_sizes.csv")
    return headers, records,s_headers, s_records

def read_csv(filename):
    with open(filename, 'r', newline='') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',',quotechar='"')
        rows=list(my_reader)
    header=rows.pop(0)
    return header,rows

def write_csv(data,filename):
    headers=list(zip(*[(k,v) for k,v in data[0].items()]))[0]
    records=[list(zip(*[(k,v) for k,v in row.items()]))[1] for row in data]

    with open(filename, 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        my_writer.writerow(headers)
        my_writer.writerows(records)

    return headers, records

def form_entry(input,defaults):
    '''
    input={
    epoxy_color,
    manager,
    note,
    quantity,
    wood,
    }
    '''

    in_dict={
    'additional_furniture_price':  defaults['additional_furniture_price'], # float from DB
    'd':                           defaults ['d'], # int from DB - days to complete
    'epoxy_color':                 input['epoxy_color'], # str ask - dropdown, 3  - choices in DB
    'epoxy_type':                  defaults['epoxy_type'], # str from DB
    'manager':                     input['manager'], # str ask - dropdown, default, 4  - choices in DB
    'note':                        (defaults['note']+input['note']), # str from DB & formed in gui add note from GUI , 5
    'price':                       defaults['price']                       , # float from DB
    'product_type':                defaults['product_type']                 , # str from DB
    'quantity':                    input['quantity']                      , # int ask, check if divisible by batch (from DB) - spinbox or dropdown, 6
    'resin_volume':                defaults['resin_volume']                 , # float from DB
    'size_x':                      defaults['size_x']                       , # int from DB
    'size_y':                      defaults['size_y']                       , # int from DB
    'thickness':                   defaults['thickness']                    , # int from DB
    'wood':                        input['wood']                             , # str ask - dropdown, 7  - choices in DB
    'wood_price':                  defaults['wood_price'] , # float from DB
    }

    dict_structure_cleaned={
    'additional_furniture_price': str(in_dict[additional_furniture_price]), # handles, legs etc. get from standars table
    'brand': '"лазер"',                   # mostly branded on the laser engraver
    'changed_at': datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), # now
    'city': '"Ужгород"',
    'country': '"Україна"',
    'customer': '"Наявність"',
    'date': datetime.date.today().strftime("%m/%d/%Y"), # now
    'deadline_date': (datetime.date.today()+datetime.timedelta(days=in_dict[d])).strftime("%m/%d/%Y"), # now + d
    'epoxy_color': f'"{in_dict[epoxy_color]}"',  # ask for color
    'epoxy_finish': '"Натуральний"',
    'epoxy_type': f'"{in_dict[epoxy_type]}"',  # ask for epoxy_type
    'finish': '"OSMO 3032"',         #  don't ask for finish
    'manager': f'"{in_dict[manager]}"',            # ask for manager
    'media': '"Ужгород шоурум"',     # Ужгород шоурум
    'note': f'"{in_dict[note]}"',  # ask for item name and description (select from list)
    'price': str(in_dict[price]),                # price - get from standars table
    'product_type': f'"{in_dict[product_type]}"',     # item type - get from standarts table
    'quantity': str(in_dict[quantity]),                 # ask for quantity - check if q-ty is divisible by batch size
    'resin_volume': str(in_dict[resin_volume]),          # volume - get from standarts table
    'size_x': str(in_dict[size_x]),                # size - get from standarts table
    'size_y': str(in_dict[size_y]),                 # size - get from standarts table
    'thickness': str(in_dict[thickness]),             # size - get from standarts table
    'wood': f'"{in_dict[wood]}"',                # ask for wood species
    'wood_price': str(in_dict[wood_price]),            # get wood price from standars table
    }
    return dict_structure_cleaned

def get_order_fields(fields,id):
    values=db.all(
    f"""
    SELECT
    {",".join(fields)}
    FROM
    orders
    WHERE
    ID = '{id}'
    ORDER BY
    id desc
    LIMIT 1 ;
    """)
    # print (order_id_record[0])
    return record_to_dict(values[0])

def create_entry(input,defaults): # form_entry(...) output goes here

   sorted_dict=[(k,v) for k,v in form_entry(input,defaults).items()]
   unzipped =list(zip(*sorted_dict))
   return unzipped
   # db.run(f"""
   #         insert
   #         into test_orders ({}})
   #         values ('{rfid}', {location}, '{timestamp}' )
   #         """)

if __name__ == "__main__" :
    import pprint
    pass
    csv_data=read_csv('out.csv')
    pprint.pprint(csv_data, indent=2)
    print (csv_data[1][0][7])
    # print(', '.join(unzipped[0]))
    # print()
    # print(', '.join(unzipped[1]))
    #pprint.pprint(export_csv(articles=['Мисочка Саторі']), indent=2)


    print()
    print("test succesfull")
