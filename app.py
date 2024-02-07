from flask import Flask, render_template, request, redirect, url_for, Response
import mysql.connector
import io
import csv

app = Flask(__name__)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Kedondong12",
    database = "data_siswa"
)

cursor = db.cursor()

@app.route("/")
def index():
    cursor.execute("SELECT * FROM siswa")
    data = cursor.fetchall()
    return render_template('index.html',data=data)

@app.route('/add', methods=['POST']) 
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']

        # Menambahkan data ke database
        cursor.execute('INSERT INTO siswa (nama,email) VALUES (%s, %s)', (nama, email))
        db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    if request.method == 'GET':
        # Mengambil data berdasarkan id
        cursor.execute('SELECT * FROM siswa WHERE id = %s',(id,))
        data = cursor.fetchone()
        return render_template('edit.html', data=data)
    
    elif request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']

        #Mengupdate data di database
        cursor.execute('UPDATE siswa SET nama=%s, email=%s WHERE id=%s',(nama, email, id))
        db.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    # Menghapus data dari database
    cursor.execute('DELETE FROM siswa WHERE id = %s',(id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/export/csv')
def export_csv():
    cursor.execute('SELECT * FROM siswa')
    data = cursor.fetchall()

    output = io.StringIO()
    csv_writer = csv.writer(output)

    csv_writer.writerow(['id','nama','email'])

    csv_writer.writerows(data)

    response = Response(output.getvalue(),content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=exported.csv'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)