from sqlalchemy.orm import sessionmaker
from Models.Evidence import *
from Models.Connection import SessionLocal
from datetime import date

Session = sessionmaker(bind=engine)
session = Session()

class evidenceController:
    def __init__(self):
        self.session = session

    def get_evidences():
        evidences = session.query(Evidence).all()
        return [{
            'id': e.id,
            'indicator_id': e.indicator_id,
            'evidence': e.evidence,
            'scored_by': e.scored_by,
            'justification': e.justification
        } for e in evidences]

    def get_evidence(evidence_id):
        evidence = session.query(Evidence).filter_by(id=evidence_id).first()
        if not evidence:
            return None
        return {
            'id': evidence.id,
            'indicator_id': evidence.indicator_id,
            'evidence': evidence.evidence,
            'scored_by': evidence.scored_by,
            'justification': evidence.justification
        }


    def create_evidence(data):
        new_evidence = Evidence(
            indicator_id=data.get('indicator_id'),
            evidence=data.get('evidence'),
            scored_by=data.get('scored_by'),
            justification=data.get('justification')
        )
        session.add(new_evidence)
        session.commit()
        return {'message': 'Evidence created successfully'}

    def update_evidence(id, data):
        evidence = session.query(Evidence).filter_by(id=id).first()
        if not evidence:
            return None
        
        evidence.indicator_id = data.get('indicator_id', evidence.indicator_id)
        evidence.evidence = data.get('evidence', evidence.evidence)
        evidence.scored_by = data.get('scored_by', evidence.scored_by)
        evidence.justification = data.get('justification', evidence.justification)
        session.commit()
        
        return {'message': 'Evidence updated successfully'}

    def delete_evidence(id):
        evidence = session.query(Evidence).filter_by(id=id).first()
        if not evidence:
            return None
        session.delete(evidence)
        session.commit()
        return {'message': 'Evidence deleted successfully'}
