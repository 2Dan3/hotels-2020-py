import datetime

def str2Date(strdate, date_format):
    lista = strdate.strip().split("-")
    
    if date_format == 'ymd':
        year = int(lista[0])
        month = int(lista[1])
        day = int(lista[2])
    elif date_format == 'dmy':
        day = int(lista[0])
        month = int(lista[1])
        year = int(lista[2])
    
    Date = datetime.date(year, month, day)
    return Date


def povecaj_id(key_id):
    target = open("last_ID.txt", "r")
    id_list = []

    for row in target.readlines():
            last_id = {}
            frag = row.strip().split(": ")
            last_id['name'] = frag[0]
            last_id['last_id'] = frag[1]
            id_list.append(last_id)
            
    for last_id in id_list:
        if last_id['name'] == key_id:
            last_added_id = (str(int(last_id['last_id']) + 1)).zfill(6)
            last_id['last_id'] = last_added_id
            break
    target.close()

    target = open("last_ID.txt", "w")
    for new_id in id_list:
        target.write(new_id['name'] + ": " + new_id['last_id'] + "\n")
    target.close()

    return last_added_id



def sign_in():

    user_list = ucitaj_entity("all_users.txt",'user')

    login_tries = 0
    user_exists = False

    while login_tries < 3:
        print('\nPrijavite se na sistem >> \n')
        u_username = input('Korisničko ime: ')
        u_password = input('Lozinka: ')
        login_tries += 1
        for user1 in user_list:
            if user1['username'] == u_username and user1['password'] == u_password:
                
                current_user = user1['username']
                user_exists = True
                break
            
        if user_exists :
            return current_user  
        else:
            print('\nPogrešno uneta šifra ili lozinka !')
    return None

# HOTELI

def add_hotel():
    new_hotel = {}
    vec_postoji = False

    new_hotel['id'] = povecaj_id('last_hotel')
    new_hotel['name'] = input('Naziv hotela: ').capitalize()
    new_hotel['address'] = input('Adresa hotela: ').capitalize()
    new_hotel['pool'] = input('Bazen postoji? (d/n): ').lower()
    new_hotel['restaurant'] = input('Restoran postoji? (d/n): ').lower()
    new_hotel['deleted'] = ''
    new_hotel['avg'] = 0.0

    hotel_list = ucitaj_entity('all_hotels.txt','hotel')

    for hotel in hotel_list:
        if hotel['id'] == new_hotel['id']:
            if hotel['deleted'] == 'deleted':
                if (input('Ovaj hotel je bio obrisan.\nŽelite li da ponovo dodate hotel na spisak (d/n)? ')).lower().strip() == 'd':
                    hotel['deleted'] = ''
                    save_hotels(hotel_list)
                    vec_postoji = True
                    break
            else:
                vec_postoji = True
                print('\n-----Postoji hotel sa tim ID -----')
                break
    if not vec_postoji:
        hotel_list.append(new_hotel)
        save_hotels(hotel_list)
        print('\n-----Hotel je uspešno dodat-----')



def hotel2Str(new_hotel):
    s = new_hotel['id'] + "|" + new_hotel['name'] + "|" + new_hotel['address'] + "|" + new_hotel['pool'] + "|" + new_hotel['restaurant'] + "|" + new_hotel['deleted'] + "|" + str(new_hotel['avg'])
    return s

def str2Hotel(row):
    new_hotel = {}
    frag = row.strip().split("|")
    new_hotel['id'] = frag[0]
    new_hotel['name'] = frag[1]
    new_hotel['address'] = frag[2]
    new_hotel['pool'] = frag[3]
    new_hotel['restaurant'] = frag[4]
    new_hotel['deleted'] = frag[5]
    new_hotel['avg'] = frag[6]
    return new_hotel


def save_hotels(hotel_list):

    target = open("all_hotels.txt", "w")
    for new_hotel in hotel_list:
        target.write(hotel2Str(new_hotel) + "\n")
    target.close()


def show_all_hotels():
    hotel_list = ucitaj_entity('all_hotels.txt','hotel')
    print("ID     Naziv                     Adresa                         Bazen       Restoran    Ocena")
    print("---------------------------------------------------------------------------------------------")
    for new_hotel in hotel_list:
        if new_hotel['deleted'] != 'deleted':
            print(str(new_hotel['id']).ljust(7) 
            + new_hotel['name'][:25].ljust(26) + new_hotel['address'][:30].ljust(31) + new_hotel['pool'].ljust(12) + new_hotel['restaurant'].ljust(12)
            + str(new_hotel['avg']))
    print("\n")

# Ucitavanje .txt -> list

def ucitaj_entity(File_name, str2):

    entity_list = []
    
    target = open(File_name, "r")
    for row in target.readlines():

        if str2 == 'hotel':
            entity_list.append(str2Hotel(row))
        elif str2 == 'room':
            entity_list.append(str2Room(row))
        elif str2 == 'user':
            entity_list.append(str2User(row))
        elif str2 == 'reservation':
            entity_list.append(str2Reservation(row))
        elif str2 == 'rating':
            entity_list.append(str2Rate(row))
                      
    target.close()

    return entity_list

