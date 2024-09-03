# import module
# interact with an Odoo server via its XML-RPC API
import xmlrpc.client

# define connection parameters
url = 'http://localhost:8069'
db = 'v16_ce_amani_demo3'
username = 'admin'
password = 'admin'

# create a Server Proxy
# common proxy object
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# Fetching and Printing Version Information
print("Version info : ", common.version())

#authentication
uid = common.authenticate(db, username, password, {})
if uid:
    print("Authentication success")

    # create a model Proxy
    # proxy object
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Performing Operations

    # search method
    partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'limit': 7})
    print("Partners : ", partners)
    # search count method
    partners_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
    print("Partners_count : ", partners_count)
    # read method
    partner_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partners], {'fields': ['id', 'name']})
    print("Partners_rec : ", partner_rec)

    # search read : comnination of search and read method
    partner_rec2 = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]],
                                     {'fields': ['id', 'name']})
    print("Partner rec2 : ", partner_rec2)

    # create method
    vals = {
        'name': "Odoo Mates External API",
        'email': "odoomates@gmail.com"
    }
    created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
    print("created record ->", created_id)

    # write method (update)
    partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'odoomates@gmail.com']]])
    print(partners)
    models.execute_kw(db, uid, password, 'res.partner', 'write', [partners, {'mobile': "3333333", "phone": "88888888"}])

    # delete method
    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [partners])

else:
    print("Authentication failed")
