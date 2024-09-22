from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField, URLField
from wtforms.validators import DataRequired
import csv
from validators import URL
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
csrf = CSRFProtect(app)
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location On Google Maps(URL)', validators=[DataRequired(),  URL(require_tld=True, message="Please enter a valid URL")])
    open_time = TimeField('Open Time', format="%H:%M",  validators=[DataRequired()])
    close_time = TimeField('Close Time', format="%H:%M", validators=[DataRequired()])
    coffee_rating = SelectField('☕️Coffee Rating', choices=[('✘','✘'), ('☕️','☕️'), ('☕️☕️','☕️☕️'), ('☕️☕️☕️','☕️☕️☕️'), ('☕️☕️☕️☕️','☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️','☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi_rating = SelectField('💪Wifi Rating', choices=[('✘','✘'), ('💪','💪'), ('💪💪','💪💪'), ('💪💪💪','💪💪💪'), ('💪💪💪💪','💪💪💪💪'), ('💪💪💪💪💪','💪💪💪💪💪')], validators=[DataRequired()])
    power_rating = SelectField('🔌Power Rating', choices=[('✘','✘'), ('🔌','🔌'), ('🔌🔌','🔌🔌'), ('🔌🔌🔌','🔌🔌🔌'), ('🔌🔌🔌🔌','🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌','🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('💨Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        open_time_12hr = form.open_time.data.strftime('%I:%M %p')
        close_time_12hr = form.close_time.data.strftime('%I:%M %p')
        print("True")
        with open("cafe-data.csv", mode="a", newline='', encoding="utf-8") as file:
            file.write(f"\n{form.cafe.data},{form.location.data},{open_time_12hr},{close_time_12hr},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_rating.data}")
        return render_template('success.html', form=form, message="Cafe added!")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes', methods=['GET', 'POST'])
def cafes():
    list_of_rows = []
    if request.method == 'GET':
        with open('cafe-data.csv', 'r', newline='', encoding="utf-8") as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            for row in csv_data:
                list_of_rows.append(row)
                print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