# add_rate()/ rating_averages() -> Dodela ocena za postojece rezervacije u hotelu, odnosno novih prosecnih ocena hotelu

def add_rate(current_user):
    reservation_list = ucitaj_entity("all_reservations.txt", 'reservation')
    hotel_list = ucitaj_entity("all_hotels.txt", 'hotel')
    counter = 0
    hotelcic = input('ID hotela >> ')
    hotel = check_existing_hotel(hotelcic)
    if hotel == False:
        print('\nNe postoji hotel sa unetim ID.\n')
    else:
        for reservation in reservation_list:
            if hotelcic == reservation['id_hotel'] and current_user == reservation['id_guest'] and reservation['rating'] == '':
                
                new_rating = input('\nMolimo da Vaše iskustvo sa upisanim hotelom ocenite [1-5]: ').strip()
                reservation['rating'] = new_rating
                reservation['date_rated'] = str(datetime.date.today().strftime("%G-%m-%d"))

                save_reservations(reservation_list)
                print('\n---Hvala što ste ocenili hotel---\n')
                counter = 1

                # upis nove prosecne ocene u all_hotels.txt
                r8 = rating_averages(reservation['id_hotel'])

                for h in hotel_list:
                    if h['id'] == reservation['id_hotel']:
                        h['avg'] = r8
                        save_hotels(hotel_list)
                        break
                break

        if counter == 0:
            print('\nMoguće je oceniti samo neocenjene hotele u kojima ste boravili.\n')
  

def rate2Str(new_rate):
    s = new_rate['id_hotela'] + "|" + new_rate['ocena'] + "|" + new_rate['datum']
    return s

def str2Rate(row):
    new_rate = {}
    frag = row.strip().split("|")
    new_rate['id_hotela'] = frag[0]
    new_rate['ocena'] = frag[1]
    new_rate['datum'] = frag[2]
    return new_rate

def save_rate():
    rating_list = ucitaj_entity("all_rates.txt", 'rate')
    target = open("all_rates.txt", "w")
    for new_rate in rating_list:
        target.write(rate2Str(new_rate) + "\n")
    target.close()
       
def rating_averages(hotelcic):
    reservation_list = ucitaj_entity("all_reservations.txt", 'reservation')
    br_ocena = 0
    suma_ocena = 0
    prosek = 0

    for reservation in reservation_list:
        if reservation['id_hotel'] == hotelcic and reservation['rating'] !='':
            br_ocena += 1
            suma_ocena += float(reservation['rating'])
            

    if br_ocena == 0:
        prosek = 0
    else:
        prosek=suma_ocena/br_ocena
    return prosek

def report(recep_hotel):

    reservation_list = ucitaj_entity("all_reservations.txt", 'reservation')
    datum_od = input('Od datuma (dd-mm-yyyy): ')
    datum_do = input('Do datuma (dd-mm-yyyy): ')
   
    od_datuma = str2Date(datum_od,'dmy')
    do_datuma = str2Date(datum_do,'dmy')

    # racunaju i prikazuju uspesnost hotela u zadatom periodu:

    res_finished(recep_hotel, od_datuma, do_datuma, reservation_list)
    rooms_rented(recep_hotel, od_datuma, do_datuma, reservation_list)
    calc_earned(recep_hotel, od_datuma, do_datuma, reservation_list)
    calc_avg(recep_hotel, od_datuma, do_datuma, reservation_list)


def delete_hotel(ID_hotela_za_brisanje):
    hotel_list = ucitaj_entity('all_hotels.txt','hotel')
    hotel_postoji = False
    for hotel in hotel_list:
        if hotel['id'] == ID_hotela_za_brisanje:
            if hotel['deleted'] != 'deleted':
                hotel['deleted'] = 'deleted'
                save_hotels(hotel_list)
                hotel_postoji = True
                print('-----Hotel je obrisan-----')
            else:
                print('\nHotel sa unetim ID je postojao, ali je obrisan !')
                hotel_postoji = True
    if not hotel_postoji:
        print('\nNe postoji hotel sa unetim ID !')


def check_existing_hotel(hotel_id):
    hotel_list = ucitaj_entity('all_hotels.txt','hotel')
    hotel_postoji = False
    for hotel in hotel_list:
        if hotel['id'] == hotel_id:
            if hotel['deleted'] == '':
                hotel_postoji = True
                break
    return hotel_postoji

