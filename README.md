# Oil Price Prediction - an educational project for learning and practicing Python, Data Science, and Machine Learning
This project was created to learn and practice Python, Data Science, and Machine Learning. It is not intended for production use or real-world applications.
The focus is on educational purposes, exploring various libraries, tools, and techniques in the Python ecosystem.
Prediction of oil prices is a complex task that involves various factors, including historical data, market trends, geopolitical events, and economic indicators.
This project aims to build a foundation for understanding how to approach such problems using Python and its libraries but does not guarantee accurate predictions or insights into real-world oil price movements.
Due to the limited scope of this project, nobody can or should expect a working solution for oil price prediction.
But it is a great opportunity to see how challenging it can be to make accurate predictions in a complex domain like oil prices.
## Install
### Install Miniconda
````bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# check the hash
sha256sum ~/miniconda3/miniconda.sh # compare with https://docs.anaconda.com/miniconda/
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
mkdir -p ~/bin
cd ~
ln -s ~/miniconda3/bin/conda conda
````

### create conda environment
````bash
conda create --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge
````
### install conda packages
````bash
conda install --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge
````
### install pip packages
````bash
conda activate oil-price-prediction
pip install -r requirements-dev-pip.txt
````

### create requirements.txt
````bash
conda list -e > requirements.txt
````

### Start development environment
Run the following command in WSL2 to enable the conda environment:
````bash
source /opt/conda/etc/profile.d/conda.sh
conda activate oil-price-prediction
````
Start Jupyter Lab:
````bash
jupyter lab
````

### Install CUDA Toolkit for WSL Ubuntu
* CUDA Toolkit: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network
* cuDNN: https://developer.nvidia.com/rdp/cudnn-download

Install the matching version from:
https://www.tensorflow.org/install/source#gpu

### Install Tensorflow
https://www.tensorflow.org/install
https://www.tensorflow.org/install/pip#windows-wsl2

### create .env file
Copy the example .env file to create your own configuration:
````bash
cp .env.example .env
````
Edit the `.env` file to set your environment variables, such API keys, etc.