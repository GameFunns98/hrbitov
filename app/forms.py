from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, SelectMultipleField, TextAreaField, FloatField
from wtforms.validators import DataRequired

class HrbitovForm(FlaskForm):
    nazev = StringField('Název', validators=[DataRequired()])
    adresa = StringField('Adresa')
    submit = SubmitField('Uložit')

class HrobForm(FlaskForm):
    oznaceni = StringField('Označení', validators=[DataRequired()])
    typ = StringField('Typ')
    gps = StringField('GPS / sektor')
    hrbitov_id = IntegerField('ID hřbitova', validators=[DataRequired()])
    submit = SubmitField('Uložit')

class ZesnulyForm(FlaskForm):
    jmeno = StringField('Jméno', validators=[DataRequired()])
    datum_narozeni = DateField('Datum narození')
    datum_umrti = DateField('Datum úmrtí')
    hrob_id = IntegerField('ID hrobu', validators=[DataRequired()])
    submit = SubmitField('Uložit')

class NajemceForm(FlaskForm):
    jmeno = StringField('Jméno', validators=[DataRequired()])
    kontaktni_udaje = StringField('Kontaktní údaje')
    submit = SubmitField('Uložit')

class SmlouvaForm(FlaskForm):
    typ_smlouvy = StringField('Typ smlouvy', validators=[DataRequired()])
    datum_uzavreni = DateField('Datum uzavření')
    doba_trvani = IntegerField('Doba trvání (roky)')
    hrob_id = IntegerField('ID hrobu', validators=[DataRequired()])
    najemce_id = IntegerField('ID nájemce', validators=[DataRequired()])
    submit = SubmitField('Uložit')


class ZakazkaForm(FlaskForm):
    typ_zakazky = StringField('Typ zakázky', validators=[DataRequired()])
    popis = TextAreaField('Popis')
    datum_zadani = DateField('Datum zadání')
    datum_dokonceni = DateField('Datum dokončení')
    smlouvy = SelectMultipleField('Smlouvy', coerce=int)
    hroby = SelectMultipleField('Hroby', coerce=int)
    submit = SubmitField('Uložit')


class KomentarForm(FlaskForm):
    text = TextAreaField('Komentář', validators=[DataRequired()])
    submit = SubmitField('Přidat')


class VykazForm(FlaskForm):
    polozka = StringField('Položka', validators=[DataRequired()])
    naklady = FloatField('Náklady')
    jednotka = StringField('Jednotka')
    pocet = FloatField('Počet')
    cena_celkem = FloatField('Cena celkem')
    submit = SubmitField('Uložit')