def find_hotel():
    hotel_list = ucitaj_entity("all_hotels.txt", 'hotel')
    brojac = 0

    print('\n\n** Kriterijum za pretragu moguće je ostaviti (celokupno) nepopunjenim **')
    print('** Kod kriterijuma sa nazivima (adresama, imenima...), moguće je uneti samo početnih par slova zvaničnog naziva **')
    hotel_name = input('\nNaziv hotela: ').strip().capitalize()
    hotel_address = input('Adresa hotela: ').strip().capitalize()
    hotel_stars = input('Prosečna ocena hotela >  (od - do): ').strip()
    if hotel_stars != '':
        if "-" in hotel_stars:
            hotel_stars = hotel_stars.split("-")

    print('\nNaziv hotela        Adresa hotela                   Bazen   Restoran   Ocena')
    print('------------------------------------------------------------------------------')
    for hotel in hotel_list:

            if (hotel_name == '' or (hotel_name in hotel['name'])) and (hotel_address == '' or (hotel_address in hotel['address'])) and (hotel_stars == '' or (float(hotel_stars[0].strip()) <= float(hotel['avg']) and float(hotel_stars[1].strip()) >= float(hotel['avg']))) and (hotel['deleted'] != 'deleted'):
                print(hotel['name'].ljust(20) + hotel['address'].ljust(32) + hotel['pool'].ljust(8) + hotel['restaurant'].ljust(11) + hotel['avg'])
                brojac += 1
    if brojac !=0:
        print("\n*----------------------*\n'd'= postoji")
        print("'n'= ne postoji\n*----------------------*\n")
        if (brojac >= 10 and brojac <= 20) or (brojac % 10 > 4):
            print('Pronađeno je', brojac, 'hotela.\n')
        else:
            if (brojac % 10) == 1:
                print('Pronađen je', brojac, 'hotel.\n')
            elif (brojac % 10) > 1 and (brojac % 10) < 5:
                print('Pronađena su', brojac, 'hotela.\n')

    else:
        print('Nijedan hotel ne odgovara unetim kriterijumima.\n')

def show_best_hotels():
    hotel_list = ucitaj_entity('all_hotels.txt','hotel')
    def func(e):
        return e['avg']
    hotel_list.sort(reverse=True, key=func)
    i = 0
    print('Naziv                   Prosečna ocena\n------------------------------------')
    for hotel in hotel_list:
        if hotel['deleted'] != 'deleted':
            print(hotel['name'].ljust(23), hotel['avg'])
            i+=1
            if i==5:
                print('\n')
                break

# SOBE

def add_room(hotel_choice):
    room_list = ucitaj_entity("rooms.txt", 'room')
    new_room = {}
    vec_postoji = False

    new_room['id'] = povecaj_id('last_room')
    room_num = input('Broj sobe: ')
    new_room['num'] = room_num

    new_room['beds'] = input('Broj kreveta u sobi: ')
    new_room['type'] = input('Apartman ili 1 soba (a/s)? ').lower()
    new_room['ac'] = input('Klima postoji (d/n)? ').lower()
    new_room['tv'] = input('TV postoji (d/n)? ').lower()
    new_room['price'] = input('Cena noćenja: ')
    new_room['hotel_id'] = hotel_choice
    new_room['deleted'] = ''

    for room in room_list:
        if room['hotel_id'] == new_room['hotel_id'] and room['num'] == new_room['num']:
            # aktiviranje obrisane sobe
            if room['deleted'] == 'deleted':
                if (input('Ova soba je bila obrisana iz svog hotela.\nŽelite li da ponovo dodate sobu na spisak (d/n)? ')).lower().strip() == 'd':
                    room['deleted'] = ''
                    save_rooms(room_list)
                    vec_postoji = True
                    break
            else:
                print('\n-----Uneti broj sobe već postoji u odabranom hotelu-----')        
                vec_postoji = True
                break

    if not vec_postoji:
        room_list.append(new_room)
        save_rooms(room_list)
        print('\n-----Soba je uspešno dodata-----')

def room2Str(new_room):
    st = new_room['id'] + "|" + new_room['num'] + "|" + new_room['beds'] + "|" + new_room['type'] + "|" + new_room['ac'] + "|" + new_room['tv'] + "|" + new_room['price'] + "|" + new_room['hotel_id'] + "|" + new_room['deleted']
    return st

def str2Room(row):
    new_room = {}
    frag = row.strip().split("|")
    new_room['id'] = frag[0]
    new_room['num'] = frag[1]
    new_room['beds'] = frag[2]
    new_room['type'] = frag[3]
    new_room['ac'] = frag[4]
    new_room['tv'] = frag[5]
    new_room['price'] = frag[6]
    new_room['hotel_id'] = frag[7]
    new_room['deleted'] = frag[8]

    return new_room


def save_rooms(room_list):

    target = open("rooms.txt", "w")
    for new_room in room_list:
        target.write(room2Str(new_room) + "\n")
    target.close()

def show_all_rooms(hotel_choice):
    
    print('ID     Broj    Br. kreveta     Tip    Klima    TV    Cena noćenja')
    print('-------------------------------------------------------------------')
    room_list = ucitaj_entity("rooms.txt", 'room')
    for new_room in room_list:
        if new_room['hotel_id'] == hotel_choice and new_room['deleted'] != 'deleted':

            print((new_room['id'].ljust(7) + new_room['num'].ljust(8) + new_room['beds'].ljust(16) + new_room['type'].ljust(7) 
            + new_room['ac'].ljust(9) + new_room['tv'].ljust(6) + new_room['price']))
    print('\n')


