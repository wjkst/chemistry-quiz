import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def encrypt_password(password, key):
    iv = os.urandom(16)  
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()

    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_password).decode()

def decrypt_password(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password.encode())
    iv = encrypted_password[:16]
    encrypted_password = encrypted_password[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_password) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    password = unpadder.update(decrypted_data) + unpadder.finalize()
    return password.decode()

key = os.environ.get('ENCRYPTION_KEY', 'This is a key123').encode('utf-8')

encrypted_password = "agZiy7MEVLYFAH1NdwyagbVFlVRdcmyfe/AjWfJBCt9PwT/ZJl1QtiiH0pinPBUb"

# E-mail functie
def verzend_resultaten_via_email(naam, score, totaal_vragen):
    afzender_email = "project@wjkst.nl"
    afzender_wachtwoord = decrypt_password(encrypted_password, key)
    ontvanger_emails = ['example@webpage.com'] #enter an e-mail address to send the results to here. separate multiple e-mail addresses with a comma.

    onderwerp = f"Resultaten van de quiz - {naam}"
    body = f'{naam} heeft {score} van de {totaal_vragen} vragen correct beantwoord!'

    msg = MIMEMultipart()
    msg['From'] = afzender_email
    msg['To'] = ", ".join(ontvanger_emails)
    msg['Subject'] = onderwerp

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.strato.com', 587)
        server.starttls()
        server.login(afzender_email, afzender_wachtwoord)
        text = msg.as_string()
        server.sendmail(afzender_email, ontvanger_emails, text)
        server.quit()
        print("Resultaten succesvol verzonden via e-mail.")
    except Exception as e:
        print(f"Fout bij het verzenden van e-mail: {e}")


# Quiz data
vragen_en_antwoorden_onderwerp1 = [
    ('Cu is ', ['koper'], 'koper'),
    ('Cd is ', ['cadmium'], 'cadmium'),
    ('Zn is ', ['zink'], 'zink'),
    ('Sn is ', ['tin'], 'tin'),
    ('Pb is ', ['lood'], 'lood'),
    ('Fe is ', ['ijzer'], 'ijzer'),
    ('Ne is ', ['neon'], 'neon'),
    ('Cr is ', ['chroom'], 'chroom'),
    ('H is ', ['waterstof'], 'waterstof'),
    ('Cl is ', ['chloor'], 'chloor'),
    ('He is ', ['helium'], 'helium'),
    ('Au is ', ['goud'], 'goud'),
    ('S is ', ['zwavel'], 'zwavel'),
    ('Ar is ', ['argon'], 'argon'),
    ('Hg is ', ['kwik'], 'kwik'),
    ('N is ', ['stikstof'], 'stikstof'),
    ('Al is ', ['aluminium'], 'aluminium'),
    ('F is ', ['fluor'], 'fluor'),
    ('Ni is ', ['nikkel'], 'nikkel'),
    ('Mg is ', ['magnesium'], 'magnesium'),
    ('C is ', ['koolstof'], 'koolstof'),
    ('Pt is ', ['platina'], 'platina'),
    ('O is ', ['zuurstof'], 'zuurstof'),
    ('Ca is ', ['calcium'], 'calcium'),
    ('Ba is ', ['barium'], 'barium'),
    ('Br is ', ['broom'], 'broom'),
    ('Ag is ', ['zilver'], 'zilver'),
    ('Si is ', ['silicium'], 'silicium'),
    ('K is ', ['kalium'], 'kalium'),
    ('P is ', ['fosfor'], 'fosfor'),
    ('Na is ', ['natrium'], 'natrium'),
    ('I is ', ['jood'], 'jood'),
    ('C2H60 is ', ['alcohol'], 'alcohol'),
    ('NH4', ['ammoniak'], 'ammoniak'),
    ('C6H1206', ['glucose'], 'glucose'),
    ('CH4', ['methaan'], 'methaan'),
    ('Na2CO3', ['soda'], 'soda'),
    ('H20', ['water'], 'water'),
    ('H202', ['waterstofperoxide'], 'waterstofperoxide'),
    ('Br2', ['broom'], 'broom'),
    ('Cl2', ['chloor'], 'chloor'),
    ('F2', ['fluor'], 'fluor'),
    ('I2', ['jood'], 'jood'),
    ('N2', ['stikstof'], 'stikstof'),
    ('H2', ['waterstof'], 'waterstof'),
    ('O2', ['zuurstof'], 'zuurstof')
]

