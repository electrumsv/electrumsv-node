The ElectrumSV node project
===========================

The ElectrumSV node project is intended to provide cross-platform and easily runnable builds of
the node software for developers to develop, test and experiment with.  While ElectrumSV wallet
uses these builds for it's automated testing processes, and in other situations, these builds are
not ElectrumSV-specific in any way. However, as ElectrumSV is a trusted project in the Bitcoin SV
ecosystem, by curating these builds we can provide them in a form developers can trust.

You are more than welcome to get involved and help us make our builds even better.

The goal of the developers of the official `Bitcoin SV node project`__, is to release nodes for
miners to use. It would drain their resources to also have to focus on creating cross-platform
development environments for application developers. For this reason, they only provide Linux
builds themselves.

__ https://bitcoinsv.io/node-software/

.. important::
   Head on over to `electrumsv.io/node-project <https://electrumsv.io/node-project>`_ to find the node project
   home page, and links to the latest archived builds.

Possible uses
-------------

* Run your application against a local blockchain you control, generating both blocks and coins
  when you need them.
* Stress test your application with continual reorgs, ensuring your handling is robust.
* Develop offline, whether due to travel or productivity reasons, taking advantage of your
  ability to access a blockchain without network connectivity.

.. toctree::
   :maxdepth: 2
   :caption: Using our builds

   /release-artifacts/python-packages
   /release-artifacts/archived-binaries