def delete_room(ID_sobe_za_brisanje):
    room_list = ucitaj_entity("rooms.txt", 'room')
    soba_postoji = False
    for room in room_list:
        if room['id'] == ID_sobe_za_brisanje:
            room['deleted'] = 'deleted'
            save_rooms(room_list)
            soba_postoji = True
            print('\n-----Soba je obrisana-----')
            break
    if not soba_postoji:
        print('\nNe postoji soba sa unetim ID !')


def check_existing_room(hotel_id, room_num):
    room_list = ucitaj_entity("rooms.txt", 'room')
    soba_postoji = False
    for room in room_list:
        if room['num'] == room_num and room['hotel_id'] == hotel_id:
            if room['deleted'] == '':
                soba_postoji = True
                break
    return soba_postoji

def find_room(recep_hotel):
    room_list = ucitaj_entity("rooms.txt", 'room')
    reservation_list = ucitaj_entity("all_reservations.txt", 'reservation')
    brojac = 0

    print('\n\n** Kriterijum za pretragu moguće je ostaviti (celokupno) nepopunjenim **')
    room_num = (input('\nBroj sobe: ')).strip()
    room_bed_num = (input('Broj kreveta: ')).strip()
    room_type = (input('Apartman ili soba >  (s / a): ')).strip().lower()
    room_ac = (input('Sa klimom >  (d / n): ')).strip().lower()
    room_tv = (input('Sa TV-om >  (d / n): ')).strip().lower()
    room_pr = (input("Unesite maksimalnu cenu ili raspon cene (od - do): ")).strip()
    room_availability = (input('Period dostupnosti sobe >  (dd-mm-yyyy dd-mm-yyyy): ')).strip()

    if room_pr != '':
        if "-" in room_pr:
            room_pr = room_pr.split("-")

    if room_availability != '':
        l = room_availability.split()
        input1 = l[0].strip()
        input2 = l[1].strip()
        date1 = str2Date(input1,'dmy')
        date2 = str2Date(input2,'dmy')
        free_rooms = []
        #
        def func(e):
            return e['room_num']
        reservation_list.sort(key=func)
        for room in room_list:
            if room['hotel_id'] == recep_hotel and room['deleted']!='deleted':
                reservation_exists = False
                free = True


                for r in reservation_list:
                    if r['id_hotel'] == recep_hotel and r['room_num'] == room['num'] and free and r['status'] != 'z':
                        reservation_exists = True

                        date_in = str2Date(r['date_in'],'ymd')
                        date_out = str2Date(r['date_out'],'ymd')
                        if (date1 >= date_out) or (date2 < date_in):
                            continue
                        else:
                            free = False

                if (reservation_exists and free) or (not reservation_exists):
                    free_rooms.append(room['num'])
                
    print('\n\nBroj sobe   Broj kreveta   Tip    Klima     TV   Cena noćenja')
    print('--------------------------------------------------------------')

    for room in room_list:
        if room['hotel_id'] == recep_hotel:
            if (room_num == '' or room['num'] == room_num) and (room_bed_num == '' or room['beds'] == room_bed_num) and (room_type == '' or room['type'] == room_type) and (room_ac == '' or room['ac'] == room_ac) and (room_tv == '' or room['tv'] == room_tv) and (room_pr == '' or (room['price'] <= room_pr[1].strip() and room['price'] >= room_pr[0].strip())) and (room_availability =='' or (room['num'] in free_rooms)) and (room['deleted'] != 'deleted'):
                print(room['num'].ljust(12) + room['beds'].ljust(16) + room['type'].ljust(8) + room['ac'].ljust(8) + room['tv'].ljust(5) + room['price'])
                brojac += 1
    if brojac !=0:
        print("\n*----------------------*\n'd'= postoji")
        print("'n'= ne postoji")
        print("'a'= apartman")
        print("'s'= jednosoban smeštaj\n*----------------------*\n")
        if (brojac >= 10 and brojac <= 20) or (brojac % 10 > 4):
            print('Pronađeno je', brojac, 'soba.\n')
        else:
            if (brojac % 10) == 1:
                print('Pronađena je', brojac, 'soba.\n')
            elif (brojac % 10) > 1 and (brojac % 10) < 5:
                print('Pronađene su', brojac, 'sobe.\n')
            
    else:
        print('Nijedna soba ne odgovara unetim kriterijumima.\n')



# UPDATE MENIji (izmena podataka unutar hotela / soba)

def room_data_change(room_choice, hotel_choice):
    room_list = ucitaj_entity("rooms.txt", 'room')

    beds = input('Novi broj kreveta u sobi: ')
    r_type = input('Apartman ili 1 soba (a/s)?: ').lower()
    ac = input('Klima postoji (d/n)?: ').lower()
    tv = input('TV postoji (d/n)?: ').lower()
    r_price = input('Nova cena sobe: ')

    for room in room_list:
        if room['hotel_id'] == hotel_choice and room['num'] == room_choice:
            room['beds'] = beds
            room['type'] = r_type
            room['ac'] = ac
            room['tv'] = tv
            room['price'] = r_price
            
    save_rooms(room_list)