vragen_en_antwoorden_onderwerp2 = [
    ('Bij een chemische reactie verdwijnen de beginstoffen en ontstaan er nieuwe stoffen, de ... ', ['reactieproducten'], 'reactieproducten'),
    ('Je kunt de fase van een stof weergeven met een afkorting, de gasvormige fase is ... ', ['g'], 'g'),
    ('Je kunt de fase van een stof weergeven met een afkorting, vioeibare fase is ... ', ['l'], 'l'),
    ('Je kunt de fase van een stof weergeven met een afkorting, de vaste fase is ... ', ['s'], 's'),
    ('Stoffen veranderen als je ze voldoende verhit, de stof kan ..., als er voldoende zuurstof aanwezig is ', ['verbranden'], 'verbranden'),
    ('Stoffen veranderen als je ze voldoende verhit, de stof kan ..., als er geen zuurstof aanwezig is ', ['ontleden'], 'ontleden'),
    ('Bij een ... staat één stof voor de pijl en twee of meer stoffen na de pijl ', ['ontledingsreactie'], 'ontledingsreactie'),
    ('Bij de ontleding van een ... stof ontstaan witte rook, water (condens) en koolstof (roet) ', ['organische'], 'organische'),
    ('Er zijn zeven reactieverschijnselen, verandering van keur, verandering van geur, verandering van smaak, warmte, rook, vlammen en ... ', ['licht'], 'licht'),
    ('Atomen zijn de ... van moleculen ', ['bouwstenen'], 'bouwstenen'),
    ('Een ... is een stof die je, door een chemische reactie, niet in nog kleinere deeltjes kunt splitsen ', ['element'], 'element'),
    ('Een element bestaat uit één ... ', ['atoomsoort'], 'atoomsoort'),
    ('Elementen kun je onderverdelen in ... ', ['metalen en niet metalen'], 'metalen en niet metalen'),
    ('De eigenschappen van een ... zijn anders dan de eigenschappen van de atomen waaruit het ... is opgebouwd (andwoord scheiden met komma)', ['molecuul, molecuul'], 'molecuul, molecuul'),
    ('Een moleculaire stof is opgebouwd uit ...', ['niet metalen'], 'niet metalen '),
    ('Bij een chemische reactie veranderen de atomen niet, maar worden ze anders ...', ['gerangschikt'], 'gerangschikt'),
    ('In een ... noteer je de namen van de betrokken stoffen. Beide geven weer welke stoffen met elkaar reageren en welke stoffen ontstaan ', ['reactieschema'], 'reactieschema'),
    ('De ... is het getal dat voor de molecuulformule staat, het heeft betrekking op het hele molecuul ', ['coefficient'], 'coefficient'),
    ('De ... is het getal dat in de molecuulformule staat, heeft betrekking op het element dat ervoor staat ', ['index'], 'index'),
    ('Bij het kloppend maken van een ... zorg je ervoor dat er voor en na de pijl van elke atoomsoort evenveel atomen aanwezig zijn ', ['reactievergelijking'], 'reactievergelijking'),
    ('Bij het kloppend maken van een reactievergelijking mag je nooit een ... wijzigen ', ['index'], 'index'),
    ('Bij een ... maak je eerst koolstof en waterstof kloppend, Zuurstof maak je als laatste kloppend ', ['verbrandingsreactie'], 'verbrandingsreactie'),
    ('Je kunt stoffen ontleden door warmte toe te voeren, dit noem je ... ', ['thermolyse'], 'thermolyse'),
    ('Je kunt stoffen ontleden door er licht op te laten vallen, dit noem je ... ', ['fotolyse'],'fotolyse'),
    ('Je kunt stoffen ontleden door er elektrische stroom doorheen te leiden, dit noem je ... ', ['elektrolyse'], 'elektrolyse'),
    ('Niet-ontleedbare stoffen kunnen, door een chemische reactie, niet verder ontleed worden. Alle ... zijn niet-ontleedbare stoffen ', ['elementen'], 'elementen'),
    ('Alle verbindingen behoren tot de ... stoffen ', ['ontleedbare'], 'ontleedbare'),
    ('Nitroglycerine heeft een grote explosieve kracht, omdat er bij de ontleding veel ... stoffen vrijkomen ', ['gasvormige'], 'gasvormig'),
    ('Bij het verbranden van waterstof komt alleen water vrij Daarom draagt het gebruik van waterstof als brandstof niet bij aan het ... ', ['broeikaseffect'], 'broeikaseffect'),
    ('Waterstof kun je maken door de elektrolyse van water. Als de hiervoor benodigde elektrische energie op een duurzame manier is geproduceerd, spreek je van ... ', ['groene waterstof'], 'groene waterstof'),
    ('De grondstof voor de productie van aluminium is bauxiet. Dit bestaat voor een groot gedeelte uit ... ', ['aluminiumoxide'], 'aluminiumoxide'),
    ('De grondstof voor de productie van aluminium is ... . Dit bestaat voor een groot gedeelte uit aluminiumoxide ', ['bauxiet'], 'bauxiet'),
    ('Aluminium kun je maken door de ... van vioeibaar aluminiumoxide ', ['elektrolyse'], 'elektrolyse'),
    ('Aluminium kun je maken door de elektrolyse van vioeibaar ... ', ['aluminiumoxide'], 'aluminiumoxide')
]

