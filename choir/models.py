from django.db import models


class SingletonModel(models.Model):
    """Base for models that should only ever have one row (id=1)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    short_name = models.CharField(max_length=20, default="SSK")
    name_sw = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    parish_sw = models.CharField(max_length=200)
    parish_en = models.CharField(max_length=200)
    diocese_sw = models.CharField(max_length=200)
    diocese_en = models.CharField(max_length=200)
    tagline_sw = models.CharField(max_length=200)
    tagline_en = models.CharField(max_length=200)
    founded_year = models.PositiveIntegerField(default=1975)
    po_box = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    choir_photo = models.ImageField(upload_to="site/", blank=True, null=True)
    registration_form_pdf = models.FileField(upload_to="documents/", blank=True, null=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.name_en or "Site settings"


class AboutPage(SingletonModel):
    intro_sw = models.TextField(blank=True)
    intro_en = models.TextField(blank=True)
    history_sw = models.TextField(blank=True)
    history_en = models.TextField(blank=True)
    vision_sw = models.TextField(blank=True)
    vision_en = models.TextField(blank=True)
    mission_sw = models.TextField(blank=True)
    mission_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "About page"
        verbose_name_plural = "About page"

    def __str__(self):
        return "About page content"


class CalendarEvent(models.Model):
    year = models.PositiveIntegerField(default=2026)
    month_index = models.PositiveSmallIntegerField(help_text="0 = January … 11 = December")
    month_name_sw = models.CharField(max_length=20)
    month_name_en = models.CharField(max_length=20)
    date = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Day of month, blank if undated")
    title_sw = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)

    class Meta:
        ordering = ["year", "month_index", "date"]

    def __str__(self):
        return f"{self.month_name_en} {self.date or ''}: {self.title_en}".strip()


class Committee(models.Model):
    slug = models.SlugField(unique=True)
    name_sw = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    description_sw = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name_en"]

    def __str__(self):
        return self.name_en


class CommitteeMember(models.Model):
    committee = models.ForeignKey(Committee, related_name="members", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    role_sw = models.CharField(max_length=200)
    role_en = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["committee", "order"]

    def __str__(self):
        return f"{self.name} ({self.committee.name_en})"


class ChoirMember(models.Model):
    """Mirrors "Fomu ya Usajili wa Mwanakwaya" (the choir's paper registration
    form) section by section, so the dashboard can capture everything the
    form does instead of just name/voice/joined-year."""

    class VoicePart(models.TextChoices):
        SOPRANO = "soprano", "Soprano"
        ALTO = "alto", "Alto"
        TENOR = "tenor", "Tenor"
        BASS = "bass", "Bass"

    class Gender(models.TextChoices):
        FEMALE = "F", "Kike"
        MALE = "M", "Kiume"

    name = models.CharField(max_length=200)
    voice_part = models.CharField(max_length=10, choices=VoicePart.choices)
    joined_year = models.PositiveIntegerField()

    # A: Taarifa Binafsi (Personal information)
    birth_day = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_month = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    community = models.CharField("Jumuiya", max_length=200, blank=True)
    parish = models.CharField("Parokia", max_length=200, blank=True)
    address = models.CharField("Anwani ya makazi", max_length=255, blank=True)
    phone = models.CharField("Namba ya simu", max_length=50, blank=True)

    # B: Taarifa za Kiroho (Spiritual information)
    baptized = models.BooleanField("Ubatizo", default=False)
    communion = models.BooleanField("Komunyo", default=False)
    confirmed = models.BooleanField("Kipaimara", default=False)
    married = models.BooleanField("Ndoa", default=False)
    spiritual_gift = models.CharField("Huduma ya kiroho/karama", max_length=255, blank=True)

    # C: Taarifa ya Utume wa Kwaya (Choir ministry information)
    other_talent = models.CharField("Kipaji/karama nyingine", max_length=255, blank=True)
    plays_instrument = models.BooleanField("Upigaji wa ala za muziki", default=False)
    instrument_name = models.CharField(max_length=200, blank=True)

    # D: Masharti na Maazimio (Terms and registration processing)
    agreed_to_constitution = models.BooleanField(default=False)
    registration_date = models.DateField(null=True, blank=True)
    received_by = models.CharField("Imepokelewa na", max_length=200, blank=True)
    received_by_title = models.CharField("Cheo", max_length=200, blank=True)
    leader_comments = models.TextField("Maoni/Maamuzi", blank=True)
    processed_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["voice_part", "name"]

    def __str__(self):
        return self.name


class SongCategory(models.Model):
    slug = models.SlugField(unique=True)
    name_sw = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    description_sw = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name_en"]
        verbose_name_plural = "Song categories"

    def __str__(self):
        return self.name_en


class Song(models.Model):
    category = models.ForeignKey(SongCategory, related_name="songs", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=32, blank=True, null=True)
    lyrics = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category", "order"]

    def __str__(self):
        return self.title


class NewsItem(models.Model):
    slug = models.SlugField(unique=True)
    title_sw = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    date = models.DateField()
    excerpt_sw = models.TextField()
    excerpt_en = models.TextField()
    body_sw = models.TextField()
    body_en = models.TextField()

    class Meta:
        ordering = ["-date"]
        verbose_name = "News item"

    def __str__(self):
        return self.title_en


class Homily(models.Model):
    slug = models.SlugField(unique=True)
    title_sw = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    date = models.DateField()
    reading_sw = models.CharField(max_length=255)
    reading_en = models.CharField(max_length=255)
    summary_sw = models.TextField()
    summary_en = models.TextField()

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Homilies"

    def __str__(self):
        return self.title_en


class ShopItem(models.Model):
    name_sw = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    price = models.CharField(max_length=50, help_text="e.g. TZS 20,000")
    description_sw = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name_en


class KinandaProject(SingletonModel):
    title_sw = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    goal_amount = models.CharField(max_length=50, help_text="e.g. TZS 8,000,000")
    raised_amount = models.CharField(max_length=50, help_text="e.g. TZS 3,200,000")
    description_sw = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "Kinanda project"
        verbose_name_plural = "Kinanda project"

    def __str__(self):
        return self.title_en


class ConstitutionArticle(models.Model):
    heading_sw = models.CharField(max_length=255)
    heading_en = models.CharField(max_length=255)
    body_sw = models.TextField()
    body_en = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.heading_en


class Album(models.Model):
    slug = models.SlugField(unique=True)
    title_sw = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    description_sw = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title_en


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery/")
    caption_sw = models.CharField(max_length=255, blank=True)
    caption_en = models.CharField(max_length=255, blank=True)
    album = models.ForeignKey(
        Album, related_name="images", on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.caption_en or f"Image {self.pk}"
