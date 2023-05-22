from openalea.core import *

__name__ = "ipmdecisions.epymix"
__version__ = '1.0.0'
__license__ = 'CECILL-C'
__authors__ = 'Sebastien Levionnois, Christophe Pradal, ...'
__institutes__ = 'INRAE/CIRAD'
__description__ = 'Intercropping for pest management'
__url__ = 'https://github.com/openalea-incubator/epymix'

__editable__ = 'True'
__icon__ = 'icon.png'
__alias__ = ["EpyMix"] # Aliases for compatibitity

__all__ = """
rain
inoculum
configuration
dispersion_kernel_rust
dispersion_kernel_septo
growth_pea
SEIR
""".split()

"""

.split()
"""

rain = Factory(name='rain',
                 category='Environment',
                 nodemodule='adaptor',
                 nodeclass='rain',
                 outputs=[dict(name='precipitation', interface='ISequence')],
                 )

inoculum = Factory(name='inoculum',
                 category='Initialization',
                 nodemodule='adaptor',
                 nodeclass='inoculum',
                 outputs=[dict(name='inoculum', interface='ISequence'),
                          dict(name='ng_ext', interface='IInt')],
                 )

configuration = Factory(name='configuration',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='configuration',
                 outputs=[dict(name='arrangement', interface='ISequence')],
                 )

dispersion_kernel_rust = Factory(name='dispersion_kernel_rust',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='dispersion_kernel_rust',
                outputs=[dict(name='kernel_ure', interface='ISequence'),
                          dict(name='C_Disp_ure', interface='IInt')],

                 )

dispersion_kernel_septo = Factory(name='dispersion_kernel_septo',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='dispersion_kernel_septo',
                outputs=[dict(name='kernel_asco', interface='ISequence'),
                          dict(name='C_Disp_asco', interface='IInt'),
                          dict(name='kernel_pycnid', interface='ISequence'),
                          dict(name='C_Disp_pycnid', interface='IInt'),
                          ],
                 )

growth_pea = Factory(name='growth_pea',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='growth_pea',
                 outputs=[dict(name='Pth_inde', interface='ISequence'),
                          dict(name='Pea_inde', interface='ISequence')]
                 )

SEIR = Factory(name='SEIR',
                 category='Main function',
                 nodemodule='adaptor',
                 nodeclass='SEIR',
                 outputs=[
                     dict(name='Nsp', interface='ISequence'),
                     dict(name='Pth', interface='ISequence'),
                     dict(name='Poi', interface='ISequence'),
                     dict(name='Sth', interface='ISequence'),
                     dict(name='Sus', interface='ISequence'),
                     dict(name='Lat', interface='ISequence'),
                     dict(name='Ifc', interface='ISequence'),
                     dict(name='Ifv', interface='ISequence'),
                     dict(name='Rem', interface='ISequence'),
                     dict(name='LAI', interface='ISequence'),
                     dict(name='LAI_wheat', interface='ISequence'),
                     dict(name='Poo', interface='ISequence'),
                     dict(name='Eps', interface='ISequence'),
                     dict(name='AUDPC', interface='ISequence'),
                     dict(name='Scont', interface='ISequence'),
                 ]
                 )
