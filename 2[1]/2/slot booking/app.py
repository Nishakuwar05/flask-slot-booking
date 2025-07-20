from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import mysql.connector as mq
from mysql.connector import Error
from markupsafe import Markup
from datetime import datetime
import mailing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

def dbconnection():
    con = mq.connect(host='localhost', database='slotbooking',user='root',password='root')
    return con



@app.route('/')
def loginpage():
    return render_template('login.html', title='Login')

@app.route('/aboutpage')
def aboutpage():
    return render_template('about.html', title='Loaboutgin')

@app.route('/registerpage')
def registerpage():
    return render_template('register.html', title='register')

@app.route('/addsubadminpage')
def addsubadminpage():
    return render_template('addsubadmin.html', title='subadmin')


@app.route('/adminhomepage')
def adminhomepage():
    return render_template('adminhome.html', title='admin home')


@app.route('/subadminprofile')
def subadminprofile():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from subadmin where id={}".format(int(session['said'])))
    res = cursor.fetchall()
    return render_template('subprofile.html', title='admins',res=res)

@app.route('/manageadminpage')
def manageadminpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from subadmin")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data Found</h3>")
        flash(message)
        return render_template('manageadmin.html')
    else:
        return render_template('manageadmin.html', title='admins',res=res)
    
@app.route('/bookslotpage')
def bookslotpage():
    id = request.args.get('id')
    return render_template('bookslot.html', title='bookslot', id = id)

@app.route('/viewsbookingspage')
def viewsbookingspage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("""
    SELECT * 
    FROM bookings 
    LEFT JOIN user ON bookings.uid = user.id left join events on bookings.evid=events.id
    ORDER BY 
      CASE bookings.status
        WHEN 'Pending' THEN 1
        WHEN 'Accepted' THEN 2
        WHEN 'Rejected' THEN 3
        ELSE 4
      END
""")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data Found</h3>")
        flash(message)
        return render_template('bookings.html')
    else:
        return render_template('bookings.html', title='bookings',res=res)
    
@app.route('/viewsbookingspagesadmin')
def viewsbookingspagesadmin():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from bookings left join user on bookings.uid=user.id")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data Found</h3>")
        flash(message)
        return render_template('bookingsforsub.html')
    else:
        return render_template('bookingsforsub.html', title='bookings',res=res)

@app.route('/mybookings')
def mybookings():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from bookings left join events on bookings.evid=events.id where bookings.uid={}".format(int(session['uid'])))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data Found</h3>")
        flash(message)
        return render_template('viewmybookings.html')
    else:
        return render_template('viewmybookings.html', title='bookings',res=res)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        regno = request.form['regno']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from user where email='{}' or regno='{}' or phone='{}'".format(email,regno,phone))
        res = cursor.fetchall()
        if res==[]:
                cursor.execute("insert into user(name,regno,phone,email,password)values('{}','{}','{}','{}','{}')".format(
                    name,regno,phone,email,password))
                con.commit()
                con.close()
                message = Markup("<h3>Success! Registration success</h3>")
                flash(message)
                return redirect(url_for('registerpage'))
        else:
           message = Markup("<h3>Failed! Email Id or Phone number or Register number already Exist</h3>")
           flash(message)
           return redirect(url_for('registerpage'))