vragen_en_antwoorden_onderwerp3 = [
    ('ontleden is ', ['het in kleine deeltjes uit elkaar vallen van moleculen', 'het spleiten van atomen', 'het delen van cellen'], 'het in kleine deeltjes uit elkaar vallen van moleculen'),
    ('een reactieverschijnsel is ', ['een stof die verscheint tijdens een ontledeing', 'verschijnsel dat je kunt waarnemen bij een chemische reactie', 'een gas dat ontstaad tijden een reactie'], 'verschijnsel dat je kunt waarnemen bij een chemische reactie'),
    ('een verbrandingsproduct is ', ['een restproduct dat ontstaat tijdens een verbranding', 'een brandstof', 'stof die ontstaat bij een verbrandingsreactie'], 'stof die ontstaat bij een verbrandingsreactie'),
    ('een atoom is ', ['ehet zelfde als een molecuul', 'bouwsteen van moleculen die je niet in nog keleinere deeltje kunt splitsen', 'bouwsteen van moleculen die je in keleinere deeltje kunt splitsen'], 'bouwsteen van moleculen die je niet in nog keleinere deeltje kunt splitsen'),
    ('een symbool is ', ['afkorting warmee een atoom of atoomsoort mee wordt aangegeven', 'afkorting warmee een element, atoom of atoomsoort mee wordt aangegeven', 'afkorting warmee een element mee wordt aangegeven'], 'afkorting warmee een element, atoom of atoomsoort mee wordt aangegeven'),
    ('een atoomsoort is ', ['een molecuul', 'type atoom', 'een verbinding'], 'type atoom'),
    ('een verbinding is ', ['een stof waarin twee elementen element aan elkaar zijn verbonden', 'een stof waarin twee, of meer, elementen element aan elkaar zijn verbonden', 'een stof waarin minimaal 5 elementen aan elkaar zijn verbonden'], 'een stof waarin twee, of meer, elementen element aan elkaar zijn verbonden'),
    ('een element is ', ['stof die uit één atoomsoort bestaat', 'edelmetaal', 'stof die uit meerdere atoomsoorten bestaat'], 'stof die uit één atoomsoort bestaat'),
    ('een moleculaire stof is ', ['stof die is opgebouwd uit metalen', 'stof die is opgebouwd uit niet metalen', 'een niet ontleedbare stof'], 'stof die is opgebouwd uit niet metalen'),
    ('coëfficiënt is ', ['getal dat in een reactievergelijking voor de molecuulformule staat', 'getal dat in een reactievergelijking na de molecuulformule staat', 'getal dat in een reactievergelijking voor de molecuulformule staat en het betreffende aantal moleculen weergeeft', 'getal dat in een reactievergelijking na de molecuulformule staat en het betreffende aantal moleculen weergeeft'], 'getal dat in een reactievergelijking voor de molecuulformule staat en het betreffende aantal moleculen weergeeft'),
    ('een molecuulformule is ', ['formule die aangeeft hoe vaak elke atoom in een molecuul voorkomt','formule die aangeeft hoe vaak elke atoomsoort in een molecuul voorkomt', 'een formule die aangeeft wat de onderlinge aantrekkingskracht is'], 'formule die aangeeft hoe vaak elke atoomsoort in een molecuul voorkomt'),
    ('een index is ', ['getal in molecuulformule dat het betreffende aantal atomen weergeeft', 'getal in molecuulformule dat het betreffende aantal protonen weergeeft', 'getal in molecuulformule dat het betreffende aantal neutronen weergeeft'], 'getal in molecuulformule dat het betreffende aantal atomen weergeeft'),
    ('een reactievergelijking is ', ['manier om met behulp van formules een molecuul te noteren', 'manier om met behulp van formules een chemische reactie te noteren', 'manier om met behulp van formules een organiche reactie te noteren'], 'manier om met behulp van formules een chemische reactie te noteren'),
    ('elektrolyse is ', ['ontledingsreactie met licht als energiebron', 'ontledingsreactie met elektrische stroom als energiebron', 'ontledingsreactie met waterstof als energiebron'], 'ontledingsreactie met elektrische stroom als energiebron'),
    ('een ontleedbare stof is ', ['stof die door een chemische reactie ontleed kan worden', 'stof die door een chemische reactie niet ontleed kan worden', 'stof die door een organiche reactie ontleed kan worden'], 'stof die door een chemische reactie ontleed kan worden'),
    ('fotolyse is ', ['ontledingsreactie met stroom als energiebron', 'ontledingsreactie met licht als energiebron', 'ontledingsreactie met straling als energiebron'], 'ontledingsreactie met licht als energiebron'),
    ('thermolyse is ', ['ontledingsreactie met licht als energiebron', 'ontledingsreactie met straling als energiebron', 'ontledingsreactie met warmte als energiebron'], 'ontledingsreactie met warmte als energiebron'),
    ('een niet-ontleedbare stof is ', ['stof die door een chemische reactie niet verder ontleed kan worden']),
    ('bauxiet is ', ['grondstof voor aluminiumproductie', 'een grondstof voor aluminiumproductie']),
    ('groene waterstof is ', ['waterstof', 'waterstof die op duurzame manier is geproduceerd', 'waterstof dat is geproduceerd'], 'waterstof die op duurzame manier is geproduceerd'),
    ('dynamiet is ', ['explosieve stof met dyroglycerine als werkzame stof', 'explosieve stof met nitroglycerine als werkzame stof', 'explosieve stof met C4 als werkzame stof'], 'explosieve stof met nitroglycerine als werkzame stof'),
    ('waterstof is ', ['broeikasgas', 'stof die kan dienen als zuurstof', 'stof die kan dienen als brandstof'], 'stof die kan dienen als brandstof')
]

