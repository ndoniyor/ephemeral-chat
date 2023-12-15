class ConnectionManager:
    def get_conversation(self, conversation_id):
        raise NotImplementedError

    def create_conversation(self, conversation_id):
        raise NotImplementedError

    def delete_conversation(self, conversation_id):
        raise NotImplementedError

    def get_or_create_conversation(self, conversation_id):
        raise NotImplementedError
