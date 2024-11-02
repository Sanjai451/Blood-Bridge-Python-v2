# from flask import Flask, render_template, redirect, url_for, flash, request
# from flask_sqlalchemy import SQLAlchemy 

# app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sanjai%40451@localhost/lifelink_db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:spiderman_@database-1.c3g8kocwsx8i.eu-north-1.rds.amazonaws.com:3306'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:spiderman_@database-1.c3g8kocwsx8i.eu-north-1.rds.amazonaws.com:3306/database-1'
# # app.config['MYSQL_DATABASE_HOST'] = 'database-1.c3g8kocwsx8i.eu-north-1.rds.amazonaws.com:3306' # Specify Endpoint
# # app.config['MYSQL_DATABASE_USER'] = 'admin' # Specify Master username
# # app.config['MYSQL_DATABASE_PASSWORD'] = 'spiderman_' # Specify Master password
# # app.config['MYSQL_DATABASE_DB'] = 'lifelink_db' # Specify database name

# app.config['SECRET_KEY'] = 'your_secret_key'
# db = SQLAlchemy(app)

# # Models
# class BloodRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     blood_type = db.Column(db.String(10), nullable=False)
#     name = db.Column(db.String(19), nullable=False)
#     contact_info = db.Column(db.String(20), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     priority = db.Column(db.Boolean, default=True)
#     requestor_type = db.Column(db.String(20), nullable=False)  # Add type to identify acceptor


# class Inventory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     blood_type = db.Column(db.String(10), nullable=False)
#     stock_level = db.Column(db.Integer, nullable=False)

# class BloodDonation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     donor_name = db.Column(db.String(100), nullable=False)
#     blood_type = db.Column(db.String(10), nullable=False)
#     contact_info = db.Column(db.String(100), nullable=False)
#     address = db.Column(db.String(200), nullable=True)  # Add address field


# # Routes
# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/dashboard')
# def dashboard():
#     blood_requests = BloodRequest.query.all()
#     donors = BloodDonation.query.all()  # Fetch all donors
#     inventory = Inventory.query.all()
#     return render_template('dashboard.html', blood_requests=blood_requests, donors=donors, inventory=inventory)


# @app.route('/request_blood', methods=['GET', 'POST'])
# def request_blood():
#     if request.method == 'POST':
#         blood_type = request.form.get('blood_type')
#         quantity = int(request.form.get('quantity'))
#         requestor_type = request.form.get('requestor_type')  # Ensure this retrieves the value from the form
#         name = request.form.get('name')  # Ensure this retrieves the value from the form
#         contact_info = request.form.get('contact_info')  # Ensure this retrieves the value from the form
        
#         # Check if requestor_type is None or empty
#         if not requestor_type:
#             flash('Requestor type is required.')
#             return redirect(url_for('request_blood'))
        
#         new_request = BloodRequest(blood_type=blood_type, quantity=quantity, requestor_type=requestor_type,name=name,contact_info=contact_info)
#         db.session.add(new_request)
#         db.session.commit()
#         flash('Blood request submitted!')
#         return redirect(url_for('dashboard'))
#     return render_template('request_blood.html')



# @app.route('/update_inventory', methods=['GET', 'POST'])
# def update_inventory():
#     if request.method == 'POST':
#         blood_type = request.form.get('blood_type')
#         stock_level = int(request.form.get('stock_level'))
#         inventory = Inventory.query.filter_by(blood_type=blood_type).first()
#         if inventory:
#             inventory.stock_level = stock_level
#         else:
#             new_inventory = Inventory(blood_type=blood_type, stock_level=stock_level)
#             db.session.add(new_inventory)
#         db.session.commit()
#         flash('Inventory updated!')
#         return redirect(url_for('dashboard'))
#     return render_template('update_inventory.html')


# @app.route('/donate_blood', methods=['GET', 'POST'])
# def donate_blood():
#     if request.method == 'POST':
#         donor_name = request.form.get('donor_name')
#         blood_type = request.form.get('blood_type')
#         contact_info = request.form.get('contact_info')
#         address = request.form.get('address')  # Get address from the form
#         new_donor = BloodDonation(donor_name=donor_name, blood_type=blood_type, contact_info=contact_info, address=address)
#         db.session.add(new_donor)
        
#          # Update inventory
#         inventory = Inventory.query.filter_by(blood_type=blood_type).first()
#         if inventory:
#             inventory.stock_level += 1  # Increment stock by 1 (or adjust quantity as needed)
#         else:
#             # If blood type does not exist in inventory, add a new record
#             new_inventory = Inventory(blood_type=blood_type, stock_level=1)
#             db.session.add(new_inventory)

#         # Commit changes to both tables
#         db.session.commit()

#         flash('Donor information submitted and inventory updated!')
#         return redirect(url_for('dashboard'))
#     return render_template('donate_blood.html')


# # Run the application
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, redirect, url_for, flash, request
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'database-1.c3g8kocwsx8i.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'spiderman_',
    'database': 'lifelink',
    'port': 3306
}

# Function to get a new connection
def get_db_connection():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port']
    )
    return connection

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM BloodRequest")
        blood_requests = cursor.fetchall()

        cursor.execute("SELECT * FROM BloodDonation")
        donors = cursor.fetchall()

        cursor.execute("SELECT * FROM Inventory")
        inventory = cursor.fetchall()

    connection.close()
    return render_template('dashboard.html', blood_requests=blood_requests, donors=donors, inventory=inventory)

@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        quantity = int(request.form.get('quantity'))
        requestor_type = request.form.get('requestor_type')
        name = request.form.get('name')
        contact_info = request.form.get('contact_info')

        if not requestor_type:
            flash('Requestor type is required.')
            return redirect(url_for('request_blood'))

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO BloodRequest (blood_type, quantity, requestor_type, name, contact_info) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (blood_type, quantity, requestor_type, name, contact_info))
            connection.commit()

        connection.close()
        flash('Blood request submitted!')
        return redirect(url_for('dashboard'))

    return render_template('request_blood.html')

@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        stock_level = int(request.form.get('stock_level'))
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Inventory WHERE blood_type = %s", (blood_type,))
            inventory = cursor.fetchone()

            if inventory:
                cursor.execute("UPDATE Inventory SET stock_level = %s WHERE blood_type = %s", (stock_level, blood_type))
            else:
                sql = "INSERT INTO Inventory (blood_type, stock_level) VALUES (%s, %s)"
                cursor.execute(sql, (blood_type, stock_level))
            connection.commit()

        connection.close()
        flash('Inventory updated!')
        return redirect(url_for('dashboard'))

    return render_template('update_inventory.html')

@app.route('/donate_blood', methods=['GET', 'POST'])
def donate_blood():
    if request.method == 'POST':
        donor_name = request.form.get('donor_name')
        blood_type = request.form.get('blood_type')
        contact_info = request.form.get('contact_info')
        address = request.form.get('address')

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO BloodDonation (donor_name, blood_type, contact_info, address) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (donor_name, blood_type, contact_info, address))
            
            # Update inventory
            cursor.execute("SELECT * FROM Inventory WHERE blood_type = %s", (blood_type,))
            inventory = cursor.fetchone()

            if inventory:
                cursor.execute("UPDATE Inventory SET stock_level = stock_level + 1 WHERE blood_type = %s", (blood_type,))
            else:
                cursor.execute("INSERT INTO Inventory (blood_type, stock_level) VALUES (%s, %s)", (blood_type, 1))

            connection.commit()

        connection.close()
        flash('Donor information submitted and inventory updated!')
        return redirect(url_for('dashboard'))

    return render_template('donate_blood.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
