from flask import Flask, render_template, flash, request, redirect,url_for
import os
import sqlite3

app = Flask(__name__)
app.secret_key="123"
app.config['UPLOAD_FOLDER']='static/images'

con=sqlite3.connect("mydata.db")
con.execute("create table if not exists image(pid integer primary key,img TEXT)")
con.close

@app.route("/")
def home():
    con = sqlite3.connect("mydata.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from image")
    data = cur.fetchall()
    con.close()
    return render_template("Uploadimages.html",data=data)

@app.route("/upload_file",methods=['POST'])
def upload_file():
    if request.method=='POST':
        if 'files[]' not in request.files:
            flash("No File","danger")
            return redirect(request.url)
        files=request.files.getlist('files[]')
    for file in files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        con=sqlite3.connect("mydata.db")
        cur=con.cursor()
        cur.execute("insert into image(img)values(?)",(file.filename,))
        con.commit()
    flash("Files Upload Successfully","success")
    con=sqlite3.connect("mydata.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("Uploadimages.html",data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=sqlite3.connect("mydata.db")
        cur=con.cursor()
        cur.execute("delete from image where pid=?",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Delete Failed", "danger")
    finally:
        return redirect(url_for("home"))
        con.close()

if __name__ == '__main__':
    app.run(debug=True)