def hotel_data_change(hotel_choice):
    hotel_list = ucitaj_entity('all_hotels.txt','hotel')
    hotel_pool = input('Bazen postoji (d/n)?: ').lower()
    hotel_restaurant = input('Restoran postoji (d/n)?: ').lower()
    address_hotel = input('Izmenite adresu ili ostavite prazno (zadržati staru): ').strip()
    name_hotel = input('Izmenite naziv ili ostavite prazno (zadržati stari): ').strip()
    for hotel in hotel_list:
        if hotel['id'] == hotel_choice:

            hotel['pool'] = hotel_pool
            hotel['restaurant'] = hotel_restaurant
            if address_hotel != '':
                hotel['address'] = address_hotel.capitalize()
            if name_hotel != '':
                hotel['name'] = name_hotel.capitalize()

            save_hotels(hotel_list)
            break

def hotel_update(hotel_choice):
    
    var_command = ''
    while var_command.lower() != 'x':
        print('\n1) Dodaj novu sobu')
        print('2) Obriši sobu')
        print('3) Pregled svih soba')
        print('4) Izmena postojeće sobe')
        print('5) Izmena hotela')
        print('x) Izlaz')

        var_command = input('Unesite komandu >> ')

        if var_command == '1':
            
            print('\nDodavanje nove sobe >> ')
            add_room(hotel_choice)
            
        elif var_command == '2':
            show_all_rooms(hotel_choice)
            print('\nBrisanje sobe >> ')
            ID_sobe_za_brisanje = input('\nID sobe za brisanje: ')
            
            delete_room(ID_sobe_za_brisanje)

        elif var_command == '3':
            
            print('\nPregled svih soba izabranog hotela >> ')
            show_all_rooms(hotel_choice)

        elif var_command == '4':
            print('\nIzmena postojeće sobe >> ')
            room_choice = input('\nAžuriraj sobu broj: ')
            room_checked = check_existing_room(hotel_choice, room_choice)
            if not room_checked:
                print('\nNe postoji takva soba u izabranom hotelu !')
            else:
                room_data_change(room_choice, hotel_choice)
                print('\n-----Podaci su uspešno izmenjeni-----')

        elif var_command == '5':
            print('\nIzmena podataka o hotelu >> ')
            hotel_data_change(hotel_choice)
            print('\n-----Podaci su uspešno izmenjeni-----')

        elif var_command.lower() == 'x':
            print('\nAžuriranje hotela - završeno.\n')
        
        else:
            print('\nUneta komanda ne postoji!')




# RECEPCIONERI

def add_user(new_role):
    new_user = {}
    user_list = ucitaj_entity('all_users.txt','user')
    vec_postoji = False

    if new_role == 'recepcioner' :
        hotel_id = input('ID hotela: ')
        hotel_postoji = check_existing_hotel(hotel_id)
        if hotel_postoji:
            new_user['id'] = hotel_id
        else:
            print('\nNe postoji hotel sa unetim ID !')
            return 'error'
    else:
        new_user['id'] = ''


    new_user['name'] = input('Ime : ').capitalize().strip()
    new_user['lastname'] = input('Prezime : ').capitalize().strip()
    new_user['phone'] = input('Br. telefona: ').strip()
    new_user['email'] = input('Email adresa: ').strip()
    new_user['username'] = input('Korisničko ime: ').lower().strip()
    new_user['password'] = input('Lozinka: ')
    new_user['role'] = new_role
           
    for user in user_list:
        if user['username'] == new_user['username']:
            print('\n-----Postoji korisnik sa tim korisničkim imenom -----')
            vec_postoji = True
            break

    if not vec_postoji:
            user_list.append(new_user)
            save_user(user_list)
            print('\n-----Korisnik je uspešno dodat-----')

def user2Str(new_user):
    s = new_user['id'] + "|" + new_user['name'] + "|" + new_user['lastname'] + "|" + new_user['phone'] + "|" + new_user['email'] + "|" + new_user['username'] + "|" + new_user['password'] + "|" + new_user['role']
    return s

def str2User(row):
    new_user = {}
    frag = row.strip().split("|")
    new_user['id'] = frag[0]
    new_user['name'] = frag[1]
    new_user['lastname'] = frag[2]
    new_user['phone'] = frag[3]
    new_user['email'] = frag[4]
    new_user['username'] = frag[5]
    new_user['password'] = frag[6]
    new_user['role'] = frag[7]
    return new_user


def save_user(user_list):
    target = open("all_users.txt", "w")
    for new_user in user_list:
        target.write(user2Str(new_user) + "\n")
    target.close()

def show_all_receps(File_name, str2):
    print("ID hotela   Ime        Prezime         Telefon     Email                Šifra / Lozinka            Uloga")
    print("--------------------------------------------------------------------------------------------------------------")
    user_list = ucitaj_entity('all_users.txt','user')

    for new_recep in user_list:
        if new_recep['role'] == 'recepcioner' :
            print(str(new_recep['id']).ljust(12) 
            + new_recep['name'][:10].ljust(11) + new_recep['lastname'][:15].ljust(16)
            + new_recep['phone'][:11].ljust(12) + new_recep['email'][:20].ljust(21)
            + new_recep['username'][:15].ljust(11) + new_recep['password'].ljust(16)
            + new_recep['role'])
    print("\n")

