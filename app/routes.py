import io
from flask import render_template, redirect, url_for, flash, send_file
from . import app, db
from .models import (
    Hrbitov,
    Hrob,
    Zesnuly,
    Najemce,
    Smlouva,
    Zakazka,
    Komentar,
    VykazZakazky,
    generate_cislo_zakazky,
)
from .forms import (
    HrbitovForm,
    HrobForm,
    ZesnulyForm,
    NajemceForm,
    SmlouvaForm,
    ZakazkaForm,
    KomentarForm,
    VykazForm,
)
from .utils import generate_qr, generate_pdf

@app.route('/')
def index():
    hrbitovy = Hrbitov.query.all()
    return render_template('index.html', hrbitovy=hrbitovy)

@app.route('/hrbitov/<int:hrbitov_id>')
def hrbitov_detail(hrbitov_id):
    hrbitov = Hrbitov.query.get_or_404(hrbitov_id)
    return render_template('hrbitov_detail.html', hrbitov=hrbitov)

@app.route('/pridat_hrbitov', methods=['GET', 'POST'])
def pridat_hrbitov():
    form = HrbitovForm()
    if form.validate_on_submit():
        hrb = Hrbitov(nazev=form.nazev.data, adresa=form.adresa.data)
        db.session.add(hrb)
        db.session.commit()
        flash('Hřbitov přidán')
        return redirect(url_for('index'))
    return render_template('pridat_hrbitov.html', form=form)

@app.route('/pridat_hrob', methods=['GET', 'POST'])
def pridat_hrob():
    form = HrobForm()
    if form.validate_on_submit():
        h = Hrob(oznaceni=form.oznaceni.data, typ=form.typ.data, gps=form.gps.data, hrbitov_id=form.hrbitov_id.data)
        db.session.add(h)
        db.session.commit()
        flash('Hrob přidán')
        return redirect(url_for('hrbitov_detail', hrbitov_id=form.hrbitov_id.data))
    return render_template('pridat_hrob.html', form=form)

@app.route('/pridat_zesnuly', methods=['GET', 'POST'])
def pridat_zesnuly():
    form = ZesnulyForm()
    if form.validate_on_submit():
        z = Zesnuly(jmeno=form.jmeno.data, datum_narozeni=form.datum_narozeni.data, datum_umrti=form.datum_umrti.data, hrob_id=form.hrob_id.data)
        db.session.add(z)
        db.session.commit()
        flash('Zesnulý přidán')
        return redirect(url_for('hrbitov_detail', hrbitov_id=Hrob.query.get(form.hrob_id.data).hrbitov_id))
    return render_template('pridat_zesnuly.html', form=form)

@app.route('/pridat_najemce', methods=['GET', 'POST'])
def pridat_najemce():
    form = NajemceForm()
    if form.validate_on_submit():
        n = Najemce(jmeno=form.jmeno.data, kontaktni_udaje=form.kontaktni_udaje.data)
        db.session.add(n)
        db.session.commit()
        flash('Nájemce přidán')
        return redirect(url_for('index'))
    return render_template('pridat_najemce.html', form=form)

@app.route('/pridat_smlouvu', methods=['GET', 'POST'])
def pridat_smlouvu():
    form = SmlouvaForm()
    if form.validate_on_submit():
        s = Smlouva(
            typ_smlouvy=form.typ_smlouvy.data,
            datum_uzavreni=form.datum_uzavreni.data,
            doba_trvani=form.doba_trvani.data,
            hrob_id=form.hrob_id.data,
            najemce_id=form.najemce_id.data,
        )
        db.session.add(s)
        db.session.commit()
        flash('Smlouva přidána')
        return redirect(url_for('smlouvy'))
    return render_template('pridat_smlouvu.html', form=form)

@app.route('/smlouvy')
def smlouvy():
    smlouvy = Smlouva.query.all()
    return render_template('smlouvy.html', smlouvy=smlouvy)

@app.route('/smlouva/<int:smlouva_id>/pdf')
def smlouva_pdf(smlouva_id):
    sml = Smlouva.query.get_or_404(smlouva_id)
    html = render_template('smlouva_pdf.html', smlouva=sml)
    pdf = generate_pdf(html)
    return send_file(pdf, download_name='smlouva.pdf', as_attachment=True)

