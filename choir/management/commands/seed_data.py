from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from choir import models

# Real assets live in the Next.js frontend's public/ folder.
FRONTEND_PUBLIC = Path(__file__).resolve().parents[4] / "frontend" / "public"


class Command(BaseCommand):
    help = "Seed the database with the choir's real current content (mirrors the frontend's src/data files)."

    def handle(self, *args, **options):
        self.seed_site_settings()
        self.seed_about_page()
        self.seed_calendar()
        self.seed_committees()
        self.seed_members()
        self.seed_songs()
        self.seed_news()
        self.seed_homilies()
        self.seed_projects()
        self.seed_constitution()
        self.seed_gallery()
        self.stdout.write(self.style.SUCCESS("Seed data loaded."))

    def attach_file(self, field, relative_path):
        path = FRONTEND_PUBLIC / relative_path
        if path.exists():
            with open(path, "rb") as f:
                field.save(path.name, File(f), save=False)

    def seed_site_settings(self):
        s = models.SiteSettings.load()
        s.short_name = "SSK"
        s.name_sw = "Kwaya ya Mt. Stefano Shahidi"
        s.name_en = "St. Stefano the Martyr Choir"
        s.parish_sw = "Parokia ya Kipawa"
        s.parish_en = "Kipawa Parish"
        s.diocese_sw = "Jimbo Kuu la Dar es Salaam"
        s.diocese_en = "Archdiocese of Dar es Salaam"
        s.tagline_sw = "Tunaimba kwa Utukufu wa Mungu"
        s.tagline_en = "Singing for the Glory of God"
        s.founded_year = 1975
        s.po_box = "S.L.P 77326, Dar es Salaam, Tanzania"
        s.phone = "+255 700 000 000"
        s.email = "info@kwayastefanoshahidi.or.tz"
        s.whatsapp = "+255 700 000 000"
        s.facebook_url = "https://facebook.com"
        s.instagram_url = "https://instagram.com"
        s.youtube_url = "https://youtube.com"
        self.attach_file(s.logo, "images/logo.jpg")
        self.attach_file(s.choir_photo, "images/choir-photo.jpg")
        self.attach_file(s.registration_form_pdf, "documents/fomu-ya-usajili-mwanakwaya.pdf")
        s.save()
        self.stdout.write("Site settings seeded.")

    def seed_about_page(self):
        a = models.AboutPage.load()
        a.intro_sw = (
            "Kwaya ya Mt. Stefano Shahidi ni familia ya waimbaji wa Parokia ya Kipawa, iliyoanzishwa "
            "mwaka 1975 kwa lengo la kuongoza ibada kwa nyimbo na kuimarisha imani ya waumini kupitia "
            "muziki wa kiliturujia. Kwa zaidi ya miaka hamsini, kwaya imeendelea kutumikia Kanisa kwa "
            "moyo wa unyenyekevu, umoja na shauku ya kumtukuza Mungu."
        )
        a.intro_en = (
            "The St. Stefano the Martyr Choir is a family of singers from Kipawa Parish, founded in 1975 "
            "to lead worship through song and deepen the faith of the congregation through liturgical "
            "music. For more than fifty years, the choir has continued to serve the Church with humility, "
            "unity, and a shared passion for glorifying God."
        )
        a.history_sw = (
            "Kwaya ya Mt. Stefano Shahidi ilianzishwa mwaka 1975 katika Parokia ya Kipawa, Jimbo Kuu la "
            "Dar es Salaam, ikiwa na lengo la kutoa huduma ya muziki wa kiliturujia wakati wa Misa "
            "Takatifu na matukio mengine ya Kanisa. Tangu kuanzishwa kwake, kwaya imepitia vizazi kadhaa "
            "vya wanakwaya, ikiendelea kukua kiidadi na kiubora wa huduma. Jina la kwaya linaenzi Mt. "
            "Stefano, Shahidi wa kwanza wa Kanisa, akiwa mfano wa uaminifu na moyo wa kujitoa. Leo hii, "
            "kwaya inaendelea kutumikia kwa kuandaa nyimbo za matukio maalum, kushiriki ziara za kiimbaji "
            "ndani na nje ya Jimbo, na kuendesha miradi mbalimbali ya maendeleo ya huduma yake."
        )
        a.history_en = (
            "The St. Stefano the Martyr Choir was founded in 1975 at Kipawa Parish, Archdiocese of Dar es "
            "Salaam, with the purpose of providing liturgical music ministry during Holy Mass and other "
            "church occasions. Since its founding, the choir has seen several generations of members, "
            "growing in both number and quality of service. The choir's name honors St. Stefano, the "
            "Church's first martyr, a model of faithfulness and dedication. Today the choir continues to "
            "serve by preparing music for special occasions, taking part in singing tours within and "
            "beyond the diocese, and running various projects to develop its ministry."
        )
        a.vision_sw = (
            "Kuwa kwaya ya mfano Jimboni, inayotambulika kwa ubora wa huduma ya muziki wa kiliturujia na "
            "umoja wa kiroho miongoni mwa wanakwaya."
        )
        a.vision_en = (
            "To be a model choir within the diocese, recognized for the excellence of its liturgical "
            "music ministry and the spiritual unity of its members."
        )
        a.mission_sw = (
            "Kuongoza ibada kwa nyimbo za kiliturujia kwa moyo wa unyenyekevu, kukuza vipaji vya muziki "
            "miongoni mwa vijana na waumini, na kuimarisha imani kupitia huduma endelevu ya muziki."
        )
        a.mission_en = (
            "To lead worship through liturgical song with humility, to nurture musical talent among "
            "youth and the faithful, and to strengthen faith through sustained music ministry."
        )
        a.save()
        self.stdout.write("About page seeded.")

    def seed_calendar(self):
        models.CalendarEvent.objects.all().delete()
        months = [
            ("January", "Januari", "January", 0, [
                (11, "Uapisho wa Viongozi Wapya", "Swearing-in of New Leaders"),
                (18, "Makabidhiano Viongozi Wapya na Walimaliza Muda", "Handover Between New and Outgoing Leaders"),
            ]),
            ("February", "Februari", "February", 1, [
                (1, "Semina ya Uimbaji", "Singing Seminar"),
                (15, "Kikao cha Halmashauri Kuu", "Main Council Meeting"),
                (22, "Mkutano Mkuu wa Kwaya", "Choir General Meeting"),
            ]),
            ("March", "Machi", "March", 2, [
                (None, "Recording 1", "Recording 1"),
                (21, "Semina ya Kiroho na Mafungo 1", "Spiritual Seminar & Retreat 1"),
            ]),
            ("April", "Aprili", "April", 3, [
                (26, "Mtoko wa Furaha", "Joy Excursion"),
            ]),
            ("May", "Mei", "May", 4, [
                (None, "Ziara ya Uimbaji (Ndani ya Jimbo)", "Singing Tour (Within the Diocese)"),
            ]),
            ("June", "Juni", "June", 5, [
                (7, "Fundraising", "Fundraising"),
                (21, "Kikao cha Halmashauri Kuu ya Kwaya", "Choir Main Council Meeting"),
                (28, "Mkutano Mkuu wa Kwaya", "Choir General Meeting"),
            ]),
            ("July", "Julai", "July", 6, [
                (None, "Ziara ya Uimbaji (Nje ya Jimbo)", "Singing Tour (Outside the Diocese)"),
                (None, "Recording 2", "Recording 2"),
            ]),
            ("August", "Agosti", "August", 7, [
                (8, "Hija na Matendo ya Upendo", "Pilgrimage & Acts of Charity"),
            ]),
            ("September", "Septemba", "September", 8, [
                (None, "Ziara ya Uimbaji (Ndani ya Jimbo)", "Singing Tour (Within the Diocese)"),
            ]),
            ("October", "Oktoba", "October", 9, [
                (18, "Kikao cha Halmashauri Kuu ya Kwaya", "Choir Main Council Meeting"),
                (25, "Mkutano Mkuu wa Kwaya", "Choir General Meeting"),
            ]),
            ("November", "Novemba", "November", 10, [
                (None, "Recording 3", "Recording 3"),
            ]),
            ("December", "Desemba", "December", 11, [
                (5, "Semina ya Kiroho na Mafungo 2", "Spiritual Seminar & Retreat 2"),
                (26, "Stefano Day", "Stefano Day"),
            ]),
        ]
        for _, month_sw, month_en, idx, events in months:
            for date, title_sw, title_en in events:
                models.CalendarEvent.objects.create(
                    year=2026,
                    month_index=idx,
                    month_name_sw=month_sw,
                    month_name_en=month_en,
                    date=date,
                    title_sw=title_sw,
                    title_en=title_en,
                )
        self.stdout.write("Calendar events seeded.")

    def seed_committees(self):
        models.Committee.objects.all().delete()
        data = [
            ("utendaji", "Kamati ya Utendaji", "Executive Committee",
             "Kamati inayosimamia shughuli za kila siku za kwaya na kutekeleza maamuzi ya Halmashauri Kuu.",
             "Oversees the choir's day-to-day activities and carries out decisions of the Main Council.",
             [
                 ("Anold Mushi", "Mwenyekiti", "Chairperson"),
                 ("Grace Kileo", "Makamu Mwenyekiti", "Vice Chairperson"),
                 ("Baraka Ndosi", "Katibu", "Secretary"),
                 ("Consolata Mbwana", "Mtunza Fedha", "Treasurer"),
             ]),
            ("halmashauri", "Halmashauri", "Council",
             "Chombo cha juu cha maamuzi kinachoongoza dira, sera na mipango ya muda mrefu ya kwaya.",
             "The choir's senior decision-making body, guiding vision, policy, and long-term planning.",
             [
                 ("Fr. Method Komba", "Mchungaji wa Kiroho", "Spiritual Director"),
                 ("Anold Mushi", "Mwenyekiti", "Chairperson"),
                 ("Edina Lyimo", "Mjumbe", "Member"),
                 ("Method Shayo", "Mjumbe", "Member"),
             ]),
            ("fedha", "Kamati ya Fedha, Uchumi na Mipango", "Finance, Economy & Planning Committee",
             "Inasimamia mapato, matumizi, miradi ya kiuchumi na mipango ya maendeleo ya kwaya.",
             "Manages income, expenditure, income-generating projects, and the choir's development plans.",
             [
                 ("Consolata Mbwana", "Mwenyekiti", "Chairperson"),
                 ("Ombeni Massawe", "Katibu", "Secretary"),
                 ("Rehema Kessy", "Mjumbe", "Member"),
             ]),
            ("maadili", "Kamati ya Maadili", "Ethics Committee",
             "Inalinda nidhamu, maadili mema na utu wema miongoni mwa wanakwaya.",
             "Safeguards discipline, good conduct, and moral integrity among choir members.",
             [
                 ("Method Shayo", "Mwenyekiti", "Chairperson"),
                 ("Fausta Mrema", "Mjumbe", "Member"),
             ]),
            ("muziki", "Kamati ya Muziki na Litrujia", "Music & Liturgy Committee",
             "Inapanga nyimbo, mazoezi na huduma ya muziki kulingana na kalenda ya kiliturujia.",
             "Plans songs, rehearsals, and musical ministry in line with the liturgical calendar.",
             [
                 ("Edina Lyimo", "Kiongozi wa Muziki", "Music Director"),
                 ("Baraka Ndosi", "Msaidizi wa Muziki", "Assistant Music Director"),
                 ("Grace Kileo", "Mjumbe", "Member"),
             ]),
            ("mavazi", "Kamati ya Mavazi", "Attire Committee",
             "Inashughulikia sare za kwaya, ununuzi na utunzaji wa mavazi ya matukio maalum.",
             "Handles choir uniforms, procurement, and the upkeep of attire for special occasions.",
             [
                 ("Rehema Kessy", "Mwenyekiti", "Chairperson"),
                 ("Fausta Mrema", "Mjumbe", "Member"),
             ]),
        ]
        for order, (slug, name_sw, name_en, desc_sw, desc_en, members) in enumerate(data):
            committee = models.Committee.objects.create(
                slug=slug, name_sw=name_sw, name_en=name_en,
                description_sw=desc_sw, description_en=desc_en, order=order,
            )
            for m_order, (name, role_sw, role_en) in enumerate(members):
                models.CommitteeMember.objects.create(
                    committee=committee, name=name, role_sw=role_sw, role_en=role_en, order=m_order,
                )
        self.stdout.write("Committees seeded.")

    def seed_members(self):
        models.ChoirMember.objects.all().delete()
        roster = [
            ("Grace Kileo", "soprano", 2016), ("Edina Lyimo", "soprano", 2014),
            ("Consolata Mbwana", "soprano", 2018), ("Fausta Mrema", "soprano", 2020),
            ("Rehema Kessy", "alto", 2015), ("Neema Shirima", "alto", 2019),
            ("Doroth Massoud", "alto", 2021),
            ("Anold Mushi", "tenor", 2012), ("Baraka Ndosi", "tenor", 2017),
            ("Method Shayo", "tenor", 2013),
            ("Ombeni Massawe", "bass", 2011), ("Deogratius Komba", "bass", 2016),
            ("Yustin Mwakalinga", "bass", 2022),
        ]
        for name, part, year in roster:
            models.ChoirMember.objects.create(name=name, voice_part=part, joined_year=year)
        self.stdout.write("Choir members seeded.")

    def seed_songs(self):
        models.SongCategory.objects.all().delete()
        data = [
            ("mwanzo", "Nyimbo za Mwanzo", "Opening Songs",
             "Nyimbo za kuanza Misa na kukaribisha Umati kwa Ibada.",
             "Songs used to open Mass and welcome the congregation into worship.",
             ["Tumsifu Mungu Wetu", "Njoo Ukae Nasi"]),
            ("kati", "Nyimbo za Kati", "Middle of Mass Songs",
             "Nyimbo zinazoimbwa katikati ya Ibada, kabla na baada ya Neno la Mungu.",
             "Songs sung during the middle portion of Mass, around the Liturgy of the Word.",
             ["Neno Lako Bwana"]),
            ("matoleo", "Nyimbo za Matoleo", "Offertory Songs",
             "Nyimbo za wakati wa kutoa sadaka na kuandaa Meza ya Bwana.",
             "Songs for the offertory procession and preparation of the altar.",
             ["Tunakuletea Bwana"]),
            ("komunio", "Nyimbo za Komunio", "Communion Songs",
             "Nyimbo za wakati wa kupokea Ekaristi Takatifu.",
             "Songs sung during the reception of Holy Communion.",
             ["Karibu Yesu Karibu", "Mkate wa Uzima"]),
            ("christmas", "Nyimbo za Christmass", "Christmas Songs",
             "Nyimbo za sikukuu ya kuzaliwa kwa Bwana wetu Yesu Kristo.",
             "Songs for the celebration of the birth of our Lord Jesus Christ.",
             ["Leo Kristo Amezaliwa"]),
            ("pasaka", "Nyimbo za Pasaka", "Easter Songs",
             "Nyimbo za furaha ya ufufuko wa Bwana wetu Yesu Kristo.",
             "Joyful songs celebrating the resurrection of our Lord Jesus Christ.",
             ["Kristo Amefufuka"]),
            ("kwaresma", "Nyimbo za Kwaresma", "Lenten Songs",
             "Nyimbo za toba na maandalizi wakati wa Kwaresima.",
             "Songs of repentance and preparation during the season of Lent.",
             ["Ee Bwana Uturehemu"]),
            ("majilio", "Nyimbo za Majilio", "Advent Songs",
             "Nyimbo za matarajio wakati wa Majilio, kuandaa njia ya Bwana.",
             "Songs of hopeful expectation during Advent, preparing the way of the Lord.",
             ["Njoo Bwana Yesu"]),
            ("bikira-maria", "Nyimbo za Bikira Maria", "Marian Songs",
             "Nyimbo za heshima kwa Bikira Maria, Mama wa Mungu.",
             "Songs honoring the Virgin Mary, Mother of God.",
             ["Salamu Maria"]),
            ("nyinginezo", "Nyimbo Nyinginezo", "Other Songs",
             "Nyimbo nyingine za ibada na matukio maalum ya kwaya.",
             "Other worship songs and songs for special choir occasions.",
             ["Asante Bwana"]),
        ]
        for order, (slug, name_sw, name_en, desc_sw, desc_en, songs) in enumerate(data):
            cat = models.SongCategory.objects.create(
                slug=slug, name_sw=name_sw, name_en=name_en,
                description_sw=desc_sw, description_en=desc_en, order=order,
            )
            for s_order, title in enumerate(songs):
                models.Song.objects.create(category=cat, title=title, youtube_id=None, order=s_order)
        self.stdout.write("Song categories seeded.")

    def seed_news(self):
        models.NewsItem.objects.all().delete()
        data = [
            ("uapisho-viongozi-wapya-2026",
             "Uapisho wa Viongozi Wapya wa Kwaya", "Swearing-in of the Choir's New Leaders",
             "2026-01-11",
             "Kwaya imefanya ibada ya uapisho kwa viongozi wapya waliochaguliwa kuongoza kwa mwaka ujao.",
             "The choir held a swearing-in ceremony for the new leaders elected to serve in the coming year.",
             "Jumapili tarehe 11 Januari, kwaya ilifanya ibada maalum ya uapisho kwa viongozi wapya "
             "waliochaguliwa na wanakwaya. Ibada hii iliambatana na sala na baraka kutoka kwa Mchungaji "
             "wa Kiroho, ikifuatiwa na makabidhiano rasmi kutoka kwa viongozi walimaliza muda wao.",
             "On Sunday, January 11th, the choir held a special swearing-in service for the new leaders "
             "elected by choir members. The ceremony included prayers and a blessing from the Spiritual "
             "Director, followed by the formal handover from the outgoing leadership."),
            ("semina-ya-uimbaji-2026",
             "Semina ya Uimbaji Yafanyika", "Singing Seminar Held",
             "2026-02-01",
             "Wanakwaya wamepata mafunzo ya uimbaji na ustadi wa sauti kuboresha huduma ya muziki.",
             "Choir members received training in singing technique and vocal skills to strengthen the music ministry.",
             "Semina ya uimbaji ilifanyika ikiwashirikisha wanakwaya wote, ikilenga kuboresha ustadi wa "
             "sauti, upumuaji na uelewano wa vipande vya muziki vinavyotumika Kanisani.",
             "The singing seminar brought together all choir members, focusing on improving vocal "
             "technique, breathing, and understanding of the musical pieces used in church."),
            ("mtoko-wa-furaha-2026",
             "Mtoko wa Furaha wa Kwaya", "Choir Joy Excursion",
             "2026-04-26",
             "Wanakwaya walifurahia siku ya mapumziko na burudani pamoja kama familia moja.",
             "Choir members enjoyed a day of rest and recreation together as one family.",
             "Kwaya ilifanya mtoko wa furaha uliojumuisha michezo, chakula na muda wa kujengana kiroho "
             "na kijamii miongoni mwa wanakwaya na familia zao.",
             "The choir held a joy excursion that included games, food, and time to build spiritual and "
             "social bonds among members and their families."),
        ]
        for slug, title_sw, title_en, date, excerpt_sw, excerpt_en, body_sw, body_en in data:
            models.NewsItem.objects.create(
                slug=slug, title_sw=title_sw, title_en=title_en, date=date,
                excerpt_sw=excerpt_sw, excerpt_en=excerpt_en, body_sw=body_sw, body_en=body_en,
            )
        self.stdout.write("News items seeded.")

    def seed_homilies(self):
        models.Homily.objects.all().delete()
        data = [
            ("jumapili-ya-kwanza-2026",
             "Jumapili ya Kwanza ya Mwaka", "First Sunday of the Year",
             "2026-01-04", "Yohana 1:1-18", "John 1:1-18",
             "Neno alifanyika mwili akakaa kwetu — tafakari juu ya kuzaliwa upya kwa imani mwanzoni mwa mwaka.",
             "The Word became flesh and dwelt among us — a reflection on renewing our faith at the start of the year."),
            ("jumapili-ya-kwaresma-2026",
             "Jumapili ya Kwanza ya Kwaresma", "First Sunday of Lent",
             "2026-02-22", "Mathayo 4:1-11", "Matthew 4:1-11",
             "Yesu anajaribiwa jangwani — tunaalikwa kutafakari kuhusu majaribu na sala katika safari yetu ya Kwaresima.",
             "Jesus is tempted in the desert — an invitation to reflect on temptation and prayer during our Lenten journey."),
        ]
        for slug, title_sw, title_en, date, reading_sw, reading_en, summary_sw, summary_en in data:
            models.Homily.objects.create(
                slug=slug, title_sw=title_sw, title_en=title_en, date=date,
                reading_sw=reading_sw, reading_en=reading_en,
                summary_sw=summary_sw, summary_en=summary_en,
            )
        self.stdout.write("Homilies seeded.")

    def seed_projects(self):
        models.ShopItem.objects.all().delete()
        data = [
            ("T-Shirt ya Kwaya", "Choir T-Shirt", "TZS 20,000",
             "T-Shirt yenye nembo ya Kwaya ya Mt. Stefano Shahidi, ipatikane kwa saizi mbalimbali.",
             "T-Shirt featuring the St. Stefano Shahidi Choir emblem, available in various sizes."),
            ("CD ya Nyimbo za Kwaya", "Choir Songs CD", "TZS 10,000",
             "Mkusanyiko wa nyimbo teule zilizorekodiwa na kwaya.",
             "A collection of selected songs recorded by the choir."),
            ("Kalenda ya Kwaya 2026", "2026 Choir Calendar", "TZS 5,000",
             "Kalenda rasmi ya matukio ya kwaya kwa mwaka 2026.",
             "The official 2026 choir events calendar."),
        ]
        for order, (name_sw, name_en, price, desc_sw, desc_en) in enumerate(data):
            models.ShopItem.objects.create(
                name_sw=name_sw, name_en=name_en, price=price,
                description_sw=desc_sw, description_en=desc_en, order=order,
            )

        k = models.KinandaProject.load()
        k.title_sw = "Mradi wa Kinanda"
        k.title_en = "Instrument (Kinanda) Fund"
        k.goal_amount = "TZS 8,000,000"
        k.raised_amount = "TZS 3,200,000"
        k.description_sw = (
            "Kwaya inaendesha mradi wa kuchangisha fedha kwa ajili ya kununua kinanda (keyboard) kipya "
            "ili kuboresha huduma ya muziki Kanisani."
        )
        k.description_en = (
            "The choir is running a fundraising project to purchase a new keyboard (kinanda) to "
            "strengthen its music ministry at church."
        )
        k.save()
        self.stdout.write("Projects seeded.")

    def seed_constitution(self):
        models.ConstitutionArticle.objects.all().delete()
        data = [
            ("Ibara ya 1: Jina na Makazi", "Article 1: Name and Domicile",
             "Chombo hiki kitaitwa Kwaya ya Mt. Stefano Shahidi (SSK), kikiwa na makazi yake katika "
             "Parokia ya Kipawa, Jimbo Kuu la Dar es Salaam.",
             "This body shall be known as the St. Stefano the Martyr Choir (SSK), domiciled at Kipawa "
             "Parish, Archdiocese of Dar es Salaam."),
            ("Ibara ya 2: Dhumuni", "Article 2: Purpose",
             "Kuimba na kuongoza ibada kwa nyimbo, kukuza vipaji vya muziki miongoni mwa waumini, na "
             "kuimarisha imani kupitia huduma ya muziki wa kiliturujia.",
             "To lead worship through song, nurture musical talent among the faithful, and strengthen "
             "faith through liturgical music ministry."),
            ("Ibara ya 3: Uanachama", "Article 3: Membership",
             "Uanachama uko wazi kwa waumini wote wa Parokia ya Kipawa wenye nia ya kutumikia kwa njia "
             "ya muziki na wanaozingatia maadili ya Kikristo.",
             "Membership is open to all faithful of Kipawa Parish who desire to serve through music and "
             "who uphold Christian values."),
            ("Ibara ya 4: Uongozi", "Article 4: Leadership",
             "Kwaya inaongozwa na Halmashauri Kuu na kusimamiwa kiutendaji na Kamati ya Utendaji, "
             "ikisaidiwa na kamati za idara mbalimbali.",
             "The choir is governed by the Main Council and administered day-to-day by the Executive "
             "Committee, assisted by various departmental committees."),
            ("Ibara ya 5: Nidhamu na Maadili", "Article 5: Discipline and Conduct",
             "Kila mwanakwaya anatakiwa kuzingatia nidhamu, uwajibikaji na maadili mema wakati wote wa "
             "huduma na shughuli za kwaya.",
             "Every choir member is expected to uphold discipline, accountability, and good conduct at "
             "all times during ministry and choir activities."),
        ]
        for order, (heading_sw, heading_en, body_sw, body_en) in enumerate(data):
            models.ConstitutionArticle.objects.create(
                heading_sw=heading_sw, heading_en=heading_en,
                body_sw=body_sw, body_en=body_en, order=order,
            )
        self.stdout.write("Constitution articles seeded.")

    def seed_gallery(self):
        models.Album.objects.all().delete()
        models.GalleryImage.objects.all().delete()

        albums_data = [
            ("matukio-2025", "Matukio ya Mwaka 2025", "2025 Highlights",
             "Mkusanyiko wa picha na kumbukumbu za matukio muhimu ya kwaya mwaka 2025.",
             "A collection of photos and memories from the choir's key events in 2025."),
            ("stefano-day", "Stefano Day", "Stefano Day",
             "Kumbukumbu za sherehe ya kila mwaka ya Stefano Day, tarehe 26 Desemba.",
             "Memories from the annual Stefano Day celebration held every December 26th."),
        ]
        albums = []
        for order, (slug, title_sw, title_en, desc_sw, desc_en) in enumerate(albums_data):
            albums.append(models.Album.objects.create(
                slug=slug, title_sw=title_sw, title_en=title_en,
                description_sw=desc_sw, description_en=desc_en, order=order,
            ))

        images_data = [
            ("images/choir-photo.jpg", "Wanakwaya baada ya Ibada", "Choir members after Mass"),
            ("images/logo.jpg", "Nembo ya Kwaya", "Choir Emblem"),
        ]
        for order, (rel_path, caption_sw, caption_en) in enumerate(images_data):
            img = models.GalleryImage(
                caption_sw=caption_sw, caption_en=caption_en,
                album=albums[order % len(albums)], order=order,
            )
            self.attach_file(img.image, rel_path)
            img.save()
        self.stdout.write("Gallery seeded.")
