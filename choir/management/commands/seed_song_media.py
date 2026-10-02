from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from choir import models

# Pre-generated locally (not shipped in the repo) and placed directly under
# the bind-mounted media volume — see conversation notes. Safe to re-run:
# only updates specific existing Song rows by title, never deletes anything
# (unlike `seed_data`, which rebuilds song categories from scratch).
SEED_ASSETS = Path(__file__).resolve().parents[3] / "media" / "_seed_assets"

# Real, public, embeddable Tanzanian/Catholic choir performances (verified
# via YouTube's oEmbed API) used as demo content for the "plays from
# YouTube" path — not recordings by this choir.
YOUTUBE_DEMOS = {
    "Njoo Ukae Nasi": "uuMNMHGoVTk",
    "Neno Lako Bwana": "Dnz3UEYD1I0",
    "Karibu Yesu Karibu": "CNH9FhSzfOg",
}

# Locally-generated, original text-to-speech placeholder clips (not
# copyrighted music) used as demo content for the "downloadable audio
# file" path.
AUDIO_DEMOS = {
    "Tumsifu Mungu Wetu": "demo-tumsifu.m4a",
    "Mkate wa Uzima": "demo-mkate.m4a",
}


class Command(BaseCommand):
    help = "Attach demo YouTube IDs / downloadable audio files to a few existing songs."

    def handle(self, *args, **options):
        for title, youtube_id in YOUTUBE_DEMOS.items():
            updated = models.Song.objects.filter(title=title).update(youtube_id=youtube_id)
            self.stdout.write(f"{title}: youtube_id set on {updated} row(s).")

        for title, filename in AUDIO_DEMOS.items():
            song = models.Song.objects.filter(title=title).first()
            if not song:
                self.stdout.write(self.style.WARNING(f"{title}: no matching song found, skipped."))
                continue
            path = SEED_ASSETS / filename
            if not path.exists():
                self.stdout.write(self.style.WARNING(f"{title}: {path} not found, skipped."))
                continue
            with open(path, "rb") as f:
                song.audio_file.save(filename, File(f), save=True)
            self.stdout.write(f"{title}: audio_file attached.")

        self.stdout.write(self.style.SUCCESS("Song media seeded."))
