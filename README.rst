############
Segwarides
############

Segwarides maps names for services to credentials for those services.
These are expected to be services that must be shared by multiple other services.
The initial example is the EFD InfluxDB.
We have low risk (readonly) credentials for the various InfluxDB deployments.
We would like these credentials to be easy to obtain and easy to update without making them public to the whole internet.
There are other low risk services for wich we do not control authentication where a service for providing credentials may be useful.
An example may be a centralized logging service.

This is a Rubin Observatory DM SQuaRE microservice, developed with the `Safir <https://safir.lsst.io>`__ framework and hosted on `Roundtable <https://roundtable.lsst.io>`__.

Usage
=====

Use ``segwarides run`` to start the service.
By default, it will run on port 8080.
This can be changed with the ``--port`` option.

Configuration
-------------

The following environment variables must be set in Segwarides' runtime environment.

* ``CREDENTIAL_PATH``: The service expects the k8s secret containing the credentials to be served to be mounted at this location.

The following environment variables may optionally be set to change default behavior.

- ``SAFIR_PROFILE``: Set to ``production`` to enable production logging
- ``SAFIR_LOG_LEVEL``: Set to ``DEBUG``, ``INFO``, ``WARNING``, or ``ERROR`` to change the log level.
  The default is ``INFO``.

Routes
------

* ``/``: Returns service metadata with a 200 status (used by Google Container Engine Ingress health check)

* ``/segwarides``: Returns metadata about the service.

* ``/segwarides/list``: Returns the names of all service credentials know to the service.

* ``/segwarides/creds/<service_name>``: Returns a JSON object for the service with ``<service_name>``.
  The object is a dictionary of credential keys to the values for each.
  For example, username/password/service endpoint for the EFD service.
  A 404 is returned if there are no credentials for ``<service_name>``.
  A 500 is returned if the service cannot decode the credentials from disk using ``json.load``.

Adding Credentials
------------------

Credentials are served from `Vault <https://www.vaultproject.io/>`__.
The SQuaRE vault service is served from roundtable.
Check 1Password for the relevant credentials.

In order to add a credential, a new key must be added to the ``secret/k8s_operator/roundtable/segwarides/creds`` secret.
The value of the key is a valid JSON document containing the credentials.
The credentials can specify any number of key/value pairs, but for EFD credentials ``host``, ``username``, and ``password`` are expected.
It is assumed this same mechanism can be extended to serve e.g. access tokens as well as username/password pairs.
An example valid document is:

.. code::

  '{"host": "service.endpoint.org", "username": "swordfish", "password": "12345"}'

Since we are using `K/V Version 2 <https://www.vaultproject.io/docs/secrets/kv/kv-v2>`__ we will use the `vault kv patch <https://www.vaultproject.io/docs/commands/kv/patch>`__ command to add credentials to the secret.
Putting it all together, adding a credential looks something like the following:

.. code::

  export VAULT_ADDR=https://secret.vault.location.codes
  export VAULT_TOKEN=<super secret vault token>
  vault kv patch secret/k8s_operator/roundtable/segwarides/creds some_service_name='{"host": "service.endpoint.org", "username": "swordfish", "password": "12345"}'

Segwarides will automatically pick up the change as it re-reads the secret any time a request is made.
Though it may take some time for the kubernetes secret to be refreshed.

Deployment
==========

Segwarides support deployment on Kubernetes via Kustomize using the configuration in ``manifests/base``.
It depends on a Kubernetes secret, a template for which can be found in ``manifests/secret.template.yaml``.

The deployment manifest is pinned to the corresponding version of the Docker image, and thus pinning to a version of the deployment manifest ensures that one is deploying a known version of the Segwarides application.
So, for example, one can wrap this deployment in a Kustomization resource such as:

.. code-block:: yaml

   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization

   resources:
     - github.com/lsst-sqre/segwarides.git//manifests/base?ref=0.1.0
     - resources/secret.yaml

where ``resources/secret.yaml`` provides the required Kubernetes ``Secret`` resource via some local mechanism.
This will install version 0.3.0 of the Segwarides application.

Naming
======

Segwarides is in reference to the name of the knight Safir's brother.
Segwarides was developed using the Safir framework produced by the SQuaRE team.