@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html', title='admin home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        ltype = request.form['ltype']
        con = dbconnection()
        cursor = con.cursor()
        if ltype=='admin':
            cursor.execute("select * from admin where email='{}' and password='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return render_template('login.html', title='login')
            else:
                #session['did']=res[0][0]
                return redirect(url_for('adminhomepage'))
        elif ltype=='subadmin':
                cursor.execute("select * from subadmin where email='{}' and password='{}'".format(email,password))
                res = cursor.fetchall()
                if res==[]:
                    message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                    flash(message)
                    return render_template('login.html', title='login')
                else:
                    session['said']=res[0][0]
                    return redirect(url_for('subadminprofile'))
                    #return render_template('subprofile.html', title='subadminprofile',res=res)
                
        else:
            cursor.execute("select * from user where email='{}' and password='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return render_template('login.html', title='login')
            else:
                session['uid'] = res[0][0]
                return redirect(url_for('userdashboard'))

@app.route('/book',methods=['GET','POST'])
def book():
    id = request.form['id']
    date = request.form['date']
    gender = request.form['gender']
    comitee = request.form['comitee']
    uid = session['uid']
    status = "Pending"
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from bookings where uid={} and bdate='{}' and evid={}".format(int(uid),date,int(id)))
    res = cursor.fetchall()
    if res==[]:
        '''cursor.execute("UPDATE events SET noslots=CAST(noslots AS UNSIGNED) - 1 WHERE id=%s", (id,))
        con.commit()'''
        cursor.execute("insert into bookings(bdate,gender,comitee,status,uid,evid)values('{}','{}','{}','{}',{},{})".format(
            date,gender,comitee,status,int(uid),id))
        con.commit()
        con.close()
        message = Markup("<h3>Booking Success!</h3>")
        flash(message)
        return redirect(url_for('bookslotpage'))
    else:
        message = Markup("<h3>You have already booked slot for this date</h3>")
        flash(message)
        return redirect(url_for('bookslotpage'))
    
    
@app.route('/accept')
def accept():
    id  = request.args.get("id")
    evid  = request.args.get("evid")
    con = dbconnection()
    cursor = con.cursor()
    
    status = "Accepted"
    cursor.execute("update bookings set status='{}' where id={}".format(status,int(id)))
    con.commit()
    
    cursor.execute("UPDATE events SET noslots=CAST(noslots AS UNSIGNED) - 1 WHERE id=%s", (evid,))
    con.commit()
    
    cursor.execute("select * from bookings inner join user on bookings.uid=user.id where bookings.id={}".format(int(id)))
    res = cursor.fetchall()
    email = res[0][11]
    subject = "SLOT BOOKING UPDATE"
    body = "Dear User,\nYour Slot booking has been Approved by admin."
    try:
        
        mailing.mailsend(email,subject,body)
    except:
        print("Error sending email")
    con.close()
    return redirect(url_for('viewsbookingspage'))

@app.route('/reject')
def reject():
    id  = request.args.get("id")
    con = dbconnection()
    cursor = con.cursor()
    status = "Rejected"
    cursor.execute("update bookings set status='{}' where id={}".format(status,int(id)))
    con.commit()
    cursor.execute("select * from bookings inner join user on bookings.uid=user.id where bookings.id={}".format(int(id)))
    res = cursor.fetchall()
    email = res[0][11]
    subject = "SLOT BOOKING UPDATE"
    body = "Dear User,\nYour Slot booking has been Rejected by admin."
    try:
        
        mailing.mailsend(email,subject,body)
    except:
        print("Error sending email")
    con.close()
    return redirect(url_for('viewsbookingspage'))
    
@app.route('/accept2')
def accept2():
    id  = request.args.get("id")
    con = dbconnection()
    cursor = con.cursor()
    status = "Accepted"
    cursor.execute("update bookings set status='{}' where id={}".format(status,int(id)))
    con.commit()
    cursor.execute("UPDATE events SET noslots=CAST(noslots AS UNSIGNED) - 1 WHERE id=%s", (evid,))
    con.commit()
    cursor.execute("select * from bookings inner join user on bookings.uid=user.id where bookings.id={}".format(int(id)))
    res = cursor.fetchall()
    email = res[0][11]
    subject = "SLOT BOOKING UPDATE"
    body = "Dear User,\nYour Slot booking has been Approved by Sub Admin."
    try:
        
        mailing.mailsend(email,subject,body)
    except:
        print("Error sending email")
    con.close()
    return redirect(url_for('viewsbookingspagesadmin'))

@app.route('/reject2')
def reject2():
    id  = request.args.get("id")
    con = dbconnection()
    cursor = con.cursor()
    status = "Rejected"
    cursor.execute("update bookings set status='{}' where id={}".format(status,int(id)))
    con.commit()
    cursor.execute("select * from bookings inner join user on bookings.uid=user.id where bookings.id={}".format(int(id)))
    res = cursor.fetchall()
    email = res[0][11]
    subject = "SLOT BOOKING UPDATE"
    body = "Dear User,\nYour Slot booking has been Rejected by Sub Admin."
    try:
        
        mailing.mailsend(email,subject,body)
    except:
        print("Error sending email")
    con.close()
    return redirect(url_for('viewsbookingspagesadmin'))

@app.route('/addsubadmin', methods=['GET', 'POST'])
def addsubadmin():
    if request.method == 'POST':
        name = request.form['name']
        regno = request.form['regno']
        aclass = request.form['class']
        section = request.form['section']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from subadmin where email='{}' or regno='{}' or phone='{}'".format(email,regno,phone))
        res = cursor.fetchall()
        if res==[]:
                cursor.execute("insert into subadmin(name,regno,class,section,phone,email,password)values('{}','{}','{}','{}','{}','{}','{}')".format(
                    name,regno,aclass,section,phone,email,password))
                con.commit()
                con.close()
                message = Markup("<h3>Success! Admin Added</h3>")
                flash(message)
                return redirect(url_for('addsubadminpage'))
        else:
           message = Markup("<h3>Failed! Email Id or Phone number or Register number already Exist</h3>")
           flash(message)
           return redirect(url_for('addsubadminpage'))
    
    
@app.route('/remove')
def remove():
    id  = request.args.get("id")
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("delete from subadmin where id={}".format(int(id)))
    con.commit()
    con.close()
    return redirect(url_for('manageadminpage'))

@app.route('/cancelslot')
def cancelslot():
    id  = request.args.get("id")
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("delete from bookings where id={}".format(int(id)))
    con.commit()
    con.close()
    return redirect(url_for('mybookings'))


@app.route('/updatesubadmin', methods=['GET', 'POST'])
def updatesubadmin():
    id  = request.form['id']
    name = request.form['name']
    regno = request.form['regno']
    aclass = request.form['class']
    section = request.form['section']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update subadmin set class='{}', section='{}', password='{}' where id={}".format(
        aclass, section, password, int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Profile updated</h3>")
    flash(message)
    return redirect(url_for('subadminprofile'))

@app.route('/addeventpage')
def addeventpage():
    return render_template('addevent.html', title='bookslot')

@app.route('/addevent', methods=['GET', 'POST'])
def addevent():
    if request.method == 'POST':
        evname = request.form['evname']
        evtype = request.form['evtype']
        noslots = request.form['noslots']
       
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("insert into events(evname,evtype,noslots)values('{}','{}','{}')".format(
            evname,evtype,noslots))
        con.commit()
        con.close()
        message = Markup("<h3>Success! Event Added</h3>")
        flash(message)
        return redirect(url_for('addeventpage'))
        

@app.route('/aviewevents')
def aviewevents():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from events")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data Found</h3>")
        flash(message)
        return render_template('aviewevents.html')
    else:
        return render_template('aviewevents.html', title='events',res=res) 
       
@app.route('/upcomingevents')
def upcomingevents():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from events where noslots>0")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data Found</h3>")
        flash(message)
        return render_template('uviewevents.html')
    else:
        return render_template('uviewevents.html', title='events',res=res) 


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
