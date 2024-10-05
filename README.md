# Install
## create conda environment
````bash
conda create --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge
````
## install conda packages
````bash
conda install --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge
conda create --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge

````
## install pip packages
````bash
pip install -r requirements-dev-pip.txt
````

## create requirements.txt
````bash
conda list -e > requirements.txt
````

## Start development environment
Run the following command in WSL2 to enable the conda environment:
````bash
source /opt/conda/etc/profile.d/conda.sh
conda activate oil-price-prediction
````
Start Jupyter Lab:
````bash
jupyter lab
````

## Install CUDA Toolkit for WSL Ubuntu
* CUDA Toolkit: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network
* cuDNN: https://developer.nvidia.com/rdp/cudnn-download

Install the matching version from:
https://www.tensorflow.org/install/source#gpu

## Install Tensorflow
https://www.tensorflow.org/install
https://www.tensorflow.org/install/pip#windows-wsl2