def delete_recep(recepcioner_za_brisanje):
    user_list = ucitaj_entity('all_users.txt','user')
    recep_postoji = False

    for user in user_list:
        if user['role'] == 'recepcioner':
            
            if user['username'] == recepcioner_za_brisanje:
                user_list.remove(user)
                save_user(user_list)
                print('\n-----Recepcioner je obrisan-----')
                recep_postoji = True
                break
    if not recep_postoji:
        print('\nNe postoji takav recepcioner !')


def find_recep():
    user_list = ucitaj_entity("all_users.txt", 'user')
    
    print('\n\n** Kriterijum za pretragu moguće je ostaviti (celokupno) nepopunjenim **')
    print('** Kod kriterijuma sa nazivima (adresama, imenima...), moguće je uneti samo početnih par slova zvaničnog naziva **')
    recep_ime = input('\nIme: ').strip().capitalize()
    recep_prezime = input('Prezime: ').strip().capitalize()
    recep_sifra = input('Korisničko ime: ').strip().lower()
    recep_email = input('Email: ').strip()
    recep_uloga = input('Uloga: ').strip().lower()
    rec_hotel = input('Unesite ceo ID hotela: ').strip()

    print('\nIme         Prezime         Korisničko ime    Email                Uloga        Hotel')
    print('----------------------------------------------------------------------------------------')
    for user in user_list:
        if (recep_ime == '' or (recep_ime in user['name'])) and (recep_prezime == '' or (recep_prezime in user['lastname'])) and (recep_sifra == '' or (recep_sifra in user['username'])) and (recep_email == '' or (recep_email in user['email'])) and (recep_uloga == '' or (recep_uloga in user['role'])) and (rec_hotel == '' or user['id'] == rec_hotel):
            print(user['name'].ljust(12) + user['lastname'].ljust(16) + user['username'].ljust(18) + user['email'].ljust(21) + user['role'].ljust(13) + user['id'])
         


# REZERVACIJE

def add_reservation(current_user):
    new_reservation = {}
     
    hotel_id = input('ID hotela: ')

    hotel_postoji = check_existing_hotel(hotel_id)
    if not hotel_postoji:
        print('\nNe postoji hotel sa unetim ID !\n')
    else:
        new_reservation['id_hotel'] = hotel_id
        room_num = input('Broj sobe: ')
        soba_postoji = check_existing_room(hotel_id, room_num)
        if not soba_postoji:
            print('\nNe postoji soba sa unetim brojem !\n')
        else:
            new_reservation['room_num'] = room_num    
            new_reservation['creation_datetime'] = str(datetime.datetime.now())

            new_reservation['id_guest'] = current_user

            # Unos perioda rezervacije:
            date_now = datetime.date.today()
            while True:
                date_in = input('\nUnesite početni datum (dd-mm-yyyy) >> ')        
                date_in = str2Date(date_in,'dmy')


                if (date_in < date_now):
                    print('\nNe možete uneti datum pre današnjeg !')
                else:
                    break
                
            br_nocenja = int(input('Unesite br. noćenja >> '))

            br_noci = datetime.timedelta(days = br_nocenja)
            date_out = date_in + br_noci
        
            # KONTROLA
            room_list = ucitaj_entity("rooms.txt", 'room')   
            reservation_list = ucitaj_entity("all_reservations.txt", 'reservation')

            date_in_counter = date_in
            list_of_wanted_dates = []
            list_of_taken_dates = []
            while(date_in_counter < date_out):
                list_of_wanted_dates.append(date_in_counter)
                date_in_counter += datetime.timedelta(days=1)
            
            for room in room_list:
                if room['hotel_id'] == hotel_id and room['num'] == room_num:
                    for date in reservation_list:
                        if date['room_num'] == room_num:
                        
                            date_start = str2Date(date['date_in'],'ymd')
                            date_end = str2Date(date['date_out'],'ymd')

                            while date_start < date_end:
                                list_of_taken_dates.append(date_start)
                                date_start += datetime.timedelta(days=1)

                    for new_date in list_of_wanted_dates:
                        if new_date in list_of_taken_dates:
                            print('\n-----Datum Vaše rezervacije poklopio se sa datumom već postojeće rezervacije !-----\n')


            print('\nDatum odjave:', date_out.strftime("%d-%m-%G"))

            new_reservation['date_in'] = str(date_in)
            new_reservation['night_num'] = str(br_nocenja)
            new_reservation['date_out'] = str(date_out.strftime("%G-%m-%d"))
            new_reservation['status'] = 'n'
            new_reservation['id_reservation'] = povecaj_id('last_reservation')
            new_reservation['rating'] = ''
            new_reservation['date_rated'] = ''

            reservation_list.append(new_reservation)
            save_reservations(reservation_list)
            print('\n-----Vaša rezervacija je uspešno kreirana-----\n')


