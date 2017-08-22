from collections import OrderedDict
import pymssql
from django.conf import settings


class Singleton(type):
    '''
    Singleton class meta class
    '''
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class QueryManager(metaclass=Singleton):
    """
    This class handles DB connection and
    contains query methods
    """

    def _get_connection(self):
        """
        Connect to MSSQL database and return
        connection object
        :return:
        """

        conn = None

        try:
            conn = pymssql.connect(
                settings.DB.get('host'),
                settings.DB.get('user'),
                settings.DB.get('password'),
                settings.DB.get('database')
                )
        except:
            raise Exception('Cant establish connection with database')
        return conn


    def insert_data_into_cdr_plus_sip_tbl(self, data):
        """
        Insert data into OLRDialer.dbo.STG_Rpt_1074092348_CDR_Plus_SIP table
        :param data:
        :return: Bool value
        """


        conn = self._get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO OLRDialer.dbo.STG_Rpt_1074092348_CDR_Plus_SIP \
                    (" \
                        "master_contact_id, " \
                        "Contact_Code, " \
                        "media_name, " \
                        "contact_name, "\
                        "ANI_DIALNUM, " \
                        "skill_no, " \
                        "skill_name, " \
                        "X_CDN, " \
                        "X_ANI, " \
                        "X_Call_Type,"\
                        "X_connid, " \
                        "X_RCLevel, " \
                        "X_Loyalty, " \
                        "X_ConfirmationNumber, " \
                        "X_LastName, "\
                        " X_FirstName, " \
                        "X_IRC, " \
                        "X_Genesys_CallUUID, " \
                        "X_AgentID" \
                    ")\
	                VALUES('{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',                     '{}','{}','{}','{}', '{}')"

            cursor.execute(
                query.format(
                    data.get('master_contact_id'),
                    data.get('Contact_Code'),
                    data.get('media_name'),
                    data.get('contact_name'),
                    data.get('ANI_DIALNUM'),
                    data.get('skill_no'),
                    data.get('skill_name'),
                    data.get('X_CDN'),
                    data.get('X_ANI'),
                    data.get('X_Call_Type'),
                    data.get('X_connid'),
                    data.get('X_RCLevel'),
                    data.get('X_Loyalty'),
                    data.get('X_ConfirmationNumber'),
                    data.get('X_LastName'),
                    data.get('X_FirstName'),
                    data.get('X_IRC'),
                    data.get('X_Genesys_CallUUID'),
                    data.get('X_AgentID')
            )
            )
            conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            conn.close()

    def fetch_data_from_cdr_plus_sip_tbl(self):
        """
        Fetch data from OLRDialer.dbo.STG_Rpt_1074092348_CDR_Plus_SIP table
        :param
        :return: row data
        """

        conn = self._get_connection()
        cursor = None
        data = []
        try:
            cursor = conn.cursor()
            query = "SELECT * from OLRDialer.dbo.STG_Rpt_1074092348_CDR_Plus_SIP"
            cursor.execute(query)
            res = cursor.fetchall()
            if res and len(res) > 0:
                column_names = [item[0] for item in cursor.description]
                for row in res:
                    data.append(self.return_object(column_names, row))
                return data
        except Exception as e:
            raise Exception(e)
        finally:
            conn.close()

    def return_object(self, columns, res):
        """
        Crate object from input row data and return to caller
        :param res:
        :return:
        """

        if isinstance(res, list):
            row = dict(zip(columns, res[0]))
        else:
            row = dict(zip(columns, res))
        return row