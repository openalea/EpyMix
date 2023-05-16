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
                 )

inoculum = Factory(name='inoculum',
                 category='Initialization',
                 nodemodule='adaptor',
                 nodeclass='rain',
                 )

configuration = Factory(name='configuration',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='configuration',
                 )

dispersion_kernel_rust = Factory(name='dispersion_kernel_rust',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='dispersion_kernel_rust',
                 )

dispersion_kernel_septo = Factory(name='dispersion_kernel_septo',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='dispersion_kernel_septo',
                 )

growth_pea = Factory(name='growth_pea',
                 category='Additional function',
                 nodemodule='adaptor',
                 nodeclass='growth_pea',
                 )

SEIR = Factory(name='SEIR',
                 category='Main function',
                 nodemodule='adaptor',
                 nodeclass='SEIR',
                 )
"""
order_param = Factory(name='order parameters',
                   description='Set of parameters for each tree order of the weber and Penn model',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='order_parameters',
                   )

tree_param = Factory(name='tree parameters',
                   description='Set of parameters of weber and penn model.',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='tree_parameters',
                   )

quaking_aspen = Factory(name='quaking aspen',
                   description='Quaking Aspen parameters',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='quaking_aspen',
                   )

black_tupelo = Factory(name='black tupelo',
                   description='Black Tupelo parameters',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='black_tupelo',
                   )

black_oak = Factory(name='black oak',
                   description='Black Oak parameters',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='black_oak',
                   )

weeping_willow = Factory(name='weeping willow',
                   description='Weeping Willow parameters',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='weeping_willow',
                   )

weber_penn = Factory(name='weber and penn',
                   description='Tree generation from parameters.',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn',
                   )

weber_penn_markov = Factory(name='weber and penn (markov)',
                   description='Tree generation from parameters.',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn_markov',
                   )

weber_penn_mtg = Factory(name='weber and penn (mtg)',
                   description='Geometric solver using Weber and Penn parameters on MTG.',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn_mtg',
                   )

species = Factory(name='species',
                   description='Tree parameters for the Weber and Penn model.',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='Species',
                   )

read_arbaro = Factory(name='read arbaro xml',
                   description='Import weber and penn parameters from Arbaro software.',
                   category='Simulation',
                   nodemodule='trunk_parameters',
                   nodeclass='import_arbaro',
                   inputs = [dict(name='filename', interface=IFileStr('*.xml')),],
                   )



"""
