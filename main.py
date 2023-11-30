import side
import datetime

def admin_menu():
    print('\n1) Dodavanje novih hotela')
    print('2) Dodavanje novih recepcionera u hotele')
    print('3) Ažuriranje hotela')
    print('4) Brisanje hotela')
    print('5) Pretraga korisnika sistema')
    print('6) Brisanje recepcionera')
    print('x) Odjava sa sistema')
    
def admin_actions():

    print('\nDobro došli ! (admin)')
    print('--------------------------')
    izbor = ''

    while izbor.lower() != 'x':
        admin_menu()

        izbor = input('Unesite komandu >> ')

        if izbor == '1':
            print('\nDodajete hotel >> ')
            side.add_hotel()
            
        elif izbor == '2':
            print('\nDodajete recepcionere >> ')
            side.add_user('recepcioner')
                    
        elif izbor == '3':
            print('\nAžuriranje hotela u toku...\n')
            
            side.show_all_hotels()
            hotel_choice = input('\nAžuriraj hotel sa ID: ')

            # KONTROLA UNOSA
            hotel_checked = side.check_existing_hotel(hotel_choice)
            if not hotel_checked:
                print('\nNe postoji hotel sa unetim ID !')
            else:
                side.hotel_update(hotel_choice)

        elif izbor == '4':
            side.show_all_hotels()
            ID_hotela_za_brisanje = input('ID hotela za brisanje: ')
            
            side.delete_hotel(ID_hotela_za_brisanje)

        elif izbor == '5':
            print('\nPretražujete po jednom ili više zadatih kriterijuma >> \n')
            print('\nUnesite potpune podatke ili njihova početna slova >> \n')
            side.find_recep()
        
        elif izbor == '6':
            side.show_all_receps('all_users.txt', 'recepcioner')
            recepcioner_za_brisanje = input('Korisničko ime recepcionera za brisanje: ')
            side.delete_recep(recepcioner_za_brisanje)

        elif izbor.lower() == 'x':
            print('\nOdjavljeni ste...\n')
        else:
            print('\nNepoznata komanda!')
        
# GUEST MENU

def guest_menu():
    print('1) Pregled hotela')
    print('2) Pretraga hotela')
    print('3) Najbolje ocenjeni hoteli')
    print('4) Kreiraj rezervaciju')
    print('5) Pregled rezervacija')
    print('6) Oceni hotel')
    print('x) Odjava sa sistema')
    
def guest_actions(current_user):
    print('\nDobro došli ! (korisnik)')
    print('--------------------------')
    izbor = ''
    while izbor.lower() != 'x':
        guest_menu()

        izbor = input('Unesite komandu >> ')

        if izbor == '1':
            print('\nLista hotela...')
            side.show_all_hotels()

        elif izbor == '2':
            print('\nPretražujete po jednom ili više zadatih kriterijuma >> ')
            side.find_hotel()

        elif izbor == '3':
            print('\nPrikaz 5 najbolje ocenjenih hotela...\n')
            side.show_best_hotels()

        elif izbor == '4':
            print('\nKreirate rezervaciju...\n')
            
            side.add_reservation(current_user)        
        elif izbor == '5':
            print('\nPrikaz liste rezervacija...\n')

            side.show_all_reservations("all_reservations.txt", 'reservation',current_user)
        
        elif izbor == '6':
            # DOZVOLJENO OCENITI SAMO ONE HOTELE KOD KOJIH SU POSTOJALE REZERVACIJE TOG KORISNIKA odnosno GUEST-a
            side.add_rate(current_user)
        
        elif izbor.lower() == 'x':
            print('\nOdjavljeni ste...\n')
        
        else:
            print('Uneta komanda ne postoji!\n')

def recep_menu():
    print('1) Pretraga soba')
    print('2) Pretraga rezervacija')
    print('3) Kreiranje izveštaja')
    print('x) Odjava sa sistema')

def recep_actions(recep_hotel):
    print('\nDobro došli ! (recepcioner)')
    print('----------------------------')
    izbor = ''
    while izbor.lower() != 'x':
        recep_menu()

        izbor = input('Unesite komandu >> ')

        if izbor == '1':
            print('\nPretražujete po jednom ili više zadatih kriterijuma >> ')
            side.find_room(recep_hotel)
            
        elif izbor == '2':
            print('Pretraga rezervacija >> ')
            side.find_reservation(recep_hotel)
            
        elif izbor == '3':
            print('\nIzveštavanje >> ')
            side.report(recep_hotel)

        elif izbor.lower() == 'x':
            print('\nOdjavljeni ste...\n')
        else:
            print('Uneta komanda ne postoji!')


def unregistered():
    var_command = ''

    while var_command.lower() != 'x' :
        print('\n1) Registracija')
        print('2) Prijava na sistem')
        print('x) Izlazak iz aplikacije')

        var_command = input('Unesite komandu >> ')
        if var_command == '1':
            print('\nOstavite svoje podatke >>\n\n** >> Korisničko ime biće snimljeno malim slovima << **')
            side.add_user('gost')
            
        elif var_command == '2':
            current_user = side.sign_in()
            user_role = side.find_current_role(current_user)
            recep_hotel = side.find_employee_hotel(current_user)

            if user_role == 'admin' :
                admin_actions()
                
            elif user_role == 'gost' :
                guest_actions(current_user)

            elif user_role == 'recepcioner' :
                recep_actions(recep_hotel)

            elif user_role == None:
                print('\nNeuspešna prijava nakon 3 pokušaja.\nDoviđenja.\n')
                # input -> da bi se videla prikazana poruka pre izlaska iz app.
                input('')
                var_command = 'x'


        elif var_command.lower() == 'x':
            print('\nDoviđenja.\n')
        else:
            print('\nUneta komanda ne postoji!')


if __name__ == "__main__":
    unregistered()