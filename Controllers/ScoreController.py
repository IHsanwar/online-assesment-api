from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Models import Score
from Models.Score import Score  # Import Score correctly
from Models.Connection import SessionLocal
from datetime import date


class ScoreController:
    def __init__(self):
        self.session = SessionLocal()

    def add_score(self, key_id, evidence_id, score_value):
        new_score = Score(
            key_id=key_id,
            evidence_id=evidence_id,
            score=score_value,
            scoring_date=date.today()
        )
        self.session.add(new_score)
        self.session.commit()
        return new_score

    def get_scores(self):
        return self.session.query(Score).all()

    def get_score_by_key_and_evidence(self, key_id, evidence_id):
        return self.session.query(Score).filter_by(key_id=key_id, evidence_id=evidence_id).first()

    def update_score(self, key_id, evidence_id, score_value):
        score = self.get_score_by_key_and_evidence(key_id, evidence_id)
        if score:
            score.score = score_value
            self.session.commit()
        return score

    def delete_score(self, key_id, evidence_id):
        score = self.get_score_by_key_and_evidence(key_id, evidence_id)
        if score:
            self.session.delete(score)
            self.session.commit()
        return score
