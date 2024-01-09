import pickle
from application.models.preferences import Preference


class PreferencesDB:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def get_all_preferences(self):
        with self.session_manager.session_scope() as session:
            preferences = session.query(Preference).all()
            return {preference.name: self.deserialize_preference(preference) for preference in preferences}

    def get_preference(self, name, default_value=None):
        with self.session_manager.session_scope() as session:
            preference = session.query(Preference).filter_by(name=name).first()
            if preference:
                return self.deserialize_preference(preference)
            else:
                return default_value

    def set_preference(self, name, value):
        serialized_value = pickle.dumps(value)
        data_type = type(value).__name__
        with self.session_manager.session_scope() as session:
            preference = session.query(Preference).filter_by(name=name).first()
            if preference:
                preference.value = serialized_value
                preference.data_type = data_type
            else:
                new_preference = Preference(name=name, value=serialized_value, data_type=data_type)
                session.add(new_preference)

    def delete_preference(self, name):
        with self.session_manager.session_scope() as session:
            preference = session.query(Preference).filter_by(name=name).first()
            if preference:
                session.delete(preference)

    def delete_all_preferences(self):
        with self.session_manager.session_scope() as session:
            session.query(Preference).delete()

    @staticmethod
    def deserialize_preference(preference):
        return pickle.loads(preference.value)
