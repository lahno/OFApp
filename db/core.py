from .database import Base, sync_engine


class SyncCore:
    @staticmethod
    def init_db(drop=False, log_echo=False):
        sync_engine.echo = log_echo

        if drop:
            Base.metadata.drop_all(sync_engine)

        Base.metadata.create_all(sync_engine)
        sync_engine.echo = log_echo is False
