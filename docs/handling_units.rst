Handling of units
#################

.. |Ang| unicode:: U+212B
.. |Ang^-1| replace:: |Ang|\ :sup:`-1`
.. |Ang^2| replace:: |Ang|\ :sup:`2`
.. |Ang^-2| replace:: |Ang|\ :sup:`-2`

Introduction
************

At present the QENS models library contains a set of models aimed to fit :math:`S(Q, \hbar\omega)`
quasielastic neutron scattering (QENS) data [#f1]_ . As there does not yet exist a standard format for
:math:`S(Q,\hbar\omega)` data, it remains a user task to write the appropriate loader to read the
data. The library is unit agnostic and does not make any assumption about the units of the input
data.
As a consequence, if no additional information is given, any output parameter will be given in the
same units as the input data. Further information and examples are given below. The *QENS library*
also contains a few tools to help with converting units (see
`Convert_units.ipynb <https://github.com/QENSlibrary/QENSmodels/blob/master/tools/Convert_units.ipynb>`_ )

:math:`S(Q,\hbar\omega)`
************************


The dynamical structure factor should be given in units of :math:`[energy]^{-1}`
(:math:`[E]^{-1}`), although in many cases :math:`S(Q,\hbar\omega)` is not obtained in absolute
units and the fitted data will be simply given in arbitrary units. In this case, the global scaling
factor used in the fitting model will also be just an arbitrary number and its units can be
ignored.
Otherwise, if the input data were carefully normalized and the dynamical structure factor is given
in absolute units, then this scaling factor will be given also in :math:`[E]^{-1}` units.

:math:`Q`
*********

The wavevector transfer :math:`Q` has units of :math:`[length]^{-1}` (:math:`[L]^{-1}`). Typically
this is given in |Ang^-1|, but it is not uncommon to use :math:`nm^{-1}`.

:math:`\hbar\omega` (or :math:`\omega` or :math:`\nu` or :math:`\nu/c`)
***********************************************************************

The energy exchange has units of energy and is commonly expressed in :math:`meV`. However, many
other units are also used in the literature. For example, for backscattering experiments it is
quite usual to use :math:`\mu eV` instead of :math:`meV`. It is also relatively common (especially
when comparing with simulation data) to use just the angular frequency :math:`\omega` (often given
in :math:`rad.ps^{-1}` or :math:`rad^{-1}`) or the frequency :math:`\nu` (often in :math:`THz`, but
also in :math:`GHz` or :math:`Hz`). In this case the input units are of dimension
:math:`[time]^{-1}` (:math:`[T]^{-1}`).


.. Finally, in optical spectroscopy it is usual to use the optical wavevector :math:`\nu/c` in
.. :math:`cm^{-1}`, *i.e.* :math:`[L]^{-1}`. Therefore it is not uncommon that neutron vibrational
.. spectrometers provide data in :math:`cm^{-1}`. However, as this is not of common use in QENS
.. spectroscopy, we will not consider that case.

Output units
************

As said above, the units of the output parameters will correspond to the units of the input data.
This implies that it remains the user responsibility to understand the nature of the parameters in
each model in order to determine their units, and then to convert the output values to any other
physical unit [#f2]_ . A few examples to show how this can be done are given below.

Lorentzian or Gaussian models
=============================

Let’s start with the most common case: :math:`S(Q, \hbar\omega)` is in arbitrary units, :math:`Q`
is given in |Ang^-1|, and :math:`\hbar\omega` is in |Ang^-1| and we are fitting a
single Lorentzian. The three output parameters that we will get are:

* the amplitude of the Lorentzian, *scale*, given in arbitrary units,
* its position, *center*, given in :math:`meV`,
* and its half-width at half-maximum, *hwhm*, also given in :math:`meV`.

It follows naturally that if the energy transfer is given in :math:`\mu eV`, then *center* and
*hwhm* will be returned also in :math:`\mu eV`. Similarly if the input data contain
:math:`S(Q, \omega)` or :math:`S(Q, \nu)` instead of :math:`S(Q, \hbar\omega)`, the frequency is
given in :math:`rad/ps` or :math:`THz`, respectively.

In this case, the standard unit conversion tables can be used to convert directly to the desired
units, *e.g.*:
 *	`List of conversion factors for neutron scattering <https://www.ncnr.nist.gov/instruments/dcs/dcs_usersguide/Conversion_Factors.pdf>`_
 *	`Documentation about units in Mantid <https://docs.mantidproject.org/nightly/concepts/UnitFactory.html>`_
 *	`ILL online tool Neutron scattering conversion factors <https://www.ill.eu/fileadmin/user_upload/ILL/3_Users/Support_labs_infrastructure/Software-tools/DIF_tools/neutrons.html>`_

The same applies to the Gaussian model, with *sigma* replacing *hwhm*.

Self-diffusion coefficient
==========================

Let's start with the simplest model, *Brownian Translational Diffusion*. This model has also three
parameters. :math:`Scale` and :math:`center` will be treated as above. The third parameter is the
self-diffusion coefficient, :math:`D`, which is related to the half-width at half-maximum
:math:`\Gamma` of the Lorentzian function by the relation :math:`\Gamma = DQ^2`. Thus
:math:`D = \Gamma/Q^2` and its units will be :math:`E.L^2` if the input data was
:math:`S(Q, \hbar\omega)` or :math:`T^{-1}L^2` if the input data was :math:`S(Q, \omega)` or
:math:`S(Q, \nu)`.

So if we fit :math:`S(Q, \hbar\omega)` data with :math:`Q` in |Ang^-1| and
:math:`\hbar\omega` in :math:`meV`, :math:`D` will be given in |Ang^-1| :math:`.meV`. The output value
can be converted to more standard units for the self-diffusion coefficient by noting that
:math:`1` |Ang| :math:`= 10^{-10}\ m` and :math:`\hbar\omega = 1\ meV` corresponds to
:math:`\omega=1.519.10^{12}\ rad/s`, giving [#f3]_ :

:math:`1` |Ang^2| :math:`.meV = 1.519.10^{-8} m^2/s = 1.519.10^{-4} cm^2/s = 1.519` |Ang^2| :math:`/ps`


If the energy transfer is given in :math:`\mu eV` instead of :math:`meV`, then :math:`D` will be
obtained in |Ang^2| :math:`.\mu eV`, and we would need to apply:

:math:`1` |Ang^2| :math:`.\mu eV = 1.519.10^{-11} m^2/s = 1.519.10^{-7} cm^2/s = 1.519.10^{-3}` |Ang^2| :math:`/ps`


If :math:`Q` is in :math:`nm^{-1}`, then we would have :math:`D` in :math:`nm^2`.meV` or
:math:`nm^2.\mu eV`, and:

:math:`1 nm^2.meV = 1.519.10^{-6} m^2/s = 1.519.10^{-2} cm^2/s = 151.9` |Ang^2| :math:`/ps`
:math:`1 nm^2.\mu eV = 1.519.10^{-9} m^2/s = 1.519.10^{-5} cm^2/s = 1.519.10^{-1}` |Ang^2| :math:`/ps`


If the input data correspond to :math:`S(Q, \omega)` with :math:`\omega` in :math:`rad/ps`, then
:math:`D` will be obtained directly in |Ang^2| :math:`/ps` (if :math:`Q` was in |Ang^-1|) or in
:math:`nm^2/ps` (if :math:`Q` was in :math:`nm^{-1}`).

Finally, if the input is :math:`S(Q, \nu)` with :math:`\nu` in THz and :math:`Q` in
|Ang^-1|, then :math:`D` will be in |Ang^2| :math:`.THz`, and:

:math:`1` |Ang^2| :math:`.THz = 6.283.10^{-12} m^2/s = 6.283.10^{-8} cm^2/s = 6.283.10^{-4}` |Ang^2| :math:`/ps`

Naturally, the same unit conversions can be applied to the parameter :math:`D` in the
Chudley-Elliot, jump translational diffusion, or the Gaussian localized diffusion models, or in any
other derived model where :math:`D` represents a translational diffusion coefficient.

Distance parameters (*e.g.* jump length or radius)
================================================

They appear in many models, *e.g.* :math:`L` in the Chudley-Elliot model for translational
diffusion, or radius in the models of jumps among equivalent sites in a circle (simple or including
a log-norm distribution) and isotropic rotational diffusion. They are in units of [:math:`L`],
*i.e.* the inverse of the units of :math:`Q`, so if the input contains :math:`Q` in
|Ang^-1|, then the output will be the length or radius in |Ang|, while if :math:`Q`
was given in :math:`nm^{-1}`, they will be returned in :math:`nm`.

The same applies to the parameter :math:`\langle u_x^2\rangle`, quantifying the size of the region
in which the particle is confined in the Gaussian model for localized diffusion [#f4]_ . In this
case, :math:`\langle u_x^2\rangle`is in units of :math:`L^2`, so typically the parameter returned
by the model will be in |Ang^2| (if :math:`Q` was in |Ang^-1|) or in :math:`nm^2` (if
:math:`Q` was in :math:`nm^{-1}`).

Time parameters
===============

At present, the only time parameter appearing in the library of models is the residence time in a
given site, called *resTime* in the jump translational diffusion and jump between equivalent sites
in a circle (both simple or using a log-norm distribution or residence times) models. Its unit is
naturally in terms of time (:math:`T`), but if the input data correspond to
:math:`S(Q, \hbar\omega)`, the resulting residence time will be given in :math:`E^{-1}` units.
Therefore, in the most common case where we have experimental data with the energy transfer given
in :math:`meV`, the fit will give us a residence time :math:`\tau` in :math:`meV^{-1}` which can be
easily transformed to time units:

.. math::

   1 meV^{-1} = 6.583.10^{-13} s = 0.6583 ps


Rotational diffusion coefficient
================================

At present, this parameter appears only in the isotropic rotational diffusion model. It is named
*DR* and it will have units of :math:`E` if the input is :math:`S(Q, \hbar\omega)`, or
:math:`T^{-1}` if the input is :math:`S(Q, \omega)`. In the first case, the result can be converted
to the expected inverse time units easily:

.. math::

	1 meV = 1.519.10^{12} s^{-1} = 1.519 ps^{-1}


Adimensional parameters
=======================

Although they do not require any conversion, they are listed here for completeness.

 * *A0*, *A1*, *A2* in models formed by the sum of several functions (*e.g.*  *delta_lorentz*).
 * *Nsites* defining the number of sites in a circle,
   **which should not be an adjustable parameter**, in *equivalent_sites_circle* and
   *jump_sites_log_norm_dist*.
 * *Sigma* describing the width of the log-norm distribution in *jump_sites_log_norm_dist*.



.. rubric:: Footnotes

.. [#f1] In the future the library could be extended to other types of models, *e.g.* inelastic or
         *I(Q,t)* models.

.. [#f2] As sometimes this can be confusing and a source of errors, we are working on implementing
         the possibility of declaring which are the units used in the input data and the desired
         units for the output data. Then the conversion will be done at the end of the fit and the
         final parameters given already in the units preferred by the user. TO DO!

.. [#f3] Conversions done using the values appearing in the NIST conversion table.

.. [#f4] F. Volino, J.-C. Perrin, and S. Lyonnard, *J. Phys. Chem. B* **110**, 11217-11223 (2006).
