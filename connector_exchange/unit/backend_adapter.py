# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from pyews.pyews import WebCredentials, ExchangeService
from pyews.soap import SoapClient

from openerp.addons.connector.unit.backend_adapter import BackendAdapter

_logger = logging.getLogger(__name__)


class ExchangeLocation(WebCredentials):

    def __init__(self, url, user, pwd, cert=False):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.cert = cert


class ExchangeAdapter(BackendAdapter):
    def __init__(self, connector_env):
        """
        :param connector_env: current environment (backend, session, ...)
        :type connector_env: :class:`connector.connector.ConnectorEnvironment`
        """
        super(BackendAdapter, self).__init__(connector_env)
        backend = self.backend_record

        # Embed a ExchangeService instance in the backend adapter
        self.ews = ExchangeService()
        self.init_soap_client(backend.location,
                              backend.username,
                              backend.password,
                              backend.certificate_location
                              )

    def init_soap_client(self, location, user, passwd, cert):
        self.ews.soap = SoapClient(location, user=user, pwd=passwd, cert=cert)

    def set_primary_smtp_address(self, user):
        subst = {
            'u_login': user.login,
            'exchange_suffix': user.company_id.exchange_suffix or '',
        }
        self.ews.primary_smtp_address = (
            str("%(u_login)s%(exchange_suffix)s" % subst)
        )