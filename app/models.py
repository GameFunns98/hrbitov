from datetime import date, timedelta
from . import db

class Hrbitov(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(120), nullable=False)
    adresa = db.Column(db.String(200))
    hroby = db.relationship('Hrob', backref='hrbitov', lazy=True)

class Hrob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oznaceni = db.Column(db.String(50), nullable=False)
    typ = db.Column(db.String(50))
    gps = db.Column(db.String(100))
    hrbitov_id = db.Column(db.Integer, db.ForeignKey('hrbitov.id'), nullable=False)
    zesnuli = db.relationship('Zesnuly', backref='hrob', lazy=True)
    smlouvy = db.relationship('Smlouva', backref='hrob', lazy=True)
    obrazek = db.Column(db.String(200))

class Zesnuly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(120), nullable=False)
    datum_narozeni = db.Column(db.Date)
    datum_umrti = db.Column(db.Date)
    hrob_id = db.Column(db.Integer, db.ForeignKey('hrob.id'))

class Najemce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(120), nullable=False)
    kontaktni_udaje = db.Column(db.String(200))
    smlouvy = db.relationship('Smlouva', backref='najemce', lazy=True)

class Smlouva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ_smlouvy = db.Column(db.String(120))
    datum_uzavreni = db.Column(db.Date)
    doba_trvani = db.Column(db.Integer)  # roky
    hrob_id = db.Column(db.Integer, db.ForeignKey('hrob.id'), nullable=False)
    najemce_id = db.Column(db.Integer, db.ForeignKey('najemce.id'), nullable=False)

    @property
    def datum_expirace(self):
        if self.datum_uzavreni and self.doba_trvani:
            return self.datum_uzavreni + timedelta(days=365*self.doba_trvani)
        return None


# Asociacni tabulky mnoha na mnoho pro zakazky
zakazka_smlouva = db.Table(
    'zakazka_smlouva',
    db.Column('zakazka_id', db.Integer, db.ForeignKey('zakazka.id')),
    db.Column('smlouva_id', db.Integer, db.ForeignKey('smlouva.id')),
)

zakazka_hrob = db.Table(
    'zakazka_hrob',
    db.Column('zakazka_id', db.Integer, db.ForeignKey('zakazka.id')),
    db.Column('hrob_id', db.Integer, db.ForeignKey('hrob.id')),
)


class Zakazka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cislo_zakazky = db.Column(db.String(20), unique=True, nullable=False)
    typ_zakazky = db.Column(db.String(120))
    popis = db.Column(db.Text)
    datum_zadani = db.Column(db.Date)
    datum_dokonceni = db.Column(db.Date)
    stav = db.Column(db.String(20), default='otevřená')
    smlouvy = db.relationship('Smlouva', secondary=zakazka_smlouva,
                              backref=db.backref('zakazky', lazy='dynamic'))
    hroby = db.relationship('Hrob', secondary=zakazka_hrob,
                            backref=db.backref('zakazky', lazy='dynamic'))
    komentare = db.relationship('Komentar', backref='zakazka', lazy=True)
    vykazy = db.relationship('VykazZakazky', backref='zakazka', lazy=True)


class Komentar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    datum = db.Column(db.Date, default=date.today)
    zakazka_id = db.Column(db.Integer, db.ForeignKey('zakazka.id'), nullable=False)


class VykazZakazky(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    polozka = db.Column(db.String(120))
    naklady = db.Column(db.Float)
    jednotka = db.Column(db.String(50))
    pocet = db.Column(db.Float)
    cena_celkem = db.Column(db.Float)
    zakazka_id = db.Column(db.Integer, db.ForeignKey('zakazka.id'), nullable=False)


def generate_cislo_zakazky(year=None):
    year = year or date.today().year
    last = (
        Zakazka.query.filter(Zakazka.cislo_zakazky.like(f"{year}-%"))
        .order_by(Zakazka.cislo_zakazky.desc())
        .first()
    )
    if last:
        seq = int(last.cislo_zakazky.split('-')[1])
    else:
        seq = 0
    return f"{year}-{seq+1:06d}"

def create_test_data():
    if Hrbitov.query.first():
        return
    hrb = Hrbitov(nazev='Městský hřbitov Smečno', adresa='Smečno')
    db.session.add(hrb)
    hrob = Hrob(oznaceni='A1', typ='urnový', hrbitov=hrb)
    db.session.add(hrob)
    zes = Zesnuly(jmeno='Jan Novák', datum_narozeni=date(1950, 1, 1), datum_umrti=date(2020, 1, 1), hrob=hrob)
    db.session.add(zes)
    najemce = Najemce(jmeno='Petr Novák', kontaktni_udaje='petr@example.com')
    db.session.add(najemce)
    smlouva = Smlouva(typ_smlouvy='nájemní', datum_uzavreni=date.today(), doba_trvani=10, hrob=hrob, najemce=najemce)
    db.session.add(smlouva)
    db.session.commit()

    zak = Zakazka(
        cislo_zakazky='2025-000003',
        typ_zakazky='Práce na hřbitově',
        datum_zadani=date(2025, 7, 10),
        stav='otevřená'
    )
    zak.smlouvy.append(smlouva)
    zak.hroby.append(hrob)
    db.session.add(zak)
    db.session.commit()
    kom = Komentar(text='Ukázkový komentář', zakazka=zak)
    db.session.add(kom)
    db.session.commit()
