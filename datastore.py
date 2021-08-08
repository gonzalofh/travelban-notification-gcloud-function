from google.cloud import datastore

class DataStore:

    def __init__(self):
        self.__client = datastore.Client()

    def get_context(self):
        key = self.__client.key('travelban', 'travelban-context')    
        return self.__client.get(key)

    def update_context(self, context, last_update):
        context.update({'last_updated_at': last_update})
        self.__client.put(context)

    def get_recipients(self):
        query = self.__client.query(kind='travelban-sub-emails')    
        results = query.fetch()
        recipients = [*map(lambda x: x['email'], results)]
        return recipients