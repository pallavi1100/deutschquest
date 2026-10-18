"""80 original, harder A1/A1+ scenario questions for DeutschQuest."""


def C(prompt, options, answer, grammar, example):
    return {"prompt": prompt, "options": options, "answer": answer, "grammar": grammar, "example": example, "mode": "choice"}


def T(prompt, answer, grammar, example, hint=""):
    return {"prompt": prompt, "answer_text": answer, "grammar": grammar, "example": example, "hint": hint, "mode": "type"}


def O(prompt, tokens, grammar, example):
    return {"prompt": prompt, "tokens": tokens, "answer_text": " ".join(tokens), "grammar": grammar, "example": example, "mode": "order"}


def L(prompt, spoken, options, answer, grammar, example):
    return {"prompt": prompt, "listen_text": spoken, "options": options, "answer": answer, "grammar": grammar, "example": example, "mode": "listen"}


EXTRA_MISSIONS = [
    {
        "id": "morning", "title": "Der Morgenmarathon", "subtitle": "Get ready and catch the tram before work",
        "location": "Your Apartment", "emoji": "🌅", "grammar": "Time, separable verbs, word order", "difficulty": "A1+",
        "questions": [
            C("Complete: Ich stehe jeden Tag um sieben Uhr ___.", ["auf", "an", "ein"], 0, "aufstehen is separable: in a main clause, auf moves to the end.", "Ich stehe um sieben Uhr auf. — I get up at seven."),
            O("Arrange: I take the bus today.", ["Heute", "fahre", "ich", "mit", "dem", "Bus."], "In statements, the finite verb stays in second position. mit requires the dative dem Bus.", "Heute fahre ich mit dem Bus. — Today I take the bus."),
            C("Which time means 7:30 in everyday German?", ["halb acht", "halb sieben", "Viertel nach acht"], 0, "halb acht means halfway to eight, not half past eight.", "Es ist halb acht. — It is 7:30."),
            T("Complete the word: Ich ___ um acht Uhr an. (arrive)", "komme", "ankommen is separable: ich komme ... an. The conjugated part changes with ich.", "Ich komme um acht Uhr an. — I arrive at eight.", "kommen → ich ..."),
            L("Listen: What does the speaker do first?", "Zuerst frühstücke ich, dann gehe ich zur Arbeit.", ["Has breakfast", "Goes shopping", "Goes to sleep"], 0, "zuerst = first; dann = then. frühstücken means to have breakfast.", "Zuerst frühstücke ich. — First, I have breakfast."),
            C("Complete: Um wie viel Uhr ___ du auf?", ["stehst", "steht", "stehen"], 0, "With du the stem steh- takes -st; the prefix auf stays at the end.", "Wann stehst du auf? — When do you get up?"),
            O("Arrange: On Monday I work from nine to five.", ["Am", "Montag", "arbeite", "ich", "von", "neun", "bis", "fünf."], "Am Montag is first position; arbeite must be next. von ... bis ... gives a time range.", "Am Montag arbeite ich von neun bis fünf."),
            C("Choose the correct phrase: I go to bed at ten.", ["Ich gehe um zehn Uhr ins Bett.", "Ich gehe im zehn Uhr Bett.", "Ich gehen um zehn ins Bett."], 0, "Use um for an exact time, and ins Bett gehen for going to bed.", "Ich gehe um zehn Uhr ins Bett. — I go to bed at ten."),
        ]
    },
    {
        "id": "apartment", "title": "Die neue Wohnung", "subtitle": "Find an apartment and meet the neighbours",
        "location": "Apartment Building", "emoji": "🏠", "grammar": "Possessives, negation, location and dative", "difficulty": "A1+",
        "questions": [
            C("Complete: Das ist ___ Zimmer. (my room)", ["mein", "meine", "meinen"], 0, "Zimmer is neuter (das Zimmer); nominative possessive is mein Zimmer.", "Das ist mein Zimmer. — This is my room."),
            T("Write one word: Die Wohnung ist ___ . (small)", "klein", "After sein, adjectives have no ending: Die Wohnung ist klein.", "Die Wohnung ist klein, aber hell. — The flat is small but bright."),
            C("Which sentence means 'There is no balcony'?", ["Es gibt keinen Balkon.", "Es gibt nicht Balkon.", "Es sind kein Balkon."], 0, "es gibt takes accusative. Balkon is masculine, so use keinen.", "Es gibt keinen Balkon. — There is no balcony."),
            O("Arrange: The kitchen is next to the bathroom.", ["Die", "Küche", "ist", "neben", "dem", "Bad."], "neben can take dative for location (where?), so das Bad becomes dem Bad.", "Die Küche ist neben dem Bad."),
            L("Listen: Which floor is the apartment on?", "Meine Wohnung ist im dritten Stock.", ["Third floor", "First floor", "Ground floor"], 0, "im = in dem. Ordinal numbers take endings: im dritten Stock.", "Sie wohnt im dritten Stock. — She lives on the third floor."),
            C("What is the polite question for 'Is the room still available'?", ["Ist das Zimmer noch frei?", "Haben das Zimmer frei?", "Das Zimmer ist frei noch?"], 0, "In a yes/no question, the finite verb comes first. noch frei = still available.", "Ist das Zimmer noch frei? — Is the room still available?"),
            T("Write one word: Ich wohne ___ Bremen. (in)", "in", "The preposition in is used with a city to mean in.", "Ich wohne in Bremen. — I live in Bremen."),
            C("Choose the correct sentence: 'My neighbours are friendly.'", ["Meine Nachbarn sind freundlich.", "Mein Nachbarn ist freundlich.", "Meine Nachbarn seid freundlich."], 0, "Plural possessive is meine and plural sein is sind.", "Meine Nachbarn sind freundlich. — My neighbours are friendly."),
        ]
    },
    {
        "id": "appointments", "title": "Der Terminkalender", "subtitle": "Book appointments and change plans",
        "location": "Service Desk", "emoji": "📅", "grammar": "Dates, modal verbs and polite requests", "difficulty": "A1+",
        "questions": [
            C("How do you politely ask for an appointment?", ["Ich möchte einen Termin vereinbaren.", "Ich will ein Termin vereinbaren.", "Ich möchte eine Termin."], 0, "Termin is masculine. The object of vereinbaren is accusative: einen Termin.", "Ich möchte einen Termin vereinbaren. — I'd like to make an appointment."),
            O("Arrange: Can we meet on Tuesday?", ["Können", "wir", "uns", "am", "Dienstag", "treffen?"], "Yes/no questions begin with the finite modal Können, while the infinitive treffen goes last.", "Können wir uns am Dienstag treffen?"),
            L("Listen: When is the appointment?", "Der Termin ist am Donnerstag um vierzehn Uhr.", ["Thursday at 2 PM", "Tuesday at 4 PM", "Thursday at 4 PM"], 0, "vierzehn Uhr = 14:00 = 2 PM. am gives a weekday.", "Der Termin ist am Donnerstag um vierzehn Uhr."),
            T("One word: Ich ___ morgen nicht kommen. (can)", "kann", "können with ich becomes kann; the infinitive kommen stays at the end.", "Ich kann morgen nicht kommen. — I cannot come tomorrow."),
            C("Which date is spoken 'am fünften Mai'?", ["5 May", "15 May", "25 May"], 0, "Ordinal dates after am take -ten in this range: am fünften Mai = on 5 May.", "Ich habe am fünften Mai einen Termin."),
            C("Which phrase is best to postpone an appointment?", ["Können wir den Termin verschieben?", "Wann Sie Termin weg?", "Ich bin den Termin langsam."], 0, "verschieben means postpone/reschedule; the modal verb können is used for polite questions.", "Können wir den Termin verschieben?"),
            O("Arrange: I have an appointment tomorrow morning.", ["Ich", "habe", "morgen", "früh", "einen", "Termin."], "Finite verb habe is in position two; Termin is masculine accusative: einen.", "Ich habe morgen früh einen Termin."),
            C("You want someone to speak slowly. Choose the best sentence.", ["Können Sie bitte langsamer sprechen?", "Kannst Sie langsam sprechen?", "Sprechen langsamer Sie bitte?"], 0, "With formal Sie, use können. A modal yes/no question has modal + subject + infinitive.", "Können Sie bitte langsamer sprechen?"),
        ]
    },
    {
        "id": "doctor", "title": "In der Arztpraxis", "subtitle": "Explain how you feel and ask for help",
        "location": "Health Centre", "emoji": "🩺", "grammar": "Haben, body parts, müssen and seit", "difficulty": "A1+",
        "questions": [
            C("How do you say 'I have a headache'?", ["Ich habe Kopfschmerzen.", "Ich bin Kopfschmerzen.", "Ich haben Kopfweh."], 0, "German uses haben for symptoms such as Kopfschmerzen.", "Ich habe Kopfschmerzen. — I have a headache."),
            L("Listen: What hurts?", "Mein Rücken tut weh.", ["Back", "Stomach", "Leg"], 0, "weh tun = to hurt; mein Rücken is my back.", "Mein Rücken tut weh. — My back hurts."),
            T("One word: Ich ___ zum Arzt gehen. (must)", "muss", "müssen with ich becomes muss; gehen is an infinitive at the end.", "Ich muss zum Arzt gehen. — I have to go to the doctor."),
            O("Arrange: I have had a cold since Monday.", ["Ich", "bin", "seit", "Montag", "erkältet."], "For a state continuing since a time, use seit + time with present tense, not English perfect.", "Ich bin seit Montag erkältet."),
            C("Which sentence asks 'Where is the pharmacy'?", ["Wo ist die Apotheke?", "Wer ist die Apotheke?", "Wann gibt die Apotheke?"], 0, "Wo asks location; Apotheke is feminine and takes die.", "Wo ist die Apotheke? — Where is the pharmacy?"),
            C("Complete: Ich brauche ___ Medikament. (a medicine)", ["ein", "eine", "einen"], 0, "Medikament is neuter: das Medikament. Accusative neuter indefinite article is ein.", "Ich brauche ein Medikament."),
            T("One word: Mir geht es nicht ___. (well)", "gut", "Mir geht es gut / nicht gut is a standard way to express how you are feeling.", "Mir geht es nicht gut. — I don't feel well."),
            C("How do you politely ask for help?", ["Können Sie mir bitte helfen?", "Können Sie mich bitte helfen?", "Helfen ich Sie bitte?"], 0, "helfen takes a dative recipient: mir, not mich.", "Können Sie mir bitte helfen? — Can you help me, please?"),
        ]
    },
    {
        "id": "grocery", "title": "Der Einkaufsboss", "subtitle": "Complete a tricky shopping list on a budget",
        "location": "Supermarket", "emoji": "🥦", "grammar": "Quantities, kein, articles and accusative", "difficulty": "A1+",
        "questions": [
            C("Complete: Ich kaufe ___ Brot. (a loaf of bread)", ["ein", "einen", "eine"], 0, "Brot is neuter: das Brot. After kaufen the direct object uses accusative ein Brot.", "Ich kaufe ein Brot. — I am buying a loaf of bread."),
            L("Listen: How much milk is needed?", "Bitte kaufen Sie zwei Liter Milch.", ["Two litres", "Three bottles", "One litre"], 0, "zwei Liter = two litres. The measurement Liter remains unchanged after zwei.", "Ich brauche zwei Liter Milch."),
            C("Which phrase means 'No apples, please'?", ["Keine Äpfel, bitte.", "Keinen Äpfel, bitte.", "Nicht Äpfel, bitte."], 0, "The plural negative article is keine in nominative/accusative.", "Keine Äpfel, bitte. — No apples, please."),
            O("Arrange: I'm looking for the eggs.", ["Ich", "suche", "die", "Eier."], "Eier is plural; the definite accusative article is die.", "Ich suche die Eier. — I'm looking for the eggs."),
            T("One word: Ich hätte ___ eine Tüte. (gladly / please)", "gern", "ich hätte gern ... is a polite way to request something.", "Ich hätte gern eine Tüte. — I'd like a bag, please."),
            C("What's the correct plural of die Tomate?", ["die Tomaten", "die Tomate", "die Tomates"], 0, "Many feminine nouns form their plural in -n/-en: die Tomate → die Tomaten.", "Drei Tomaten, bitte. — Three tomatoes, please."),
            C("How would the cashier ask 'Anything else'?", ["Sonst noch etwas?", "Auch nicht was?", "Was Sie kein?"], 0, "Sonst noch etwas? is a common short question in German shops.", "Sonst noch etwas? — Anything else?"),
            O("Arrange: I pay by card.", ["Ich", "bezahle", "mit", "Karte."], "mit Karte is a fixed common expression; finite verb is in second position.", "Ich bezahle mit Karte. — I pay by card."),
        ]
    },
    {
        "id": "invitations", "title": "Ein Wochenende mit Freunden", "subtitle": "Make plans, accept invitations and explain why",
        "location": "City Park", "emoji": "🎉", "grammar": "Modal verbs, möchten and time expressions", "difficulty": "A1+",
        "questions": [
            C("How do you say 'Do you want to come along'? (informal)", ["Möchtest du mitkommen?", "Möchten du mitkommen?", "Du möchtest mitkommen?"], 0, "With du, möchten becomes möchtest; yes/no questions start with the conjugated verb.", "Möchtest du mitkommen? — Would you like to come along?"),
            T("One word: Ich habe am Samstag ___. (time)", "Zeit", "Zeit haben means to have time; Zeit is capitalized because it is a noun.", "Ich habe am Samstag Zeit. — I have time on Saturday."),
            O("Arrange: We want to go to the cinema.", ["Wir", "wollen", "ins", "Kino", "gehen."], "The modal wollen is conjugated; gehen stays as the infinitive at the end.", "Wir wollen ins Kino gehen."),
            L("Listen: Why can't Maria come?", "Maria muss am Samstag arbeiten.", ["She has to work", "She is ill", "She has no ticket"], 0, "müssen expresses necessity; arbeiten stays at the end.", "Sie muss am Samstag arbeiten."),
            C("What's a polite answer to an invitation?", ["Ja, gern!", "Ja, gar nicht!", "Ja, bitte nicht!"], 0, "gern expresses liking or willingness: Ja, gern! = Yes, gladly.", "Kommst du mit? — Ja, gern!"),
            C("Which preposition goes with 'Sunday' in a time expression?", ["am Sonntag", "im Sonntag", "um Sonntag"], 0, "Use am with days of the week, um with times, and im with months/seasons.", "Am Sonntag habe ich frei. — I'm free on Sunday."),
            T("One word: Ich bin heute ___ . (tired)", "müde", "After bin, an adjective is used in its basic form without an ending.", "Ich bin müde. — I'm tired."),
            C("What does 'Vielleicht nächste Woche' mean?", ["Maybe next week", "Definitely tomorrow", "Never again"], 0, "vielleicht means maybe; nächste Woche means next week.", "Vielleicht nächste Woche! — Maybe next week!"),
        ]
    },
    {
        "id": "workplus", "title": "Schichtwechsel", "subtitle": "Handle requests at work without switching to English",
        "location": "Retail Store", "emoji": "🧾", "grammar": "Polite requests, imperatives and object pronouns", "difficulty": "A1+",
        "questions": [
            C("Customer: 'Kann ich mit Karte bezahlen?' You answer:", ["Ja, natürlich.", "Nein, du ist.", "Ich verstehe Karte."], 0, "Ja, natürlich means yes, of course. Formal/customer interactions need polite phrasing.", "Ja, natürlich. — Yes, of course."),
            O("Arrange: Please wait a moment.", ["Warten", "Sie", "bitte", "einen", "Moment."], "Formal imperative: conjugated infinitive-like form + Sie; Moment is masculine accusative: einen.", "Warten Sie bitte einen Moment."),
            C("Complete: Ich frage ___ Kollegin. (my female colleague)", ["meine", "meinen", "mein"], 0, "Kollegin is feminine, so accusative possessive is meine.", "Ich frage meine Kollegin. — I'll ask my colleague."),
            T("One word: Ich verstehe Sie ___. (not)", "nicht", "nicht usually negates a verb/whole statement: Ich verstehe Sie nicht.", "Entschuldigung, ich verstehe Sie nicht."),
            L("Listen: What does the customer want?", "Entschuldigung, haben Sie eine größere Tasche?", ["A bigger bag", "A smaller jacket", "A receipt"], 0, "größere Tasche = a larger bag. This question uses formal Sie.", "Haben Sie eine größere Tasche?"),
            C("Which sentence is most appropriate at the checkout?", ["Brauchen Sie den Kassenbon?", "Du brauchst Bon?", "Will der Bon Sie?"], 0, "Brauchen Sie ...? is a polite formal question; Kassenbon is masculine: den in accusative.", "Brauchen Sie den Kassenbon? — Do you need the receipt?"),
            C("What does 'Ich schaue kurz nach' mean?", ["I'll quickly check", "I am looking away", "I'm taking a break"], 0, "nachschauen is separable: ich schaue ... nach. kurz suggests briefly.", "Ich schaue kurz nach. — I'll check quickly."),
            O("Arrange: I can't find the price.", ["Ich", "kann", "den", "Preis", "nicht", "finden."], "kann is finite in second position, while infinitive finden is at the end. Preis is masculine accusative: den.", "Ich kann den Preis nicht finden."),
        ]
    },
    {
        "id": "travelplus", "title": "Der Zug ist weg!", "subtitle": "Read timetables, buy tickets and survive delays",
        "location": "Train Station", "emoji": "🚆", "grammar": "Dative after mit, separable verbs, departures", "difficulty": "A1+",
        "questions": [
            C("Complete: Ich fahre ___ Zug nach Hamburg.", ["mit dem", "mit den", "mit der"], 0, "Zug is masculine; mit always takes dative, so mit dem Zug.", "Ich fahre mit dem Zug. — I go by train."),
            L("Listen: Which platform?", "Der Zug nach Hamburg fährt von Gleis sieben ab.", ["Platform seven", "Platform ten", "Platform six"], 0, "Gleis sieben means platform seven. abfahren is separable: fährt ... ab.", "Der Zug fährt von Gleis sieben ab."),
            O("Arrange: When does the train depart?", ["Wann", "fährt", "der", "Zug", "ab?"], "W-question: Wann + conjugated verb + subject. ab is placed at the end.", "Wann fährt der Zug ab?"),
            T("One word: Wo kann ich ein Ticket ___? (buy)", "kaufen", "Modal verbs like kann move the main infinitive to the end.", "Wo kann ich ein Ticket kaufen?"),
            C("What does 'Verspätung' mean?", ["Delay", "Discount", "Departure"], 0, "die Verspätung is a delay, often announced at railway stations.", "Der Zug hat zehn Minuten Verspätung."),
            C("Which is correct: 'I'm waiting for the train'?", ["Ich warte auf den Zug.", "Ich warte für der Zug.", "Ich warte zu die Zug."], 0, "warten auf takes accusative. Zug is masculine, so den Zug.", "Ich warte auf den Zug. — I'm waiting for the train."),
            T("One word: Ich möchte eine ___ nach Berlin. (ticket)", "Fahrkarte", "die Fahrkarte is feminine; eine Fahrkarte is accusative and means a ticket.", "Eine Fahrkarte nach Berlin, bitte."),
            C("Choose the correct response: 'Wo muss ich umsteigen?'", ["In Hannover.", "Um acht Euro.", "Drei Personen."], 0, "umsteigen means change trains; Wo? asks where.", "Sie müssen in Hannover umsteigen."),
        ]
    },
    {
        "id": "past", "title": "Was hast du gemacht?", "subtitle": "Tell a friend what happened yesterday",
        "location": "Friends' Café", "emoji": "📸", "grammar": "First Perfekt sentences with haben and sein", "difficulty": "A1+",
        "questions": [
            C("Complete: Ich ___ gestern Pizza gegessen.", ["habe", "bin", "hat"], 0, "essen uses haben in Perfekt: ich habe ... gegessen.", "Ich habe gestern Pizza gegessen."),
            O("Arrange: Yesterday I went to the cinema.", ["Ich", "bin", "gestern", "ins", "Kino", "gegangen."], "gehen forms Perfekt with sein, not haben: ich bin gegangen.", "Ich bin gestern ins Kino gegangen."),
            T("One word: Wir haben Deutsch ___ . (learned)", "gelernt", "lernen is a regular verb; its participle is gelernt: haben + gelernt.", "Wir haben Deutsch gelernt."),
            L("Listen: Where did the speaker go?", "Ich bin am Wochenende nach Berlin gefahren.", ["Berlin", "Munich", "Hamburg"], 0, "fahren to a destination often uses sein in Perfekt: bin gefahren.", "Ich bin nach Berlin gefahren."),
            C("Which sentence is grammatical?", ["Sie hat einen Film gesehen.", "Sie ist einen Film gesehen.", "Sie hat einen Film sehen."], 0, "sehen forms Perfekt with haben + gesehen.", "Sie hat einen Film gesehen."),
            C("Which means 'I didn't buy anything'?", ["Ich habe nichts gekauft.", "Ich bin nichts gekauft.", "Ich habe nicht gekauft nichts."], 0, "nichts is nothing. kaufen forms Perfekt with haben + gekauft.", "Ich habe nichts gekauft."),
            O("Arrange: What did you do yesterday?", ["Was", "hast", "du", "gestern", "gemacht?"], "A Perfekt question uses the conjugated auxiliary in second position and participle at the end.", "Was hast du gestern gemacht?"),
            T("One word: Ich bin spät nach Hause ___ . (come)", "gekommen", "kommen uses sein in Perfekt: bin gekommen.", "Ich bin spät nach Hause gekommen."),
        ]
    },
    {
        "id": "boss", "title": "A1 Boss Battle", "subtitle": "One final challenge across everyday German life",
        "location": "DeutschQuest Arena", "emoji": "⚡", "grammar": "A1 mixed revision: grammar, listening, ordering", "difficulty": "A1 BOSS",
        "questions": [
            O("Arrange: I would like to book an appointment tomorrow.", ["Ich", "möchte", "morgen", "einen", "Termin", "vereinbaren."], "The conjugated möchten goes second. With a modal-like verb, the infinitive vereinbaren finishes the sentence.", "Ich möchte morgen einen Termin vereinbaren."),
            C("Select the correct sentence.", ["Heute muss ich arbeiten.", "Heute ich muss arbeiten.", "Heute muss arbeiten ich."], 0, "Heute counts as first position; finite verb muss is in second position.", "Heute muss ich arbeiten. — I have to work today."),
            L("Listen: What does the person need?", "Entschuldigung, ich brauche eine Fahrkarte nach Bremen.", ["A ticket to Bremen", "A room in Bremen", "A coffee from Bremen"], 0, "eine Fahrkarte nach Bremen is a ticket to Bremen.", "Ich brauche eine Fahrkarte nach Bremen."),
            T("One word: Ich warte auf ___ Bus. (the)", "den", "warten auf requires accusative; Bus is masculine, so den.", "Ich warte auf den Bus."),
            C("Choose the correct combination.", ["mit dem Zug / für den Freund", "mit den Zug / für dem Freund", "mit der Zug / für der Freund"], 0, "mit always takes dative; für takes accusative.", "Ich fahre mit dem Zug. Das Geschenk ist für den Freund."),
            O("Arrange: Could you please speak more slowly?", ["Können", "Sie", "bitte", "langsamer", "sprechen?"], "With formal Sie, the modal is Können; the infinitive sprechen goes last.", "Können Sie bitte langsamer sprechen?"),
            C("Which sentence about yesterday is correct?", ["Ich bin gestern nach Hause gegangen.", "Ich habe gestern nach Hause gegangen.", "Ich bin gestern nach Hause gehen."], 0, "Movement verb gehen uses sein + past participle gegangen.", "Ich bin gestern nach Hause gegangen."),
            T("One word: Ich ___ keinen Kaffee. (would like)", "möchte", "Ich möchte + accusative object. Kaffee is masculine, so keinen in negation.", "Ich möchte keinen Kaffee. — I don't want coffee."),
        ]
    },
]