@app.route('/hrob/<int:hrob_id>/qr')
def hrob_qr(hrob_id):
    qr = generate_qr(url_for('hrob_detail', hrob_id=hrob_id, _external=True))
    return send_file(qr, mimetype='image/png')

@app.route('/hrob/<int:hrob_id>')
def hrob_detail(hrob_id):
    hrob = Hrob.query.get_or_404(hrob_id)
    return render_template('hrob_detail.html', hrob=hrob)

@app.route('/export_zesnuli')
def export_zesnuli():
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Jméno', 'Datum narození', 'Datum úmrtí', 'Hrob'])
    for z in Zesnuly.query.all():
        cw.writerow([z.jmeno, z.datum_narozeni, z.datum_umrti, z.hrob.oznaceni])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', download_name='zesnuli.csv', as_attachment=True)


@app.route('/zakazky')
def zakazky():
    zakazky = Zakazka.query.all()
    return render_template('zakazky/index.html', zakazky=zakazky)


@app.route('/zakazky/novy', methods=['GET', 'POST'])
def nova_zakazka():
    form = ZakazkaForm()
    form.smlouvy.choices = [(s.id, f"{s.id} - {s.hrob.oznaceni}") for s in Smlouva.query.all()]
    form.hroby.choices = [(h.id, h.oznaceni) for h in Hrob.query.all()]
    if form.validate_on_submit():
        zak = Zakazka(
            cislo_zakazky=generate_cislo_zakazky(),
            typ_zakazky=form.typ_zakazky.data,
            popis=form.popis.data,
            datum_zadani=form.datum_zadani.data,
            datum_dokonceni=form.datum_dokonceni.data,
        )
        for sid in form.smlouvy.data:
            zak.smlouvy.append(Smlouva.query.get(sid))
        for hid in form.hroby.data:
            zak.hroby.append(Hrob.query.get(hid))
        db.session.add(zak)
        db.session.commit()
        flash('Zakázka vytvořena')
        return redirect(url_for('zakazky'))
    return render_template('zakazky/novazakazka.html', form=form)


@app.route('/zakazka/<int:zakazka_id>', methods=['GET', 'POST'])
def zakazka_detail(zakazka_id):
    zak = Zakazka.query.get_or_404(zakazka_id)
    koment_form = KomentarForm(prefix='kom')
    vykaz_form = VykazForm(prefix='vyk')
    if koment_form.validate_on_submit() and koment_form.submit.data:
        kom = Komentar(text=koment_form.text.data, zakazka=zak)
        db.session.add(kom)
        db.session.commit()
        return redirect(url_for('zakazka_detail', zakazka_id=zak.id))
    if vykaz_form.validate_on_submit() and vykaz_form.submit.data:
        vyk = VykazZakazky(
            polozka=vykaz_form.polozka.data,
            naklady=vykaz_form.naklady.data,
            jednotka=vykaz_form.jednotka.data,
            pocet=vykaz_form.pocet.data,
            cena_celkem=vykaz_form.cena_celkem.data,
            zakazka=zak,
        )
        db.session.add(vyk)
        db.session.commit()
        return redirect(url_for('zakazka_detail', zakazka_id=zak.id))
    return render_template('zakazky/detail.html', zakazka=zak, koment_form=koment_form, vykaz_form=vykaz_form)


@app.route('/zakazka/<int:zakazka_id>/pdf')
def zakazka_pdf(zakazka_id):
    zak = Zakazka.query.get_or_404(zakazka_id)
    html = render_template('zakazky/detail.html', zakazka=zak, koment_form=KomentarForm(), vykaz_form=VykazForm())
    pdf = generate_pdf(html)
    return send_file(pdf, download_name='zakazka.pdf', as_attachment=True)


@app.route('/zakazky/kalendar')
def zakazky_kalendar():
    zakazky = Zakazka.query.all()
    return render_template('zakazky/kalendar.html', zakazky=zakazky)
