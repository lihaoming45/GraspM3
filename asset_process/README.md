# Asset process

This folder is for processing object models. For ShadowHand, the objects are based on the DexGraspNet. For the MANO hand, the objects are based on Obman, GRAB, and ContactPose.
For each object we filer out non-manifolds and models of small volumes, and calculate the sign ditacne field (sdf) as the input of out TPNP optimization. 

### Download object meshes
 - Download object models from DexGraspNet
   -- following the guidance of the [DexGraspNet](https://github.com/PKU-EPIC/DexGraspNet/tree/main/asset_process) Extraction to download the object mesh.
   ```bash
   # ShapeNetCore
   python extract.py --src data/ShapeNetCore.v2 --dst data/raw_models --set core # replace data root with yours
   ```


### MeshToSDF

you can run the following command to calculate the object sdf.

```bash
python ./mesh_to_sdf.py --grab-path $GRAB_DATASET_PATH \

```

Other dependencies are simple python packages.

```bash
pip install tqdm
pip install trimesh
pip install lxml
pip install networkx
```

## Usage

We process our object models as the following pipeline. If you have some object models and want to synthesize grasps, we recommand you to follow this pipeline to process these models too.

- Extraction: Organize models into a folder.
- Manifold: Use ManifoldPlus to convert raw models into manifolds robustly.
- Normalization: Adjust centers and sizes of models. Then filter out bad models.
- Decomposition: Use CoACD to decompose models and export urdf files for later physical simulation.

Below are sources of our object datasets:

- [ShapeNetCore](https://shapenet.org/)
- [ShapeNetSem](https://shapenet.org/)
- [Mujoco](https://github.com/kevinzakka/mujoco_scanned_objects)
- [DDG](https://gamma.umd.edu/researchdirections/grasping/differentiable_grasp_planner)(Deep Differentiable Grasp)

### Extraction

```bash
# ShapeNetCore
python extract.py --src data/ShapeNetCore.v2 --dst data/raw_models --set core # replace data root with yours
# ShapeNetSem
python extract.py --src data/ShapeNetSem/models --dst data/raw_models --set sem --meta data/ShapeNetSem/metadata.csv
# Mujoco
python extract.py --src data/mujoco_scanned_objects/models --dst data/raw_models --set mujoco
# DDG
python extract.py --src data/Grasp_Dataset/good_shapes --dst data/raw_models --set ddg
```

### Manifold

```bash
python manifold.py --src data/raw_models --dst data/manifolds --manifold_path ../thirdparty/ManifoldPlus/build/manifold
```

This generates `run.sh`. Then run it with:

```bash
bash run.sh
# or poolrun.py runs it in multiprocess
python poolrun.py -p 32
```

### Normalization

```bash
python normalize.py --src data/manifolds --dst data/normalized_models
```

### Decomposition

```bash
python decompose_list.py --src data/normalized_models --dst data/meshdata --coacd_path ../thirdparty/CoACD/build/main
```

Again this generates `run.sh`.

```bash
bash run.sh
# or
python poolrun.py -p 32
```

The structure of the final object dataset for shadow hand is:

```bash
meshdata
+-- source(-category)-code0
|  +-- coacd
|  |  +-- coacd.urdf
|  |  +-- decomposed.obj
|  |  +-- decomposed.sdf
|  |  +-- coacd_convex_piece_0.obj
|  |  +-- coacd_convex_piece_1.obj
|  |  ...
+-- source(-category)-code1
...
```