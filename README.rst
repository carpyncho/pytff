=====
pytff
=====

Wrapper arround G. Kovacs & G. Kupi Template Fourier Fitting

Setup
------

In all cases you need to download and compile
`Template Fourier Fitting <http://www.konkoly.hu/staff/kovacs/tff.html>`_
parameters file (``tff.par``) and  the Template Fourier decompositions file
(``template.dat``) are not necesary.

You can compile (in posix) the ``tff.f`` with the command

.. code-block:: bash

    $ gfortran tff.f -o tff

Basic Install
-------------

Execute

.. code-block:: bash

    $ pip install pytff

or

.. code-block:: bash

    $ easy_install pytff


Development Install
-------------------

1.  Clone this repo and then inside the local
2.  Execute

    .. code-block:: bash

        $ pip install -e .

    or

    .. code-block:: bash

        $ pip install numpy
        $ python setup.py develop


Global Configuration
--------------------

You can edit the file ``~/.config/pytff/pytff.rc`` (on posix) or
``~\APPDATA\roaming\pytff\pytff.rc`` (on windows); for setup the
location of your *tff* binary and your working directory. The file
look like


.. code-block:: ini

    [pytff]
    wrk_path =
    tff_cmd = tff


Where:

-   `tff_cmd` is the full path to the tff command if is empty or not preset
    *tff* is the default value.
-   `wrk_path` the default working directory of tff, by default every
    instance creates their own temp directory.


Tutorial
--------

https://github.com/carpyncho/pytff/blob/master/tutorial.ipynb


Legal
-----

This project is part of `Carpyncho <http://carpyncho.jbcabral.org>`_

-   The data of `tff.par` and `template.dat` is property of G. Kovacs
    & G. Kupi
-   The `dataset:single_dat` and `dataset:split_dat` is property of the
    `OGLE Experiment <http://ogle.astrouw.edu.pl/>`_


Authors
-------

Juan BC

jbc.develop@gmail.com

`IATE <http://iate.oac.uncor.edu/>`_ - `URN <http://unr.edu.ar/>`_