def reservation2Str(new_reservation):
    st = new_reservation['id_hotel'] + "|" + new_reservation['creation_datetime'] + "|" + new_reservation['room_num'] + "|" + new_reservation['id_guest'] + "|" + new_reservation['date_in'] + "|" + new_reservation['night_num'] + "|" + new_reservation['date_out'] + "|" + new_reservation['status'] + "|" + new_reservation['id_reservation'] +"|"+ new_reservation['rating'] +"|"+ new_reservation['date_rated']
    return st

def str2Reservation(row):
    new_reservation = {}
    frag = row.strip().split("|")
    new_reservation['id_hotel'] = frag[0]
    new_reservation['creation_datetime'] = frag[1]
    new_reservation['room_num'] = frag[2]
    new_reservation['id_guest'] = frag[3]
    new_reservation['date_in'] = frag[4]
    new_reservation['night_num'] = frag[5]
    new_reservation['date_out'] = frag[6]
    new_reservation['status'] = frag[7]
    new_reservation['id_reservation'] = frag[8]
    new_reservation['rating'] = frag[9]
    new_reservation['date_rated'] = frag[10]

    return new_reservation


def save_reservations(reservation_list):
    
    target = open("all_reservations.txt", "w")
    for new_reservation in reservation_list:
        target.write(reservation2Str(new_reservation) + "\n")
    target.close()

def show_all_reservations(File_name, str2, current_user):
    
    reservation_list = ucitaj_entity(File_name, str2)
    hotel_list = ucitaj_entity('all_hotels.txt','hotel')

    print('ID hotela   Hotel         Vreme rezervisanja           Br.sobe            Period rezervacije')
    print('---------------------------------------------------------------------------------------------------')
    

    for new_reservation in reservation_list:
        if new_reservation['id_guest'] == current_user:
            for h in hotel_list:
                if new_reservation['id_hotel'] == h['id']:
                    print(new_reservation['id_hotel'].ljust(12) + h['name'].ljust(14) + new_reservation['creation_datetime'].ljust(31) + new_reservation['room_num'].ljust(12) + new_reservation['date_in'].ljust(13) + '-   ' + new_reservation['date_out'])
    print('\n')

def find_reservation(recep_hotel):
    reservation_list = ucitaj_entity("all_reservations.txt", 'reservation')
    brojac = 0

    print('\n\n** Kriterijum za pretragu moguće je ostaviti (celokupno) nepopunjenim **')
    res_creation = input('\nDatum kreiranja rezervacije >  (dd-mm-yyyy): ').strip()
    res_in = input('Datum prijave >  (dd-mm-yyyy): ').strip()
    res_out = input('Datum odjave >  (dd-mm-yyyy): ').strip()
    res_guest = input('Gost: ').strip()
    res_status = input('Status rezervacije  (nije otpočeta/ u toku/ završena) >  (n/ t/ z): ').strip()

    if res_creation != '':
        res_creation = str2Date(res_creation, 'dmy')
    if res_in != '':
        res_in = str2Date(res_in, 'dmy')
    if res_out != '':
        res_out = str2Date(res_out, 'dmy')

    print('\nID rezervacije  Datum i vreme kreiranja        Br.sobe         Period rezervacije        Status   Gost       ')
    print('---------------------------------------------------------------------------------------------------------------')
    for r in reservation_list:
        date_in = str2Date(r['date_in'], 'ymd')
        date_out = str2Date(r['date_out'], 'ymd')
        date_creation = str2Date(r['creation_datetime'].split()[0], 'ymd')

        if (r['id_hotel'] == recep_hotel) and (res_creation == '' or (res_creation == date_creation)) and (res_in == '' or res_in == date_in) and (res_out == '' or res_out == date_out) and (res_guest == '' or (res_guest in r['id_guest'])) and (res_status == '' or res_status == r['status']):
            print(r['id_reservation'].ljust(16) + r['creation_datetime'].ljust(31) + r['room_num'].ljust(14) + r['date_in'].ljust(8) +'  -  '+ r['date_out'].ljust(16) + r['status'].ljust(6) + r['id_guest'])
            brojac += 1
    if brojac !=0:
        print("\n*----------------------*\n'z'= završena")
        print("'t'= u toku\n'n'= nije započeta\n*----------------------*\n")
        if (brojac >= 10 and brojac <= 20) or (brojac % 10 > 4):
            print('Pronađeno je', brojac, 'rezervacija.\n')
        else:    
            if (brojac % 10) == 1:
                print('Pronađena je', brojac, 'rezervacija.\n')
            elif (brojac % 10) > 1 and (brojac % 10) < 5:
                print('Pronađene su', brojac, 'rezervacije.\n')
        
        if input('Želite li da izmenite status rezervacije?[Da/ Ne] >  Uneti (d/ Enter): ') == 'd':
            res_id = input('Unesite ID rezervacije za izmenu: ')
            res_found = False
            for r in reservation_list:
                if res_id == r['id_reservation'] and r['status'] != 'z':
                    
                    res_found = True
                    print('Trenutni status rezervacije ',r['id_reservation'],'je:  "', r['status'],'".\nIzmeniti status? (Da/ Ne) >')
                    
                    if input('>  *Uneti [d/ Enter]: ') == 'd':
                        if r['status'] == 'n':
                            r['status'] = 't'
                            save_reservations(reservation_list)
                            print('Novi status rezervacije ',r['id_reservation'],'je: "u toku".\n')                            
                            break
                        elif r['status'] == 't':
                            r['status'] = 'z'
                            save_reservations(reservation_list)
                            print('Novi status rezervacije ',r['id_reservation'],'je: "završena".\n')
                            break

                elif res_id == r['id_reservation'] and r['status'] == 'z':
                    res_found = True
                    print('\nIzmena nije moguća! Rezervacija ',r['id_reservation'],' je već "završena".\n')
                
            if res_found == False:
                print('\nNe postoji rezervacija sa tim ID.\n')
                
    else:
        print('Nijedna rezervacija ne odgovara unetim kriterijumima.\n')

