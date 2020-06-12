import xmlrpc.client

class OdooHelper:
    
    def __init__(self, app):
        self.app = app
        self.url = 'http://' + app.config['RDM_SERVER'] + ':' + app.config['RDM_PORT']
        
    def _get_uid(self):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            uid = common.authenticate(self.app.config['RDM_DB_NAME'], self.app.config['RDM_APP_EMAIL'], self.app.config['RDM_APP_PASSWORD'], {})
            if (uid == False):
                return {'error': True, 'message': 'Access Denied', 'uid': False}
            else:
                return {'error': False, 'message': '', 'uid': uid}
        except Exception as e:
            return {'error': True, 'message': str(e), 'uid': False}

    def get_pagination(self, model, fields, offset, limit):
        result = self._get_uid()
        if result['error']:
            return result
        try:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'], model, 'search',[[['state','=','done']]],  {'offset': offset, 'limit': limit})
            datas =  models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'] ,model, 'read', [ids], {'fields': fields})
            return {'error': False, 'message': '', 'datas': datas}
        except Exception as e:
            return {'error': True, 'message': str(e),}
        
    def get_pagination_search(self, model, fields, search, offset, limit):
        result = self._get_uid()
        if result['error']:
            return result
        try:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'], model, 'search', search, {'offset': offset, 'limit': limit})
            datas =  models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'] ,model, 'read', [ids], {'fields': fields})
            return {'error': False, 'message': '', 'datas': datas}
        except Exception as e:
            return {'error': True, 'message': str(e),}
    
    def get_list(self, model, fields=[]):
        result = self._get_uid()
        if result['error']:
            return result
        try:
            print(result)
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids =  models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'], model, 'search', [[]])
            datas =  models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'],model, 'read', [ids], {'fields': fields})
            return {'error': False, 'message': '', 'datas': datas}
        except Exception as e:
            return {'error': True, 'message': str(e),}

    def get_search(self, model , search, fields):
        result = self._get_uid()
        if not result['error']:
            return result
        try:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'], model, 'search', search)
            datas =  models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'] ,model, 'read', [ids], {'fields': fields})
            return {'error': False, 'message': '', 'datas': datas}
        except Exception as e:
            return {'error': True, 'message': str(e),}    
    
    def get_id(self, model, id, fields):
        result = self._get_uid()
        if not result['error']:
            return result
        try:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            data =  models.execute_kw(self.app.config['RDM_DB_NAME'], result['uid'], self.app.config['RDM_APP_PASSWORD'], model, 'read', [id], {'fields': fields})
            return {'error': False, 'message': '', 'datas': data}
        except Exception as e:
            return {'error': True, 'message': str(e),}

    def create(self, model, vals):
        pass
    
    def write(self, model, id, vals):
        pass
    
    def unlink(self, model, id):
        pass