PHRASES = [
    {"de": "Guten Morgen! Wie geht es Ihnen?", "en": "Good morning! How are you?", "tip": "Keep the final -en in Morgen soft, and say Ihnen with a clear long ee sound."},
    {"de": "Ich heiße Lena und komme aus Indien.", "en": "My name is Lena and I'm from India.", "tip": "In ich, the ch is a soft sound made high in the mouth. ß in heiße sounds like ss."},
    {"de": "Ich möchte einen Kaffee, bitte.", "en": "I'd like a coffee, please.", "tip": "The ö in möchte is rounded. Say 'möch-te' slowly before the full sentence."},
    {"de": "Können Sie bitte langsamer sprechen?", "en": "Could you speak more slowly, please?", "tip": "Round your lips for ö in können; don't swallow the final -en."},
    {"de": "Brauchen Sie eine Tüte?", "en": "Do you need a bag?", "tip": "The ü in Tüte is made with rounded lips. Stretch both vowels deliberately."},
    {"de": "Ich arbeite heute von neun bis fünf.", "en": "I work from nine to five today.", "tip": "In heute, the eu sounds like 'oy'. Stress AR-bei-te."},
    {"de": "Wo kann ich ein Ticket kaufen?", "en": "Where can I buy a ticket?", "tip": "Use rising intonation if asking for help, and pronounce the f in kaufen clearly."},
    {"de": "Der Zug fährt um acht Uhr ab.", "en": "The train departs at eight o'clock.", "tip": "The ä in fährt is a front vowel; keep the final t audible."},
    {"de": "Ich habe morgen einen Termin.", "en": "I have an appointment tomorrow.", "tip": "Termin is stressed on the second syllable: Ter-MIN."},
    {"de": "Entschuldigung, wo ist die Apotheke?", "en": "Excuse me, where is the pharmacy?", "tip": "Apotheke is stressed on -the-: Apo-THE-ke."},
    {"de": "Ich bin gestern nach Bremen gefahren.", "en": "I traveled to Bremen yesterday.", "tip": "Stress FAH in gefahren's base fahren and keep the r gentle."},
    {"de": "Gehen Sie geradeaus und dann links.", "en": "Go straight ahead and then left.", "tip": "geradeaus flows together: ge-RA-de-aus."},
]
