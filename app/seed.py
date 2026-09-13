from datetime import date

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Event, GalleryPhoto, Member


def seed() -> None:
    with SessionLocal() as db:
        if db.scalar(select(Event.id).limit(1)) is not None:
            print("Seed déjà effectué.")
            return

        db.add_all(
            [
                Event(
                    title="Fête de la Saint-André",
                    date=date(2026, 9, 20),
                    start_time="10:30",
                    end_time="12:00",
                    venue="Place de la Mairie",
                    city="Doissin",
                    description="Aubade du matin suivie d'un défilé jusqu'à la salle des fêtes.",
                    category="passage",
                    is_free=True,
                ),
                Event(
                    title="Concert d'automne",
                    date=date(2026, 10, 17),
                    start_time="20:30",
                    end_time="22:30",
                    venue="Salle des fêtes",
                    city="Doissin",
                    description="Marches, valses et airs traditionnels du Dauphiné.",
                    category="concert",
                    is_free=True,
                ),
            ]
        )
        db.add_all(
            [
                Member(
                    first_name="Camille",
                    last_name="Ferrand",
                    instrument="Direction",
                    section="direction",
                    joined_year=2005,
                    role="Chef de clique",
                ),
                Member(
                    first_name="Élise",
                    last_name="Morel",
                    instrument="Fifre",
                    section="fifres",
                    joined_year=2015,
                ),
                Member(
                    first_name="Sophie",
                    last_name="Barbier",
                    instrument="Caisse claire",
                    section="tambours",
                    joined_year=2010,
                ),
                Member(
                    first_name="Amandine",
                    last_name="Roux",
                    instrument="Clairon",
                    section="clairons",
                    joined_year=2011,
                ),
            ]
        )
        db.add(
            GalleryPhoto(
                src="https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=900&q=80",
                alt="La clique en formation sur la place du village",
                caption="Aubade du dimanche matin",
                year=2025,
                place="Doissin",
            )
        )
        db.commit()
        print("Données de démonstration insérées.")


if __name__ == "__main__":
    seed()