def find_employee_hotel(current_user):
    user_list = ucitaj_entity('all_users.txt','user')
    
    for user in user_list:
        if user['username'] == current_user:
            
            recep_hotel = user['id']
            return recep_hotel

def find_current_role(current_user):
    user_list = ucitaj_entity('all_users.txt','user')
    for user in user_list:
        if user['username'] == current_user:
            
            user_role = user['role']
            return user_role


def rooms_rented(recep_hotel, od_datuma, do_datuma, reservation_list):

    rooms_rented_nums = []

    for res in reservation_list:
        date_in = str2Date(res['date_in'], 'ymd')
        date_out = str2Date(res['date_out'], 'ymd')
        
        if (date_out <= od_datuma or date_in > do_datuma):
            continue
        else:
            if recep_hotel == res['id_hotel']:
                # ukupno izdatih soba
                if res['room_num'] not in rooms_rented_nums:
                    rooms_rented_nums.append(res['room_num'])

    rooms_rented = len(rooms_rented_nums)
    print('Izdatih soba: ',rooms_rented)


def res_finished(recep_hotel, od_datuma, do_datuma, reservation_list):
    res_realised = 0
    
    # lista realizovanih rezervacija za hotel
    print('\nGost          Vreme rezervisanja           Br.sobe          Period rezervacije')
    print('----------------------------------------------------------------------------------')

    for res in reservation_list:
        date_in = str2Date(res['date_in'], 'ymd')
        date_out = str2Date(res['date_out'], 'ymd')
        
        # pre else -> sve rezervacije koje uopšte 'ne kače' zadati period
        if (date_out <= od_datuma or date_in > do_datuma):
            continue
        else:
            if recep_hotel == res['id_hotel']:                    
                # rezervacije koje su realizovane/završene
                if res['status'] == 'z':
                    res_realised += 1
                    print(res['id_guest'].ljust(12) + res['creation_datetime'].ljust(31) + res['room_num'].ljust(12) + res['date_in'].ljust(13) + '-   ' + res['date_out'])

    print('\nRealizovanih rezervacija: ',res_realised)


def calc_avg(recep_hotel, od_datuma, do_datuma, reservation_list):
    
    br_ocena = 0
    suma_ocena = 0
    # Prosecna ocena u periodu
    for res in reservation_list:    
        if res['id_hotel'] == recep_hotel:
            if res['date_rated'] == '':
                continue
            date_rated = str2Date(res['date_rated'], 'ymd')

            if date_rated >= od_datuma and date_rated <= do_datuma:
                br_ocena += 1
                suma_ocena += float(res['rating'])
            
    if br_ocena == 0:
        prosek = 0
    else:
        prosek = suma_ocena / br_ocena
    print('Prosečna ocena hotela: ', prosek,'\n')


def calc_earned(recep_hotel, od_datuma, do_datuma, reservation_list):
    room_list = ucitaj_entity("rooms.txt",'room')

    # Zarada u periodu
    suma = 0
    for reservation in reservation_list:

        date_in = str2Date(reservation['date_in'], 'ymd')
        date_out = str2Date(reservation['date_out'], 'ymd')

        if (date_out <= od_datuma or date_in > do_datuma):
            continue
            
        else:
            if reservation['status'] != 'n' and recep_hotel == reservation['id_hotel']:	
                # fill liste datuma trajanja TE rezervacije

                date_in_counter = od_datuma
                list_of_taken_dates = []
                list_of_wanted_dates = []

                while(date_in_counter <= do_datuma):
                    list_of_wanted_dates.append(date_in_counter)
                    date_in_counter += datetime.timedelta(days=1)

                for room in room_list:
                    if room['hotel_id'] == recep_hotel and reservation['room_num'] == room['num']:

                        for date in reservation_list:
                            if date['id_reservation'] == reservation['id_reservation']:

                                date_start = str2Date(date['date_in'], 'ymd')                    				
                                date_end = str2Date(date['date_out'], 'ymd')

                                while date_start < date_end:
                                    list_of_taken_dates.append(date_start)
                                    date_start += datetime.timedelta(days=1)
                                
                                for old_date in list_of_taken_dates:
                                    if old_date in list_of_wanted_dates:
                                        suma += int(room['price'])
    print('Ukupna zarada: ',suma)