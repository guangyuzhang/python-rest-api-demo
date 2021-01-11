import falcon
import json
import mysql.connector
import config
import uuid


class MeterCollection:
    @staticmethod
    def __init__():
        pass

    @staticmethod
    def on_options(req, resp):
        resp.status = falcon.HTTP_200

    @staticmethod
    def on_get(req, resp):
        cnx = mysql.connector.connect(**config.myems_demo_db)
        cursor = cnx.cursor(dictionary=True)

        query = (" SELECT id, name, uuid, description "
                 " FROM tbl_meters "
                 " ORDER BY id ")
        cursor.execute(query)
        rows_meters = cursor.fetchall()

        result = list()
        if rows_meters is not None and len(rows_meters) > 0:
            for row in rows_meters:
                meta_result = {"id": row['id'],
                               "name": row['name'],
                               "uuid": row['uuid'],
                               "description": row['description']}
                result.append(meta_result)

        cursor.close()
        cnx.disconnect()
        resp.body = json.dumps(result)

    @staticmethod
    def on_post(req, resp):
        """Handles POST requests"""
        try:
            raw_json = req.stream.read().decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.ERROR', description=ex)

        new_values = json.loads(raw_json)

        if 'name' not in new_values['data'].keys() or \
                not isinstance(new_values['data']['name'], str) or \
                len(str.strip(new_values['data']['name'])) == 0:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.INVALID_METER_NAME')
        name = str.strip(new_values['data']['name'])

        if 'description' in new_values['data'].keys() and \
                new_values['data']['description'] is not None and \
                len(str(new_values['data']['description'])) > 0:
            description = str.strip(new_values['data']['description'])
        else:
            description = None

        cnx = mysql.connector.connect(**config.myems_demo_db)
        cursor = cnx.cursor()

        cursor.execute(" SELECT name "
                       " FROM tbl_meters "
                       " WHERE name = %s ", (name,))
        if cursor.fetchone() is not None:
            cursor.close()
            cnx.disconnect()
            raise falcon.HTTPError(falcon.HTTP_404, title='API.BAD_REQUEST',
                                   description='API.METER_NAME_IS_ALREADY_IN_USE')

        add_values = (" INSERT INTO tbl_meters "
                      "    (name, uuid, description) "
                      " VALUES (%s, %s, %s) ")
        cursor.execute(add_values, (name,
                                    str(uuid.uuid4()),
                                    description))
        new_id = cursor.lastrowid
        cnx.commit()
        cursor.close()
        cnx.disconnect()

        resp.status = falcon.HTTP_201
        resp.location = '/meters/' + str(new_id)


class MeterItem:
    @staticmethod
    def __init__():
        pass

    @staticmethod
    def on_options(req, resp, id_):
        resp.status = falcon.HTTP_200

    @staticmethod
    def on_get(req, resp, id_):
        if not id_.isdigit() or int(id_) <= 0:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.INVALID_METER_ID')

        cnx = mysql.connector.connect(**config.myems_demo_db)
        cursor = cnx.cursor(dictionary=True)

        query = (" SELECT id, name, uuid, description "
                 " FROM tbl_meters "
                 " WHERE id = %s ")
        cursor.execute(query, (id_,))
        row = cursor.fetchone()
        cursor.close()
        cnx.disconnect()

        if row is None:
            raise falcon.HTTPError(falcon.HTTP_404, title='API.NOT_FOUND',
                                   description='API.METER_NOT_FOUND')
        else:
            meta_result = {"id": row['id'],
                           "name": row['name'],
                           "uuid": row['uuid'],
                           "description": row['description']}

        resp.body = json.dumps(meta_result)

    @staticmethod
    def on_delete(req, resp, id_):
        if not id_.isdigit() or int(id_) <= 0:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.INVALID_METER_ID')

        cnx = mysql.connector.connect(**config.myems_demo_db)
        cursor = cnx.cursor()

        cursor.execute(" SELECT uuid "
                       " FROM tbl_meters "
                       " WHERE id = %s ", (id_,))
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            cnx.disconnect()
            raise falcon.HTTPError(falcon.HTTP_404, title='API.NOT_FOUND',
                                   description='API.METER_NOT_FOUND')

        cursor.execute(" DELETE FROM tbl_meters WHERE id = %s ", (id_,))
        cnx.commit()

        cursor.close()
        cnx.disconnect()

        resp.status = falcon.HTTP_204

    @staticmethod
    def on_put(req, resp, id_):
        """Handles PUT requests"""
        try:
            raw_json = req.stream.read().decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.EXCEPTION', description=ex)

        if not id_.isdigit() or int(id_) <= 0:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.INVALID_METER_ID')

        new_values = json.loads(raw_json)

        # TODO 1: validate meter name in json
        if 'name' not in new_values['data'].keys() or \
                not isinstance(new_values['data']['name'], str) or \
                len(str.strip(new_values['data']['name'])) == 0:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.INVALID_METER_NAME')
        name = str.strip(new_values['data']['name'])
        # TODO 2: validate meter description in json
        if 'description' in new_values['data'].keys() and \
                new_values['data']['description'] is not None and \
                len(str(new_values['data']['description'])) > 0:
            description = str.strip(new_values['data']['description'])
        else:
            description = None

        cnx = mysql.connector.connect(**config.myems_demo_db)
        cursor = cnx.cursor()

        # TODO 3: check if meter id exists
        cursor.execute(" SELECT id  FROM tbl_meters WHERE id = id_")
        if cursor.fetchone() is not None:
            cursor.close()
            cnx.disconnect()
            raise falcon.HTTPError(falcon.HTTP_404, title='API.BAD_REQUEST',
                                   description='API.METER_ID_IS_ALREADY_IN_USE')
        # TODO 4: check if meter name is in use by other meters
        cursor.execute(" SELECT name FROM tbl_meters  WHERE id = id_")
        if cursor.fetchone() is not None:
            cursor.close()
            cnx.disconnect()
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.METER_NAME_IS_ALREADY_IN_USE')
        # TODO 5: update meter in database
        put_values = ("UPDATE tbl_meters set name=%s,description=%s WHERE id=%s")
        cursor.execute(put_values, (name,description,id_))
        cnx.commit()
        cursor.close()
        cnx.disconnect()

        resp.status = falcon.HTTP_200

