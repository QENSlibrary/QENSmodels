Lorentzian
==========
Definitions
-----------
Syntax
~~~~~~

A Lorentzian function is defined as:

.. math::

   \text{Lorentzian}(x, \text{scale_factor}, \text{peak_centre}, \text{fwhm})
    = \frac{\text{scale_factor}}{\pi}\frac{\frac{1}{2}\text{fwhm}}{(x-\text{peak_centre})^2+\big(\frac{1}{2}\text{fwhm}\big)^2}

Parameters
~~~~~~~~~~

.. table::

   +------------------+---------------+-----------------------------+
   | Name             | Default Value | Description                 |
   +==================+===============+=============================+
   | ``scale_factor`` | 1.0           | Scale factor                |
   +------------------+---------------+-----------------------------+
   | ``peak_centre``  | 0.0           | Centre of peak              |
   +------------------+---------------+-----------------------------+
   | ``fwhm``         | 1.0           | Full Width at Half Maximum  |
   +------------------+---------------+-----------------------------+

.. NOTE::

   - Note that the maximum of a Lorentzian is :math:`\text{Lorentzian}(\text{PeakCentre},
     \text{ScaleFactor}, \text{PeakCentre}, \text{FWHM})=\frac{2}{\pi}\frac{ \text{ScaleFactor}}{\text{FWHM}}`.

   - **Equivalence**
    ``Lorentzian`` corresponds to the following implementations in
    `Mantid <http://docs.mantidproject.org/nightly/fitfunctions/Lorentzian.html>`_ and
    `DAVE <https://www.ncnr.nist.gov/dave/documentation/pandoc_DAVE.pdf>`_

    +------------------+-----------------+------------------+
    | Equivalence      | Mantid          |  DAVE            |
    +==================+=================+==================+
    | ``Lorentzian``   | ``Lorentzian``  |  ``Lorentzian``  |
    +------------------+-----------------+------------------+
    | ``scale_factor`` | Amplitude       |  A               |
    +------------------+-----------------+------------------+
    | ``peak_centre``  | PeakCentre      |  :math:`x_0`     |
    +------------------+-----------------+------------------+
    | ``fwhm``         | FWHM            | W                |
    +------------------+-----------------+------------------+


References
----------

None.


Authorship and verification
---------------------------

* **Author**
