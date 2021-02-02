from scraper import parseWeather
from flask import Flask, render_template, request, redirect, url_for
import sqlite3 

DB = 'coursework'

app = Flask(__name__)

#******************************** FUNCTION FOR CONTACT US PAGE*****************************
def _parseWeather():
    parseWeather()

def _insertcontact(Name,Email,Subject,Message):
   if request.method == 'POST':
      try:
         Name = request.form['Name']
         Email = request.form['Email']
         Subject = request.form['Subject']
         Message = request.form['Message']
         
         with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO contacts (Name, Email, Subject, Message) VALUES (?,?,?,?)",(Name, Email, Subject, Message) )
            con.commit()
            
      except:
         con.rollback()
         
      
      finally:
         con.close()

#********************************** FUNCTION FOR DONATION PAGE***********************************************
def _insertcard(card_number, expiration, cvc, card_owner_name, amount):
   if request.method == 'POST':
      try:
         card_number = request.form['card_number']
         expiration = request.form['expiration']
         cvc = request.form['cvc']
         card_owner_name = request.form['card_owner_name']
         amount = request.form['amount']
         
         with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO makedonations (card_number, expiration, cvc, card_owner_name, amount) VALUES (?,?,?,?,?)",(card_number, expiration, cvc, card_owner_name, amount) )
            con.commit()
            
      except:
         con.rollback()
         
      
      finally:
         con.close()

#*******************************************FUNCTION FOR COMMENT PAGE***********************************************
def _insertcomment(Name,Message):
   if request.method == 'POST':
      try:
         Name = request.form['Name']
         Message = request.form['Message']
         
         with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO comments (Name, Message) VALUES (?,?)",(Name, Message) )
            con.commit()
            
      except:
         con.rollback()
         
      
      finally:
         con.close()



#************************** HOMEPAGE **********************************************

@app.route('/')
def goto_index():
        _parseWeather()
        return render_template('index.html')

#******************** CONTACT PAGE***********************************************
@app.route('/contact_us')
def goto_contact_us():
        return render_template('contact_us.html')

@app.route('/insertcontact', methods=["POST"])
def insertcontact():
        _insertcontact(request.form['Name'], request.form['Email'], request.form['Subject'], request.form['Message'])
        return redirect(url_for('viewcontacts'))

@app.route('/viewcontacts', methods=['POST', 'GET'])
def viewcontacts():
        """
        Accepts POST requests, and processes the form;
        Redirect to view when completed.
        """

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacts")
        rv = cursor.fetchall()
        cursor.close()
        return render_template("viewcontacts.html",table=rv)

#*********************************** COMMENT PAGE ***********************************************
@app.route('/comments')
def goto_comments():
        return render_template('comments.html')

@app.route('/insertcomment', methods=["POST"])
def insertcomment():
        _insertcomment(request.form['Name'], request.form['Message'])
        return render_template('comments.html')

#**************************************** DONATION PAGE***********************************************
@app.route('/donations')
def goto_donations():
        return render_template('makepayments.html')
@app.route('/insertcard', methods=["POST"])
def insertcard():
        _insertcard(request.form['card_number'],request.form['expiration'],request.form['cvc'], request.form['card_owner_name'],request.form['amount'])
        return redirect(url_for('viewdonations'))

@app.route('/viewdonations', methods=['POST', 'GET'])
def viewdonations():
        """
        Accepts POST requests, and processes the form;
        Redirect to view when completed.
        """

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM makedonations")
        rv = cursor.fetchall()
        cursor.close()
        return render_template("viewdonations.html",donated=rv)

#**************************************** WEATHER PAGE***********************************************
@app.route('/weather')
def weather():
    connection = sqlite3.connect(DB)
    cursor: Cursor = connection.cursor()
    cursor.execute("SELECT * FROM weather")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("weather.html",forecast=rv)


if  __name__ == '__main__':
        app.run()
        

