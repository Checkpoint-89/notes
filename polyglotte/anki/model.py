import hashlib

from pydantic import BaseModel, Field, computed_field


class Exemple(BaseModel):
    de: str = Field(description="Phrase exemple en allemand.")
    fr: str = Field(description="Traduction française de la phrase exemple.")


class VocabEntry(BaseModel):
    mot_de: str = Field(
        description=(
            "Mot allemand avec conventions dictionnaire : "
            "nom → article défini + pluriel abrégé (ex. 'der Hund, -e') ; "
            "verbe → infinitif + prétérit + auxiliaire si ≠ haben "
            "(ex. 'gehen (ging, ist gegangen)') ; "
            "adjectif/adverbe → forme de base."
        )
    )
    traduction_fr: str = Field(description="Traduction française du mot.")
    exemples: list[Exemple] = Field(description="Liste d'exemples (phrase allemande + traduction française).")
    page: int | None = Field(default=None, description="Numéro de page dans le document source (None si inconnu).")

    @computed_field
    @property
    def categorie(self) -> str | None:
        """Catégorie calculée après récupération du modèle."""
        return None

    @computed_field
    @property
    def id(self) -> str:
        """Identifiant stable : hash MD5 du mot allemand et du premier exemple allemand."""
        exemple_de = self.exemples[0].de.strip().lower() if self.exemples else ""
        key = f"{self.mot_de.strip().lower()}{exemple_de}"
        return hashlib.md5(key.encode()).hexdigest()[:12]


class Vocabulary(BaseModel):
    mots: list[VocabEntry] = Field(description="Liste des entrées de vocabulaire extraites.")
