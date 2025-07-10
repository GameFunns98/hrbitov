import io
from flask import render_template, redirect, url_for, flash, send_file, request
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
from datetime import date

@app.route('/')
def index():
    return redirect(url_for('hrbitovy_list'))


@app.route('/hrbitovy')
def hrbitovy_list():
    hrbitovy = Hrbitov.query.all()
    return render_template('hrbitovy/index.html', hrbitovy=hrbitovy)

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
        return redirect(url_for('hrbitovy_list'))
    return render_template('pridat_hrbitov.html', form=form)


@app.route('/hrbitov/<int:hrbitov_id>/edit', methods=['GET', 'POST'])
def edit_hrbitov(hrbitov_id):
    hrb = Hrbitov.query.get_or_404(hrbitov_id)
    form = HrbitovForm(obj=hrb)
    if form.validate_on_submit():
        form.populate_obj(hrb)
        db.session.commit()
        flash('Hřbitov upraven')
        return redirect(url_for('hrbitovy_list'))
    return render_template('pridat_hrbitov.html', form=form, edit=True)


@app.route('/hrbitov/<int:hrbitov_id>/delete', methods=['POST'])
def delete_hrbitov(hrbitov_id):
    hrb = Hrbitov.query.get_or_404(hrbitov_id)
    db.session.delete(hrb)
    db.session.commit()
    flash('Hřbitov smazán')
    return redirect(url_for('hrbitovy_list'))

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


@app.route('/hroby')
def hroby_list():
    hroby = Hrob.query.all()
    return render_template('hroby/index.html', hroby=hroby)


@app.route('/hrob/<int:hrob_id>/edit', methods=['GET', 'POST'])
def edit_hrob(hrob_id):
    hrob = Hrob.query.get_or_404(hrob_id)
    form = HrobForm(obj=hrob)
    if form.validate_on_submit():
        form.populate_obj(hrob)
        db.session.commit()
        flash('Hrob upraven')
        return redirect(url_for('hroby_list'))
    return render_template('pridat_hrob.html', form=form, edit=True)


@app.route('/hrob/<int:hrob_id>/delete', methods=['POST'])
def delete_hrob(hrob_id):
    hrob = Hrob.query.get_or_404(hrob_id)
    hrb_id = hrob.hrbitov_id
    db.session.delete(hrob)
    db.session.commit()
    flash('Hrob smazán')
    return redirect(url_for('hroby_list'))

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


@app.route('/zesnuli')
def zesnuli_list():
    zesnuli = Zesnuly.query.all()
    return render_template('zesnuli/index.html', zesnuli=zesnuli)


@app.route('/zesnuly/<int:zesnuly_id>/edit', methods=['GET', 'POST'])
def edit_zesnuly(zesnuly_id):
    zes = Zesnuly.query.get_or_404(zesnuly_id)
    form = ZesnulyForm(obj=zes)
    if form.validate_on_submit():
        form.populate_obj(zes)
        db.session.commit()
        flash('Záznam upraven')
        return redirect(url_for('zesnuli_list'))
    return render_template('pridat_zesnuly.html', form=form, edit=True)


@app.route('/zesnuly/<int:zesnuly_id>/delete', methods=['POST'])
def delete_zesnuly(zesnuly_id):
    zes = Zesnuly.query.get_or_404(zesnuly_id)
    db.session.delete(zes)
    db.session.commit()
    flash('Záznam smazán')
    return redirect(url_for('zesnuli_list'))

@app.route('/pridat_najemce', methods=['GET', 'POST'])
def pridat_najemce():
    form = NajemceForm()
    if form.validate_on_submit():
        n = Najemce(jmeno=form.jmeno.data, kontaktni_udaje=form.kontaktni_udaje.data)
        db.session.add(n)
        db.session.commit()
        flash('Nájemce přidán')
        return redirect(url_for('najemci_list'))
    return render_template('pridat_najemce.html', form=form)


@app.route('/najemci')
def najemci_list():
    najemci = Najemce.query.all()
    return render_template('najemci/index.html', najemci=najemci)


@app.route('/najemce/<int:najemce_id>/edit', methods=['GET', 'POST'])
def edit_najemce(najemce_id):
    naj = Najemce.query.get_or_404(najemce_id)
    form = NajemceForm(obj=naj)
    if form.validate_on_submit():
        form.populate_obj(naj)
        db.session.commit()
        flash('Nájemce upraven')
        return redirect(url_for('najemci_list'))
    return render_template('pridat_najemce.html', form=form, edit=True)


@app.route('/najemce/<int:najemce_id>/delete', methods=['POST'])
def delete_najemce(najemce_id):
    naj = Najemce.query.get_or_404(najemce_id)
    db.session.delete(naj)
    db.session.commit()
    flash('Nájemce smazán')
    return redirect(url_for('najemci_list'))

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
        return redirect(url_for('smlouvy_list'))
    return render_template('pridat_smlouvu.html', form=form)


@app.route('/smlouvy')
def smlouvy_list():
    smlouvy = Smlouva.query.all()
    return render_template('smlouvy/index.html', smlouvy=smlouvy)


@app.route('/smlouva/<int:smlouva_id>/edit', methods=['GET', 'POST'])
def edit_smlouva(smlouva_id):
    sml = Smlouva.query.get_or_404(smlouva_id)
    form = SmlouvaForm(obj=sml)
    if form.validate_on_submit():
        form.populate_obj(sml)
        db.session.commit()
        flash('Smlouva upravena')
        return redirect(url_for('smlouvy_list'))
    return render_template('pridat_smlouvu.html', form=form, edit=True)


@app.route('/smlouva/<int:smlouva_id>/delete', methods=['POST'])
def delete_smlouva(smlouva_id):
    sml = Smlouva.query.get_or_404(smlouva_id)
    db.session.delete(sml)
    db.session.commit()
    flash('Smlouva smazána')
    return redirect(url_for('smlouvy_list'))

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
    celkova_cena = (
        db.session.query(db.func.sum(VykazZakazky.cena_celkem))
        .filter_by(zakazka_id=zak.id)
        .scalar()
        or 0
    )

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
    return render_template(
        'zakazky/detail.html',
        zakazka=zak,
        koment_form=koment_form,
        vykaz_form=vykaz_form,
        celkova_cena=celkova_cena,
    )


@app.route('/zakazka/<int:zakazka_id>/uzavrit', methods=['POST'])
def uzavrit_zakazku(zakazka_id):
    zak = Zakazka.query.get_or_404(zakazka_id)
    zak.stav = 'uzavřená'
    if not zak.datum_dokonceni:
        zak.datum_dokonceni = date.today()
    db.session.commit()
    flash('Zakázka uzavřena')
    return redirect(url_for('zakazka_detail', zakazka_id=zak.id))



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
