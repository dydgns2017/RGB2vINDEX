# RGB2vINDEX

RGB image to vINDEX, vINDEX = {TGI, GLI, VARY, VIgreen, vNDVI}

## Installation

```
conda create -n vINDEX python=3.9
conda activate vINDEX
conda install -c conda-forge opencv
pip install numpy pyvips ## have to install vips-dev lib on window OS
## Linux
# apt install -y libvips
```

## Equation of vINDEX

#### TGI (Triangular Greeness Index)
------------------------------------

$$ TGI = { (\lambda_{Red}-\lambda_{Blue})(\rho_{Red}-\rho_{Green}) - (\lambda_{Red}-\lambda_{Green})(\rho_{Red}-\rho_{Blue}) \over 2} $$

#### VARI (Visible Atmospheric Resistant Index)
------------------------------------
$$ VARI = { Green-Red \over Green+Red-Blue} $$

#### GLI(Green Leaf Index)
------------------------------------

$$ GLI = { (Green-Red) + (Grren-Blue) \over (2*Green)+Red+Blue} $$

#### VIgreen(Visible Atmospherically Resistant Indices Green)
------------------------------------

$$ VI_{Green} = { R_{green} - R_{red} \over R_{green} + R_{red}} $$

#### vNDVI(visible NDVI)
------------------------------------

$$ vNDVI = F (camera, red, green, blue) = C ∗ (red^{w1} ∗ green^{w2} ∗ blue^{w3}) $$

## Code Example

```bash
# python RGB2GREEN.py --generate TGI|VARI|GLI|VIgreen|vNDVI --dataset dataset, relative path
python RGB2GREEN.py --generate GLI --datasets dataset
```

## Reference

- https://www.l3harrisgeospatial.com/docs/broadbandgreenness.html
- https://github.com/OpenDroneMap/WebODM
- https://www.sciencedirect.com/science/article/pii/S016816991932383X
- https://gitmemories.com/awesome-spectral-indices/awesome-spectral-indices
- https://github.com/dirceu-jr/pyvips-NDVI-and-VARI/blob/master/colormaps.py