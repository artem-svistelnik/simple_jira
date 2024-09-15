class BaseService:
    def set_service_db_session(self, db_session):
        self._s = db_session
        for name, repo in vars(self).items():
            if "_repo" in name:
                repo.set_session(db_session)
