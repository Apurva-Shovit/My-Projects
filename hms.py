import mysql.connector as c
co=c.connect(host='localhost',user='root',passwd='passwd',database='hms')
cu=co.cursor()
if co.is_connected():
    pass
else:
    print('not conncected')
#################################creating a hotels table#####################################
try:
    cu.execute('create table hotels(name varchar(20),city varchar(20),hotel_code int,primary key(name,city))')
except:
    pass
#################################various feature of software#################################
def new_hotel():
    n=input('hotel name:')
    a=''
    for i in n.split():
        a+=i+'_'
    n=a
    c=input('input location city:')
    cd=int(input('input hotel code:'))
    try:
        cu.execute('insert into hotels values (%s,%s,%s)',(n,c,cd))
        co.commit()
    except:
        print('Hotel already exists. Try again!')
    n=n+c
    cu.execute("create table "+str(n)+"(room_no int not null primary key, customer_name varchar(20),Id varchar(20),ID_no int, Allocation_date date, price int not null)")
def add_room(hn):
    n=int(input('enter room number:'))
    p=int(input('enter price:'))
    try:
        cu.execute('insert into '+str(hn)+'(room_no,price) values(%s,%s)',(n,p))
        co.commit()
    except:
        print('Room already exists.Try again!')##note to self= add price update feature;
def allot_room(hn):
    from datetime import date
    cu.execute('select * from '+str(hn)+'')
    data=cu.fetchall()
    print('avalaible rooms are:')
    for i in data:
        if i[1]==None:
            print('Room number=',i[0],',price=',i[5])
    n=int(input('enter room number to be alloted:'))
    na=input(r"enter customer's name:")
    Id=input('enter the ID provided at checkin:')
    idno=int(input('enter the idno of the ID provided:'))
    cu.execute('update '+str(hn)+' set customer_name=%s where room_no=%s',(na,n))
    cu.execute('update '+str(hn)+' set id=%s where room_no=%s',(Id,n))
    cu.execute('update '+str(hn)+' set id_no=%s where room_no=%s',(idno,n))
    cu.execute('update '+str(hn)+' set allocation_date=%s where room_no=%s',(date.today(),n))
    co.commit()
def check_out(hn):
    from datetime import date
    a='log_'+hn
    b=date.today()
    r=int(input('enter checkout room number:'))
    try:
        cu.execute('create table '+str(a)+'(room_no int, customer_name varchar(20),Id varchar(20),ID_no int, Checkin_date date,checkout_date date, total_price int)')
    except:
        pass
    cu.execute('select * from '+str(hn)+' where room_no=%s',(r,))
    data=cu.fetchone()
    cu.execute('insert into '+str(a)+'(room_no,customer_name,Id,id_no,checkin_date) values(%s,%s,%s,%s,%s)',data[:5])
    cu.execute('update '+str(a)+' set checkout_date=%s where room_no=%s',(b,r))
    try:
        price=data[5]*int(str(b-data[4]).split()[0])
    except:
        price=data[5]
    cu.execute('update '+str(a)+' set total_price=%s where room_no=%s',(price,r))
    co.commit()
    cu.execute('update '+str(hn)+' set customer_name=Null where room_no=%s',(r,))
    cu.execute('update '+str(hn)+' set Id=Null where room_no=%s',(r,))
    cu.execute('update '+str(hn)+' set id_no=Null where room_no=%s',(r,))
    cu.execute('update '+str(hn)+' set Allocation_date=Null where room_no=%s',(r,))
    co.commit()
    print('RECEIPT')
    print('customer name:',data[1])
    print('room price:', data[5])
    print('days stayed:',int(price/data[5]))
    print('amount payed:',price)
def current_details(hn):
    cu.execute('select * from '+str(hn)+'')
    data=cu.fetchall()
    print('Room_no','Customer_name','\t','ID','\t','\t','ID_no','\t','Allocation_time','\t','price')
    for i in data:
        for j in i:
            print(j,'\t',end='')
            if i[1]==j:
                print('\t',end='')
        print()
def previous_details(hn):
    z='log_'+hn
    cu.execute('select * from '+str(z)+'')
    data=cu.fetchall()
    print('Room_no','Customer_name','\t','ID','\t','ID_no','\t','Allocation_time','checkout_time','\t','total_price')
    for i in data:
        for j in i:
            print(j,'\t',end='')
            if i[1]==j:
                print('\t',end='')
        print()
#############################################program##########################################################
def execute2(hn):
    print(hn)
    print('1:add_room','2:allot_room','3:check_out','4:current_details','5:previous_details','6:exit',sep='\n')
    n=int(input('enter choice:'))
    if n==1:
        add_room(hn)
        execute2(hn)
    elif n==2:
        allot_room(hn)
        execute2(hn)
    elif n==3:
        check_out(hn)
        execute2(hn)
    elif n==4:
        current_details(hn)
        execute2(hn)
    elif n==5:
        previous_details(hn)
        execute2(hn)
    else:
        execute()
def execute():
    cu.execute('select * from hotels')
    da=cu.fetchall()
    k=1
    for i in da:
        print(k,':',i[0]+i[1])    
        k+=1
    print(k,':','new hotel')
    print(k+1,':','exit')
    n=int(input('enter choice:'))
    hn=''
    for i in range(1,k):
        if n==i:
            hn=da[i-1][0]+da[i-1][1]
    if n==k:
        new_hotel()
        execute()
    for i in range(1,k):
        if n==i:
            hn=da[i-1][0]+da[i-1][1]
            execute2(hn)
            
    if n==k:
        new_hotel()
        execute()
    elif n==k+1:
        pass
execute()

