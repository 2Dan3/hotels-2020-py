A small (beginner coding level) Python console app for Hotel reservation management as Administrator, Receptionist or Guest (programming basics).

Functionalities within the project (sr):
________________________________________
Realizovane funkcionalnosti u projektu
________________________________________

Opcije:
---------------------
1. Registracija
	- Kreiranje nove korisničke šifre sa ulogom "Gost"
2. Prijava na sistem
	- Unos korisničke šifre i lozinke, uz prepoznavanje uloge korisnika za kontrole u daljem radu
3. Izlazak iz aplikacije
_______________________________________________



Za korisničku ulogu "Administrator" :
-----------------------------------------------
1. Dodavanje novih hotela
	- Unos traženih podataka o hotelu
	- Ako uneti naziv već postoji u .txt, (logički) obrisani hotel može se povratiti u rad, biće ponovo vidljiv
2. Dodavanje novih recepcionera u hotele
	- Unos novih korisnika sa ulogom "Recepcioner"
3. Ažuriranje hotela:
	-Odabir hotela (koji nije logički obrisan)
	-Opcije unutar odabranog hotela:

	-I   Dodaj novu sobu
		-Ako uneti br. sobe već postoji u .txt, (logički) obrisana soba može se povratiti u rad, biće ponovo vidljiva
	-II  Obriši sobu
	-III Pregled svih soba
		-Tabelarni prikaz postojećih ('neobrisanih') soba odabranog hotela
	-IV  Izmena postojeće sobe
	-V   Izmena hotela
		-Izmena svih podataka odabranog hotela odjednom,mogućnost da se ne unesu određeni duži podaci koji bi se najređe menjali (u praktičnom korišćenju) 
	-x  korak nazad
4. Brisanje hotela

5. Pretraga korisnika sistema
	
6. Brisanje recepcionera
x. Odjava sa sistema
_______________________________________________


Za ulogu "Recepcioner" :
-----------------------------------------------
1. Pretraga soba
	-prema br.kreveta, broju, tipu, TV, klima, unos max. cene ili raspona cene, dostupnost sobe (od - do)
2. Pretraga rezervacija
	-prema šifri gosta koji boravi, statusu i datumima prijave, odjave i kreiranja rezervacije
	-recepcioner može da promeni status unetoj rezervaciji nakon pretrage tj. tabelarnog prikaza rezervacija
3. Kreiranje izveštaja
	-precizan unos datuma (od - do), prikaz uk. br. realizovanih rezervacija, izdatih soba, zarade, 
 prosečne ocene i tabele realizovanih rezervacija u zadatom periodu

x. Odjava sa sistema
_______________________________________________


Za ulogu "Gost":
-----------------------------------------------
1. Pregled hotela
	-tabelarni prikaz svih 'neobrisanih' hotela
2. Pretraga hotela
	-Prema nazivu, adresi, prosečnoj oceni (od - do)
	-Prikaz podataka svih hotela unutar unetih kriterijuma
	-Prikaz mini-legende (objašnjenje skraćenica)
	-Poruka koliko je hotela sistem pronašao

3. Najbolje ocenjeni hoteli
	-(Tabelarni) prikaz 5 najboljih hotela

4. Kreiraj rezervaciju
	-Unos ID hotela i broja sobe u njemu, početnog datuma i br. noćenja
	-Automatsko dodeljivanje trenutnog korisnika i vremena kreiranja u rezervaciju
	-Kontrola: da li uneti podaci postoje, odnosno da li je datum rezervacije zauzet za br. sobe u hotelu
	-Kontrola: ne može se uneti datum početka rezervacije pre današnjeg
	-Prikaz poruke o datumu odjave (dan izlaska iz sobe)
5. Pregled rezervacija
	-(Tabelarni) prikaz podataka o svim aktivnim rezervacijama trenutno prijavljenog gosta

6. Oceni hotel
	-Gost ocenjuje hotel u kom je boravio
	-Moguć unos ocene za svaku postojeću (u toku / završenu) rezervaciju tog gosta
	-Preračun i upis nove prosečne ocene za ID hotela iz (ocenjenih) rezervacija
x. Odjava sa sistema
_______________________________________________


*Napomene :
-----------------------------------------------
-Nije podržan unos slova srpske azbuke: ć,č,š,ž,đ ("UnicodeEncodeError: 'charmap' codec can't encode character")

-Pri registraciji će korisničko ime biti snimljeno u 'lowercase', i takvo se koristi za login

-Nakon 3 uzastopno neuspešnih login-a, aplikacija se zatvara uz poruku

-Logičko brisanje kod hotela i soba, trajno brisanje recepcionera

-Unos hotela, sobe ili rezervacije: automatska dodela ID broja

-Izmena hotela, sobe ili rezervacije(status): Kontrole da li postoji taj ID (a da nije obrisan)

-Brisanje hotela i soba: Kontrole i odgovarajuće poruke da li uopšte (ne)postoje ili su postojale ali su (logički) obrisane

-Pretraga: Traži se unos svih kriterijuma, jednog za drugim,mogućnost kod naziva, uloga, adresa,(prez)imena (svega sem brojeva) 
 da se unese samo prvih par slova naziva iz .txt-a ili da se NE unese kriterijum za pretragu (tabelarni prikaz bez tih filtera)
_______________________________________________
*Primer podaci za login:
-----------------------------------------------
		Korisničko  Lozinka

Admin: 		dschonberg    31

Recepcioner: 	pzivkovic     22     (Hotel:Jelak, ID:000006)

Gost:		dtusic	      11
_______________________________________________