random.shuffle(vragen_en_antwoorden_onderwerp1)
random.shuffle(vragen_en_antwoorden_onderwerp2)
random.shuffle(vragen_en_antwoorden_onderwerp3)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Applicatie")
        self.score = 0
        self.index = 0
        self.current_subject_index = 0
        self.subject_names = ["Onderwerp 1, elementen", "Onderwerp 2, begrippen", "Onderwerp 3, meerkeuzen"]
        self.naam = ""

        self.subjects = [
            vragen_en_antwoorden_onderwerp1,
            vragen_en_antwoorden_onderwerp2,
            vragen_en_antwoorden_onderwerp3
        ]

        self.name_label = tk.Label(root, text="Voer je naam in:", font=('Arial', 16))
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=10)
        self.start_button = tk.Button(root, text="Start Quiz", font=('Arial', 16), command=self.start_quiz)
        self.start_button.pack(pady=20)

    def start_quiz(self):
        self.naam = self.name_entry.get().strip()
        if not self.naam:
            messagebox.showwarning("Waarschuwing", "Voer je naam in om te beginnen.", font=('Arial', 16))
            return

        self.root.bind('<Return>', self.check_answer_event)

        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        self.subject_label = tk.Label(self.root, text=self.subject_names[self.current_subject_index])
        self.subject_label.pack()

        self.question_label = tk.Label(self.root, text="", font=('Arial', 16))
        self.question_label.pack(pady=10)

        self.var = tk.StringVar()
        self.var.set(None)

        self.answer_entry = tk.Entry(self.root)
        self.answer_entry.pack(pady=10)

        self.dropdown_var = tk.StringVar()
        self.dropdown_menu = tk.OptionMenu(self.root, self.dropdown_var, "")
        self.dropdown_menu.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Indienen", font=('Arial', 16), command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.root.bind('<Return>', self.check_answer_event)
        
        self.score_label = tk.Label(self.root, text=f'Score: {self.score}', font=('Arial', 12))
        self.score_label.pack(pady=10)

        self.load_questions()

    def load_questions(self):
        self.questions = self.subjects[self.current_subject_index]
        self.correct_answers = [q[2] for q in self.questions]
        self.index = 0
        self.display_question()

    def display_question(self):
        if self.index < len(self.questions):
            question, options, _ = self.questions[self.index]
            self.question_label.config(text=question)
            if len(options) > 1:
                self.dropdown_var.set('')
                self.dropdown_menu['menu'].delete(0, 'end')
                for option in options:
                    self.dropdown_menu['menu'].add_command(label=option, command=tk._setit(self.dropdown_var, option))
                self.dropdown_menu.pack()
                self.answer_entry.pack_forget()
            else:
                self.answer_entry.pack()
                self.dropdown_menu.pack_forget()
                self.answer_entry.delete(0, tk.END)
        else:
            self.current_subject_index += 1
            if self.current_subject_index < len(self.subjects):
                self.subject_label.config(text=self.subject_names[self.current_subject_index])
                self.load_questions()
            else:
                self.end_quiz()

    def end_quiz(self):
        self.question_label.config(text="Je hebt alle vragen beantwoord!", font=('Arial', 16))
        self.submit_button.config(state=tk.DISABLED)
        self.send_results()

    def check_answer_event(self, event):
        self.check_answer()

    def check_answer(self):
        correct_option = self.correct_answers[self.index]
        question, options, _ = self.questions[self.index]

        if len(options) > 1:
            selected_option = self.dropdown_var.get()
            if selected_option == correct_option:
                self.score += 1
                messagebox.showinfo("Resultaat", "Correct!")
            else:
                messagebox.showinfo("Resultaat", f"Fout antwoord. Het juiste antwoord is: {correct_option}")
        else:
            user_answer = self.answer_entry.get().strip()
            if user_answer.lower() == correct_option.lower():
                self.score += 1
                messagebox.showinfo("Resultaat", "Correct!")
            else:
                messagebox.showinfo("Resultaat", f"Fout antwoord. Het juiste antwoord is: {correct_option}")

        self.index += 1
        self.display_question()
        self.score_label.config(text=f'Score: {self.score}', font=('Arial', 12))

    def send_results(self):
        totaal_vragen = sum(len(subject) for subject in self.subjects)
        verzend_resultaten_via_email(self.naam, self.score, totaal_vragen)
        messagebox.showinfo("Einde", f"Je hebt {self.score} van de {totaal_vragen} vragen correct beantwoord! Resultaten zijn verzonden.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
