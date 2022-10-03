# EpyMix

## Description
This model is based on a SEIR-like model describing canopy growth and epidemic dynamics. The model consists of two organizational levels: the patch level (~1 m²) representing a small crop canopy unit, and the field level which is a bunch of patches computed in a matrix. 
At the patch level, a canopy is simulated with simple growth functions, representing one given crop, or two crops at a time (i.e. uniform mixture). The difference between crop species is first of all defined by disease susceptibility: a susceptible crop is defined as wheat, while a qualitatively resistant crop is another ‘abstraction’ crop. Within each patch, there is no explicit-spatial structure, but one or two sets of parameters for growth, phenology, planting date and canopy porosity depending on the number of crops. Plant-plant interactions and plant resource dynamics are not modelled. Regarding the epidemic, infection, spore production and spore interception are modelled at the patch level. 
At the field level, the patches are explicitly spatially structured along a matrix. Thereby, the relative crop proportions can be changed at both the patch and the field level. The explicit spatial structure of patches within the field allows to simulate different spatial arrangement. Regarding the epidemic, spore dispersion kernel and gradients are modelled at the field level. The calibration of the spore dispersion kernel determines the scale, such as we wanted that a patch is approximately 1m². 
Time is measured in degree-days (dd) and denoted by t. A cropping season starts at tstart corresponding to the sowing date, ends at tend, corresponding to the harvesting date, and T is the length of the experiment, such that T/tend gives the number of cropping season of the experiment. The inter-cropping season is modelled as an instantaneous projection from tend to the start of the next cropping year. 
The modelled diseases (rust and septoria) are associated with two different set of parameters.

## Authors
Jonathan Sanner (Ecole Normale Supérieure, CERES)
David Claessen (Ecole Normale Suéprieure, CERES)
Corinne Robert (INRAE, UMR EcoSys)
Sébastien Levionnois (INRAE, UMR EcoSys & AGAP)
Christophe Pradal (CIRAD & INRIA, UMR AGAP)
Christian Fournier (INRAE, UMR LEPSE)

## Installation


Conda environement : https://docs.conda.io/en/latest/index.html

#### User

    conda create -n epymix -c openalea3 -c conda-forge openalea.epymix notebook matplotlib
    conda activate epymix

#### Developer

##### Create a new environment with EpyMix installed in there :

    conda create -n epymix -c conda-forge python=3 scipy
    conda activate epymix

	
    # (Optional) tools
    conda install -c conda-forge ipython jupyter pytest
  
    # download EpyMix and install
    git clone https://github.com/openalea-incubator/epymix
    cd epymix
    python setup.py develop


### License

Our code is released under **Cecill-C** (https://cecill.info/licences/Licence_CeCILL_V1.1-US.txt) licence. (see LICENSE file for details).
